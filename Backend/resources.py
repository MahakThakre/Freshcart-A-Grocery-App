from flask_restful import Api, Resource, fields, marshal,marshal_with,reqparse
from flask_security import auth_required, current_user,login_required,roles_required
from flask_security.utils import hash_password
from security import user_datastore
from models import db, User as user_model,Role, Request, Category as category_model, Category_Requests, Product as product_model,Category_Update_Request,Category_Delete_Request, Cart as cart_model , BoughtProducts as buy_model
from flask import abort, request,jsonify,redirect,url_for

from time import perf_counter_ns
from flask import abort, request,jsonify,redirect,url_for
from flask_caching import Cache
import redis
import base64,os

redis_url = "redis://localhost:6379/3"
redis_client = redis.from_url(redis_url)
cache = Cache(config={"CACHE_TYPE": "redis", "CACHE_REDIS_CLIENT": redis_client})

api = Api(prefix="/api")

user_resource_fields = {
    "id": fields.Integer(),
    "username": fields.String,
    "password": fields.String,
    "email": fields.String,
    "roles": fields.List(fields.String),
}

requests_resource_fields ={
    "request_id": fields.Integer(),
    "approval": fields.Integer(),
    "requesters_name":fields.String
}
cat_requests_resource_fields ={
    "req_id": fields.Integer(),
    "requesters_id": fields.Integer(),
    "approval": fields.Integer(),
    "requesters_name":fields.String,
    "category_name":fields.String
}
cat_update_requests_resource_fields ={
    "req_id": fields.Integer(),
    "requesters_id": fields.Integer(),
    "approval": fields.Integer(),
    "requesters_name":fields.String,
    "category_name":fields.String,
    "category_id":fields.Integer(),
    "category_old_name":fields.String,
}
cat_delete_requests_resource_fields ={
    "req_id": fields.Integer(),
    "requesters_id": fields.Integer(),
    "approval": fields.Integer(),
    "requesters_name":fields.String,
    "category_name":fields.String,
    "category_id":fields.Integer(),
}
cat_resource_fields ={
    "id":fields.Integer(),
    "name":fields.String
}
products_resource_fields ={
    "id" : fields.Integer(),
    "name":fields.String,
    "manufacture_date" :fields.String,
    "expiry_date":fields.String,
    "price":fields.Integer(),
    "rate_per_unit":fields.String(),
    "stock": fields.Integer(),
    "category_id": fields.Integer(),
    "category":fields.Nested(cat_resource_fields),
    "user_id":fields.Integer(),
}
cart_resource_fields ={
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "product_id": fields.Integer(),
    "product_count": fields.Integer(),
    "product_name": fields.String,
    "product_price": fields.Integer(),
}
buy_product_resource_fields ={
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "product_id": fields.Integer(),
    "product_count": fields.Integer(),
    "bought_date":fields.String,
    "product_name": fields.String,
    "amount":fields.Integer(),
    "category_name":fields.String,
}
wishlist_resource_fields = {
    "id": fields.Integer(),
    "user_id": fields.Integer(),
    "product_id": fields.Integer(),
    "product": fields.Nested(products_resource_fields),  # Include product details
}

class User(Resource):
    def get(self, email):
        user = user_model.query.filter_by(email=email).first()
        if not user:
            abort(404, "User not found")
        user_data = marshal(user, user_resource_fields)
        return user_data 
    
    def post(self):
        email = request.json.get('email')
        password = request.json.get('password')
        username = request.json.get('username')

        if email and password and username:
            user = user_model.query.filter_by(email=email).first()
            if user:
                abort(400, "User with email already exists")
            else:
                user = user_model(email=email)
                user.password = password
                user = user_datastore.create_user(username=username, email=email, password=hash_password(password))
                db.session.commit()
                if '/user_signup' in request.path:
                    user_role= user_datastore.find_role('user')
                    user_datastore.add_role_to_user(user, user_role)
                    db.session.commit()
                    return {"message": "Signed up successfully!"},200

                elif '/manager_signup' in request.path:
                    user_id=user.id
                    new_request=Request(request_id=user_id, approval=False,requesters_name=username)
                    db.session.add(new_request)
                    db.session.commit()
                    return {"message": "Request sent successfully!"},200
        else:
            abort(400, "Email, password, and username are required")

