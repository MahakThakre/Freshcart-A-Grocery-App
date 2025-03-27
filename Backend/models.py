from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime
import pytz


db = SQLAlchemy()

IST = pytz.timezone('Asia/Kolkata')

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(),db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(),db.ForeignKey('role.id')))
    
class User(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True)
    email=db.Column(db.String, unique=True)
    username=db.Column(db.String)
    password=db.Column(db.String(255))
    active=db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

class Role(db.Model, RoleMixin):
    __tablename__='role'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Request(db.Model):
    __tablename__ = 'requests'
    r_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    request_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approval = db.Column(db.Boolean)
    requesters_name=db.Column(db.String(25), unique=True, nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Category_Requests(db.Model):
    __tablename__= 'category_requests'
    req_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    requesters_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approval = db.Column(db.Boolean)
    requesters_name=db.Column(db.String(25), nullable=False)
    category_name=db.Column(db.String(25), unique=True, nullable=False)

class Category_Update_Request(db.Model):
    __tablename__= 'category_update_request'
    req_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    requesters_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approval = db.Column(db.Boolean)
    requesters_name=db.Column(db.String(25), nullable=False)
    category_name=db.Column(db.String(25), unique=True, nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category_old_name=db.Column(db.String(25), nullable=False)

class Category_Delete_Request(db.Model):
    __tablename__= 'category_delete_request'
    req_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    requesters_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approval = db.Column(db.Boolean)
    requesters_name=db.Column(db.String(25), nullable=False)
    category_name=db.Column(db.String(25), unique=True, nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    manufacture_date = db.Column(db.String(20), default=None, nullable=True)
    expiry_date = db.Column(db.String(20), default=None, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    rate_per_unit = db.Column(db.String(20), nullable=False) 
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False) 
    product_count = db.Column(db.Integer, nullable=False)
    product_name=db.Column(db.String(100), nullable=False)

class BoughtProducts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    product_count = db.Column(db.Integer, nullable=False)
    product_name=db.Column(db.String(100), nullable=False)
    bought_date=db.Column(db.DateTime, nullable=False, default=datetime.now(IST))
    amount= db.Column(db.Integer, nullable=False)
    category_name = db.Column(db.String(100), nullable=False)