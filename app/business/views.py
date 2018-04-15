"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from app.models import Business
from app.baseview import BaseView
from app.auth.views import users

biz = Blueprint('biz', __name__, url_prefix='/api/v1/businesses')
store = []


class BusinessManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_required
    def post(self):
        if not self.validate_json():
            data = request.get_json()
            name = data.get('name')
            description = data.get('description')
            category = data.get('category')
            location = data.get('location')
            current_user = get_jwt_identity()
            data_ = dict(name=name, description=description, category=category, location=location)
            if not self.validate_null(**data_):
                user_ = [user for user in users if current_user == user.email]
                if user_:
                    data = self.remove_extra_spaces(**data_)
                    business = Business(**data, created_by=current_user)
                    store.append(business)
                    response = {'message': 'Business with name {} created'.format(name)}
                    return jsonify(response), 201
                response = {'message': 'Please login to continue'}
                return jsonify(response), 401
            return self.validate_null(**data_)
        return self.validate_json()


business_view = BusinessManipulation.as_view('businesses')
biz.add_url_rule('', defaults={'business_id':None}, view_func=business_view, methods=['GET',])
biz.add_url_rule('', view_func=business_view, methods=['POST',])
biz.add_url_rule('/<int:business_id>', view_func=business_view, methods=['GET', 'PUT', 'DELETE'])