class Admin_Dashboard(Resource):
    @cache.cached(timeout=60, key_prefix="admin_dashboard")
    def get(self,email):
        if not current_user.has_role('admin'):
            print(current_user.roles)
            abort(403, "You are not authorized to access this resource.")
        start=perf_counter_ns()
        user=user_model.query.filter_by(email=email).first()
        if not user:
            abort(404, "User not found. ")
        
        requests=Request.query.all()
        requests_2=[]
        if requests:
            for request in requests:
                request_data=marshal(request,requests_resource_fields)
                requests_2.append(request_data)
        stop = perf_counter_ns()
        print(stop-start)
        return requests_2
    
    def delete(self, request_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to delete requests.")

        request_to_delete = Request.query.filter_by(request_id=request_id).first()
        if not request_to_delete:
            abort(404, "Request not found.")

        db.session.delete(request_to_delete)
        db.session.commit()
        cache.delete('admin_dashboard')

        requests = Request.query.all()
        requests_2 = []
        if requests:
            for request in requests:
                request_data = marshal(request, requests_resource_fields)
                requests_2.append(request_data)
        return requests_2
    
    def post(self, request_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to approve requests.")

        request_to_approve = Request.query.filter_by(request_id=request_id).first()
        if not request_to_approve:
            abort(404, "Request not found.")

        request_to_approve.approval = True
        user = user_model.query.filter_by(id=request_id).first()
        manager = user_datastore.find_role('manager')
        user_datastore.add_role_to_user(user, manager)
        db.session.delete(request_to_approve)
        db.session.commit()
        cache.delete('admin_dashboard')

        requests = Request.query.all()
        requests_2 = []
        if requests:
            for request in requests:
                request_data = marshal(request, requests_resource_fields)
                requests_2.append(request_data)
        return requests_2
    


class Category_Approval(Resource):
    def get(self):
        cat_requests=Category_Requests.query.all()
        cat_requests_2=[]
        if cat_requests:
            for request in cat_requests:
                request_data=marshal(request,cat_requests_resource_fields)
                cat_requests_2.append(request_data)
            return cat_requests_2
    
    def post(self, request_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to approve requests.")

        request_to_approve = Category_Requests.query.filter_by(req_id=request_id).first()
        if not request_to_approve:
            abort(404, "Request not found.")
        request_to_approve.approval = True
        new_category=category_model(name=request_to_approve.category_name)
        db.session.add(new_category)
        db.session.commit()
        db.session.delete(request_to_approve)
        db.session.commit()
        cache.delete('admin_dashboard')

        categories = category_model.query.all()
        categories_data = [{"id": category.id, "name": category.name} for category in categories]
        requests=Category_Requests.query.all()
        requests_2=[]
        if requests:
            for request in requests:
                request_data=marshal(request,cat_requests_resource_fields)
                requests_2.append(request_data)
        
            return {"message": "Request Approved successfully!", "categories": categories_data, "requests": requests_2}
        return {"message": "Request Approved successfully!", "categories": categories_data, "requests": requests_2}
    
    def delete(self, request_id):
        request_to_decline = Category_Requests.query.filter_by(req_id=request_id).first()

        if not request_to_decline:
            abort(404, "Request not found.")

        db.session.delete(request_to_decline)
        db.session.commit()

        requests = Category_Requests.query.all()
        requests_2 = []
        if requests:
            for request in requests:
                request_data = marshal(request, cat_requests_resource_fields)
                requests_2.append(request_data)

        return {"message": "Request Declined successfully!", "requests": requests_2}

class Category(Resource):
    def put(self,category_id):
        category=category_model.query.filter_by(id=category_id).first()
        user=user_model.query.filter_by(email=current_user.email).first()
        category_name = request.form.get("category_name")
        if not category_name:
            abort(400, "Category name is required.")
        if category_model.query.filter(category_model.name == category_name).first():
            abort(400, "Category name already exists. Choose a different name.")

        if current_user.has_role('admin'):
            category.name=category_name
            db.session.commit()
            cache.delete('admin_dashboard')
        elif current_user.has_role('manager'):
            new_category_update_request=Category_Update_Request(requesters_id=user.id,approval=0,requesters_name=user.username, category_name=category_name,category_id=category_id, category_old_name=category.name)
            db.session.add(new_category_update_request)
            db.session.commit()
            cache.delete('category')
        else:
            abort(403,'You are not authorized')
        categories = category_model.query.all()
        categories_data = [{"id": category.id, "name": category.name} for category in categories]

        return {"message": "Category updated successfully!", "categories": categories_data}
    
    def get(self):
        start=perf_counter_ns()
        categories = category_model.query.all()
        categories_data = [{"id": category.id, "name": category.name} for category in categories]
        stop = perf_counter_ns()
        print(stop-start)
        return categories_data
    
    def post(self):
        user=user_model.query.filter_by(email=current_user.email).first()
        category_name = request.form.get("category_name")
        if not category_name:
            abort(400, "Category name is required.")
        if category_model.query.filter(category_model.name == category_name).first():
            abort(400, "Category name already exists. Choose a different name.")

        if current_user.has_role('admin'):
            new_category = category_model(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            cache.delete('admin_dashboard')
        elif current_user.has_role('manager'):
            new_category_request=Category_Requests(requesters_id=user.id,approval=0,requesters_name=user.username, category_name=category_name)
            db.session.add(new_category_request)
            db.session.commit()
        else:
            abort(403,'You are not authorized')
        categories = category_model.query.all()
        categories_data = [{"id": category.id, "name": category.name} for category in categories]

        return {"message": "Category added successfully!", "categories": categories_data}

    def delete(self, category_id):
        category = category_model.query.filter_by(id=category_id).first()
        user = user_model.query.filter_by(email=current_user.email).first()

        if category is None:
            abort(404, 'Category not found')

        if current_user.has_role('admin'):
            if category.products:
                return {"error": "Products are present inside this category. Deletion not allowed."}, 400

            db.session.delete(category)
            db.session.commit()
            categories = category_model.query.all()
            categories_data = [{"id": category.id, "name": category.name} for category in categories]

            return {"message": "Category deleted successfully!", "categories": categories_data}
        elif current_user.has_role('manager'):
            new_category_delete_request=Category_Delete_Request(requesters_id=user.id,approval=0,requesters_name=user.username, category_name=category.name,category_id=category_id)
            db.session.add(new_category_delete_request)
            db.session.commit()
            categories = category_model.query.all()
            categories_data = [{"id": category.id, "name": category.name} for category in categories]

            return {"message": "Category delete request successfully!", "categories": categories_data}
        else:
            abort(403,'You are not authorized')

class Category_Delete_Approval(Resource):
    def get(self):
        cat_requests=Category_Delete_Request.query.all()
        cat_requests_2=[]
        if cat_requests:
            for request in cat_requests:
                request_data=marshal(request,cat_delete_requests_resource_fields)
                cat_requests_2.append(request_data)
            return cat_requests_2
    
    def delete(self, category_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to approve requests.")
        category = category_model.query.filter_by(id=category_id).first()

        if category.products:
            return {"error": "Products are present inside this category. Deletion not allowed."}, 400
        request_to_approve = Category_Delete_Request.query.filter_by(category_id=category_id).first()
        if not request_to_approve:
            abort(404, "Request not found.")

        request_to_approve.approval = True
        category=category_model.query.filter_by(id=category_id).first()
        db.session.delete(category)
        db.session.commit()
        db.session.delete(request_to_approve)
        db.session.commit()

        categories = category_model.query.all()
        categories_data = [{"id": category.id, "name": category.name} for category in categories]
        requests=Category_Delete_Request.query.all()
        requests_2=[]
        if requests:
            for request in requests:
                request_data=marshal(request,cat_delete_requests_resource_fields)
                requests_2.append(request_data)
        
            return {"message": "Request Approved successfully!", "categories": categories_data, "requests": requests_2}
        return {"message": "Request Approved successfully!", "categories": categories_data, "requests": requests_2}

class Category_Update_Approval(Resource):
    def get(self):
        cat_requests=Category_Update_Request.query.all()
        cat_requests_2=[]
        if cat_requests:
            for request in cat_requests:
                request_data=marshal(request,cat_update_requests_resource_fields)
                cat_requests_2.append(request_data)
            return cat_requests_2
    
    def put(self, category_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to approve requests.")

        request_to_approve = Category_Update_Request.query.filter_by(category_id=category_id).first()
        if not request_to_approve:
            abort(404, "Request not found.")

        request_to_approve.approval = True
        category=category_model.query.filter_by(id=category_id).first()
        category.name=request_to_approve.category_name
        db.session.commit()
        db.session.delete(request_to_approve)
        db.session.commit()

        categories = category_model.query.all()
        categories_data = [{"id": category.id, "name": category.name} for category in categories]
        requests=Category_Update_Request.query.all()
        requests_2=[]
        if requests:
            for request in requests:
                request_data=marshal(request,cat_update_requests_resource_fields)
                requests_2.append(request_data)
        
            return {"message": "Request Approved successfully!", "categories": categories_data, "requests": requests_2}
        return {"message": "Request Approved successfully!", "categories": categories_data, "requests": requests_2}

    def delete(self, category_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to decline requests.")

        request_to_decline = Category_Update_Request.query.filter_by(category_id=category_id).first()
        if not request_to_decline:
            abort(404, "Request not found.")

        db.session.delete(request_to_decline)
        db.session.commit()

        requests = Category_Update_Request.query.all()
        requests_2 = []
        if requests:
            for request in requests:
                request_data = marshal(request, cat_update_requests_resource_fields)
                requests_2.append(request_data)

        return {"message": "Request Declined successfully!", "requests": requests_2}


class Products(Resource):
    def get(self, category_id):
        if current_user.has_role('admin') or current_user.has_role('manager'):
            category = category_model.query.filter_by(id=category_id).first()
            products = product_model.query.filter_by(category_id=category_id).all()
            m_products = []

            if products:
                for product in products:
                    manager_name = user_model.query.filter_by(id=product.user_id).first().username
                    product = marshal(product, products_resource_fields)
                    product['manager_name'] = manager_name
                    product['category'] = marshal(category, cat_resource_fields)
                    m_products.append(product)
        
            return m_products
        else:
            abort(403, 'You are not authorized')


    def post(self, category_id):
        if current_user.has_role('admin') or current_user.has_role('manager'):
            product_name = request.form.get('product_name')
            manufacture_date = request.form.get('manufacture_date')
            expiry_date = request.form.get('expiry_date') 
            price = request.form.get('price')
            rate_per_unit = request.form.get('rate_per_unit')
            stock = request.form.get("stock")
            if not manufacture_date:
                manufacture_date = None
            if not expiry_date:
                expiry_date = None
            new_product=product_model(name=product_name, manufacture_date=manufacture_date,expiry_date=expiry_date,price=price,rate_per_unit=rate_per_unit,stock=stock, category_id=category_id,user_id=current_user.id)
            db.session.add(new_product)
            db.session.commit()
            category=category_model.query.filter_by(id=category_id).first()
            products=product_model.query.filter_by(category_id=category_id).all()
            m_products=[]
            if products:
                for product in products:
                    product=marshal(product,products_resource_fields)
                    m_products.append(product)
                    product['category'] = marshal(category, cat_resource_fields)
            return m_products
        else:
            abort(403,'You are not authorized')

class SingleProduct(Resource):
    def get(self,category_id,product_id):
            product=product_model.query.filter_by(category_id=category_id,id=product_id).first()
            category=category_model.query.filter_by(id=category_id).first()
            product=marshal(product,products_resource_fields)
            product['category'] = marshal(category, cat_resource_fields)
            return product
    
    def delete(self,product_id):
        product=product_model.query.filter_by(id=product_id).first()
        if current_user.has_role('manager') and current_user.id == product.user_id:
            
            db.session.delete(product)
            db.session.commit()
        else:
            abort(403,'You are not authorized')
    
    def put(self,product_id):
        product=product_model.query.filter_by(id=product_id).first()
        if current_user.has_role('manager') and current_user.id == product.user_id:
            category=category_model.query.filter_by(id=product.category_id).first()
            product_name = request.form.get('product_name')
            manufacture_date = request.form.get('manufacture_date')
            expiry_date = request.form.get('expiry_date') 
            price = request.form.get('price')
            rate_per_unit = request.form.get('rate_per_unit')
            stock = request.form.get("stock")
            if not manufacture_date:
                manufacture_date = None
            if not expiry_date:
                expiry_date = None
            product.name=product_name
            product.manufacture_date=manufacture_date
            product.expiry_date=expiry_date
            product.price=price
            product.rate_per_unit=rate_per_unit
            product.stock=stock
            db.session.commit()
            
            product=marshal(product,products_resource_fields)
            product['category'] = marshal(category, cat_resource_fields)
            return product
        else:
            abort(403,'You are not authorized')

class UserDashboard(Resource):
    @cache.cached(timeout=60)
    def get(self):
        user = user_model.query.filter_by(email=current_user.email).first()
        start = perf_counter_ns()
        categories = category_model.query.all()
        category_list = []
        if user and categories:
            for category in categories:
                products = product_model.query.filter_by(category_id=category.id).all()
                prod_list = []
                for product in products:
                    manager_name = user_model.query.filter_by(id=product.user_id).first().username
                    prod_data = marshal(product, products_resource_fields)
                    prod_data['manager_name'] = manager_name
                    prod_list.append(prod_data)
                category_data = {"id": category.id, "name": category.name, "products": prod_list}
                category_list.append(category_data)
            stop = perf_counter_ns()
            print(stop - start)
            return category_list
        else:
            abort(404, "No categories found")


class BuyProduct(Resource):
    def get(self):
        user=user_model.query.filter_by(email=current_user.email).first()
        bought_items = buy_model.query.filter_by(user_id=user.id).all()
        bought_data = []
        for item in bought_items:
            bought_data.append(marshal(item, buy_product_resource_fields))
        return {"bucket": bought_data}

    def post(self,product_id):
        product_count=int(request.form.get("product_count"))
        user=user_model.query.filter_by(email=current_user.email).first()
        item_bought=product_model.query.filter_by(id=product_id).first()
        total_cost=item_bought.price*product_count
        new_purchase=buy_model(user_id=user.id,product_id=product_id,product_name=item_bought.name,product_count=product_count,amount=total_cost,category_name=item_bought.category.name)
        db.session.add(new_purchase)
        db.session.commit()
        item_bought.stock-=product_count
        db.session.commit()

class BuyCart(Resource):
    def post(self):
        cart=cart_model.query.filter_by(user_id=current_user.id).all()
        for item in cart:
            item_bought=product_model.query.filter_by(id=item.product_id).first()
            if item_bought.stock<=0:
                continue
            total_cost=item_bought.price*item.product_count
            new_purchase=buy_model(user_id=current_user.id, product_id=item.product_id,product_name=item.product_name,product_count=item.product_count,amount=total_cost,category_name=item_bought.category.name)
            db.session.add(new_purchase)
            db.session.commit()
            item_bought.stock-=item.product_count
            db.session.commit()
            db.session.delete(item)
            db.session.commit()


class Cart(Resource):
    def get(self):
        user = user_model.query.filter_by(email=current_user.email).first()
        cart_items = cart_model.query.filter_by(user_id=user.id).all()
        cart_data = []
        cart_price=0
        for item in cart_items:
            product=product_model.query.filter_by(id=item.product_id).first()
            if product.stock < item.product_count:
                continue
            cart_data.append(marshal(item, cart_resource_fields)) 
            amount=item.product_count*product.price
            cart_price+=amount
        return {"cart": cart_data,"cart_price":cart_price}

    def post(self,product_id):
        product_count=int(request.form.get("product_count"))
        user=user_model.query.filter_by(email=current_user.email).first()
        product=product_model.query.filter_by(id=product_id).first()
        cart_item=cart_model.query.filter_by(product_id=product_id,user_id=current_user.id).first()
        if cart_item:
            cart_item.product_count+=product_count
            count=cart_item.product_count+product_count
            if count > product.stock:
                return {'message':"We don't have enough stock available. Please enter Less quantity"}
            db.session.commit()
            return {'message':"Added successfully"}
        else:
            new_cart_entry=cart_model(user_id=user.id,product_id=product_id,product_price=product.price,product_count=product_count,product_name=product.name)
            db.session.add(new_cart_entry)
            db.session.commit()
            return {'message':"Added successfully"}


    def delete(self, product_id):
        cart_product = cart_model.query.filter_by(product_id=product_id, user_id=current_user.id).first()

        if cart_product:
            db.session.delete(cart_product)
            db.session.commit()
        else:
            print(f"Product with ID {product_id} not found in the user's cart.")
    
    def put(self, product_id):
        try:
            data = request.get_json(force=True)
            new_product_count = data['product_count']

            user = user_model.query.filter_by(email=current_user.email).first()
            cart_item = cart_model.query.filter_by(product_id=product_id, user_id=current_user.id).first()

            if cart_item:
                product = product_model.query.filter_by(id=product_id).first()

                if new_product_count > product.stock:
                    return {'message': "We don't have enough stock available. Please enter a lower quantity."}

                cart_item.product_count = new_product_count
                db.session.commit()
                return {'message': "Product count updated successfully"}
            else:
                return {'message': f"Product with ID {product_id} not found in the user's cart."}, 404

        except Exception as e:
            return {'message': f"Error processing the request: {str(e)}"}, 500
        
class Search(Resource):
    def post(self):
        form_data = request.form

        stock = form_data.get('stock')
        category = form_data.get('category')
        product_name = form_data.get('product_name')
        manufacture_date = form_data.get('manufacture_date')
        expiry_date = form_data.get('expiry_date')
        min_price = form_data.get('min_price')
        max_price = form_data.get('max_price')
        query = product_model.query
        if stock:
            query = query.filter(product_model.stock >= 0)  
        if category and category != 'All':
            query = query.join(category_model).filter(category_model.id == int(category))
        if product_name:
            query = query.filter(product_model.name.ilike(f"%{product_name}%"))
        if manufacture_date:
            query = query.filter(product_model.manufacture_date == manufacture_date)
        if expiry_date:
            query = query.filter(product_model.expiry_date == expiry_date)
        if min_price:
            query = query.filter(product_model.price >= int(min_price))
        if max_price:
            query = query.filter(product_model.price <= int(max_price))
        products = query.all()

        if not products:
            return {"message": "No products found based on the search criteria."}

        result = [marshal(product, products_resource_fields) for product in products]
        return result
    

class Category_Delete_Decline(Resource):
    def delete(self, category_id):
        if not current_user.has_role('admin'):
            abort(403, "You are not authorized to decline requests.")
            
        request_to_decline = Category_Delete_Request.query.filter_by(category_id=category_id).first()

        if not request_to_decline:
            abort(404, "Request not found.")

        db.session.delete(request_to_decline)
        db.session.commit()

        requests = Category_Delete_Request.query.all()
        requests_2 = []
        if requests:
            for request in requests:
                request_data = marshal(request, cat_delete_requests_resource_fields)
                requests_2.append(request_data)

        return {"message": "Request Declined successfully!", "requests": requests_2}



api.add_resource(User, '/manager_signup','/user_signup','/getUserData/<string:email>')
api.add_resource(Admin_Dashboard,'/admin_dashboard/<string:email>','/approveRequest/<int:request_id>','/declineRequest/<int:request_id>')
api.add_resource(Category,'/addCategory','/getCategory','/editCategory/<int:category_id>','/deleteCategory/<int:category_id>')
api.add_resource(Category_Approval,'/categoryRequests','/approveCatRequest/<int:request_id>','/declineCatRequest/<int:request_id>')
api.add_resource(Category_Delete_Decline, '/declineCatDeleteRequest/<int:category_id>', '/categoryDeleteRequests')
api.add_resource(Products,'/addProduct/<int:category_id>','/getProducts/<int:category_id>')
api.add_resource(SingleProduct,'/getProduct/<int:category_id>/<int:product_id>','/deleteProduct/<int:product_id>','/editProduct/<int:product_id>')
api.add_resource(Category_Update_Approval,'/approveCatUpdateRequest/<int:category_id>','/categoryUpdateRequests','/declineCatUpdateRequest/<int:category_id>')
api.add_resource(Category_Delete_Approval,'/approveCatDeleteRequest/<int:category_id>','/categoryDeleteRequests')
api.add_resource(UserDashboard,'/userDashboard')
api.add_resource(BuyProduct,'/buyProduct/<int:product_id>','/bought')
api.add_resource(Cart,'/cartProduct/<int:product_id>','/cart/<int:product_id>','/cart')
api.add_resource(BuyCart,'/buyCart')
api.add_resource(Search, '/search')