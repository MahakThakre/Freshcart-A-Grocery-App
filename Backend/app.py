from flask import Flask, render_template, send_file
from flask_security import auth_required
from models import db, Role, User
from resources import api, cache
from security import user_datastore, sec
from flask_security.utils import hash_password
from flask_cors import CORS
import worker
from celery import Celery
from celery.schedules import crontab
from tasks import send_mail_message , send_reminder, export_manager_csv


app=Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["SECRET_KEY"]='MAHAK'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///freshcart.db'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_ROLE_REQUIRED'] = True
app.config['CELERY_BROKER_URL']="redis://localhost:6379/1"
app.config['CELERY_RESULT_BACKEND']="redis://localhost:6379/2"
app.config['CELERY_TIMEZONE'] = 'Asia/Kolkata'
cache.init_app(app)
api.init_app(app)
db.init_app(app)

sec.init_app(app, user_datastore)
app.app_context().push()

celery = worker.celery
celery.conf.update(
    broker_url= app.config['CELERY_BROKER_URL'],
result_backend = app.config['CELERY_RESULT_BACKEND'],
timezone=app.config['CELERY_TIMEZONE']
)

celery.Task = worker.ContextTask
app.app_context().push()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=21, day_of_month='25'),
        send_mail_message.s(),
        name='FreshCart'
    )

    sender.add_periodic_task(
        crontab(hour=19, minute=21),
        send_reminder.s(),
        name="Didn't Shop Today!"
    )

@app.route('/export_manager_csv/<int:user_id>', methods=['POST']) 
@auth_required()
def export_manager_product_csv(user_id):
    task = export_manager_csv.delay(user_id=user_id)
    task_result = task.get()
    csv_file_path = task_result['csv_file_path']
    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = Role.query.filter_by(name='admin').first()
        manager = Role.query.filter_by(name='manager').first()
        user = Role.query.filter_by(name='user').first()
        if not admin:
            admin = Role(name='admin', description='Administrator Role')
            db.session.add(admin)
        if not manager:
            manager = Role(name='manager', description='Manager Role')
            db.session.add(manager)
        if not user:
            user= Role(name='user', description='General User ')
            db.session.add(user)
        db.session.commit()
        users=User.query.all()
        if not users:
            admin_user=User.query.filter_by(email="admin@gmail.com").first()    
            if not admin_user:
                admin_user = User(email='admin@gmail.com', username='admin', password=hash_password('admin'))
                admin_user.active = True  
                admin_user.fs_uniquifier = 'unique_value'
                admin_user.roles.append(admin)
                db.session.add(admin_user)
                db.session.commit()
        app.run(debug=True)