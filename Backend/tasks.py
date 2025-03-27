import os
from worker import celery
from models import User, Role,BoughtProducts, db, Product as product_model
from sqlalchemy import and_
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv

from datetime import datetime, timedelta
from json import dumps
from httplib2 import Http

from jinja2 import Template

@celery.task(bind=True)
def export_manager_csv(self, user_id):
        products = product_model.query.filter_by(user_id=user_id).all()
        bought_items = BoughtProducts.query.all()
        match_item = []
        match_product = {}

        for product in products:
            match_product[product.id] = {'product': product, 'sold_count': 0}

        for item in bought_items:
            if item.product_id in match_product:
                match_item.append(item)
                match_product[item.product_id]['sold_count'] += 1

        csv_folder_path = os.path.join(os.getcwd(), 'csv_files')

        if not os.path.exists(csv_folder_path):
            os.makedirs(csv_folder_path)

        fieldnames = ['Product Id', 'Product Name', 'Product price', 'Manufacture Date', 'Expiry Date', 'Remaining Stock',
                      'Sold Count', 'Total Sold Amount']

        csv_file_path = os.path.join(csv_folder_path, f'report_{user_id}.csv')

        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in match_item:
                product = match_product[item.product_id]['product']
                sold_count = match_product[item.product_id]['sold_count']
                total_amount = sold_count * product.price

                writer.writerow({
                    'Product Id': product.id,
                    'Product Name': product.name,
                    'Product price': product.price,
                    'Manufacture Date': product.manufacture_date,
                    'Expiry Date': product.expiry_date,
                    'Remaining Stock': product.stock,
                    'Sold Count': sold_count,
                    'Total Sold Amount': total_amount
                })
        return {'csv_file_path': csv_file_path}

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = "freshcart_23@email.com"
SENDER_PASSWORD = ""

WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAAAX2sFUCs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=k1GxBWpqZU--LX1OQszQ3kNxPhFIyi9lFtTZ3BXZpuc"
@celery.task
def send_reminder():
    url = WEBHOOK_URL
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

    users_without_shopping = User.query.join(User.roles).filter(and_(Role.name == 'user', ~User.id.in_(db.session.query(BoughtProducts.user_id).filter(BoughtProducts.bought_date >= twenty_four_hours_ago)))).all()

    if not users_without_shopping:
        return "No reminders sent. All users have bought products recently."

    for user in users_without_shopping:
        reminder_message = f"Dear {user.username}, you haven't bought any product in the last 24 hours. Please check the available products."

        send_gspace_message(reminder_message)

    return f"Reminders sent to {len(users_without_shopping)} users who haven't bought in the last 24 hours."

def send_gspace_message(message):
    url = WEBHOOK_URL
    bot_message = {'text': message}
    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    print(response)

from sqlalchemy import extract

def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))
    if attachment_file:
        with open(attachment_file, "rb") as attachment:    
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_file}",
        )
        msg.attach(part)
    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

def generate_monthly_progress_report(user_id):    
    current_month = datetime.now().month
    user = User.query.filter_by(id=user_id).first()
    
    shopping_data = BoughtProducts.query.filter(extract('month', BoughtProducts.bought_date) == current_month,BoughtProducts.user_id == user.id).all()
    item_ids = [order.product_id for order in shopping_data]
    items_bought = product_model.query.filter(product_model.id.in_(item_ids)).all()
    product_names = {}
    for order in shopping_data:
        product = product_model.query.filter_by(id=order.product_id).first()
        product_names[order.product_id] = order.product_name
    username=user.username

    with open('monthly_report.html', 'r') as template_file:
        template_content = template_file.read()
    template = Template(template_content)

    report_html = template.render(shopping_data=shopping_data, items_bought=items_bought, username=username,product_names=product_names)

    return report_html

@celery.task()
def send_mail_message():
    users_general = User.query.join(User.roles).filter(Role.name == 'user').all()

    for user in users_general:
        report_html = generate_monthly_progress_report(user.id)
        recipient_email = user.email
        recipient_username = user.username if user.username else 'Recipient'
        
        subject = 'Monthly Shopping Report On freshcart'
        message = report_html.replace('Recipient', recipient_username)

        send_email(to_address=recipient_email, subject=subject, message=message, content='html', attachment_file='monthly_report.html')
    return "Monthly report emails sent"