"""Contains views to register, login reset password and logout user"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional
from flask_bcrypt import Bcrypt
from app.models import Business
from app.baseview import BaseView
from app.auth.views import users

biz = Blueprint('biz', __name__, url_prefix='/api/v1/businesses')
rev = Blueprint('rev', __name__, url_prefix='/api/v1/businesses/<int:business_id>/reviews')
store = []


class BusinessManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_required
    def post(self):
        if not self.validate_json():
            data = request.get_json()
            name = data.get('name')
            category = data.get('category')
            location = data.get('location')
            current_user = get_jwt_identity()
            data_ = dict(name=name, category=category, location=location)
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

    @jwt_required
    def put(self, business_id):
        """update a single business"""
        if not self.validate_json():
            data = request.get_json()
            name = data.get('name')
            category = data.get('category')
            location = data.get('location')
            current_user = get_jwt_identity()
            data_ = dict(name=name, category=category, location=location)
            if not self.validate_null(**data_):
                for business in store:
                    if business_id == business.id:
                        if current_user == business.created_by:
                            data = self.remove_extra_spaces(**data_)
                            business.name = data['name']
                            business.category = data['category']
                            business.location = data['location']
                            response = {'message': 'Business updated successfully'}
                            return jsonify(response), 200
                        response = {'message': 'The operation is forbidden for this business'}
                        return jsonify(response), 403
                response = {'message': 'The business {} is not available'.format(business_id)}
                return jsonify(response), 404
            return self.validate_null(**data_)
        return self.validate_json()

    @jwt_required
    def delete(self, business_id):
        if not self.validate_json():
            data = request.get_json()
            password = data.get('password')
            current_user = get_jwt_identity()
            data_ = dict(password=password)
            if not self.validate_null(**data_):
                user_ = [user for user in users if current_user == user.email]
                if user_:
                    user = user_[0]
                    if Bcrypt().check_password_hash(user.password, password):
                        business_ = [business for business in store if business_id == business.id]
                        if business_:
                            business = business_[0]
                            if current_user == business.created_by:
                                index = store.index(business)
                                del store[index]
                                response = {'message': 'Business {} deleted'.format(business_id)}
                                return jsonify(response), 200
                            response = {'message': 'The operation is forbidden for this business'}
                            return jsonify(response), 403
                        response = {'message': 'The business {} is not available'.format(business_id)}
                        return jsonify(response), 404
                    response = {'message': 'Enter correct password to delete'}
                    return jsonify(response), 401
                response = {'message': 'Please login to continue'}
                return jsonify(response), 401
            return self.validate_null(**data_)
        return self.validate_json()

    @jwt_optional
    def get(self, business_id):
        """return a list of all businesses else a single business"""
        if business_id is None:
            business_ = [business.serialize() for business in store]
            if business_:
                response = {'message': 'The following businesss are registered',
                            'businesses': business_}
                return jsonify(response), 200
            response = {'message': 'There are no businesses registered currently'}
            return jsonify(response), 404
        else:
            business_ = [business.serialize() for business in store if business_id == business.id]
            if business_:
                response = {'businesses': business_,}
                return jsonify(response), 200
            response = {'message': 'The business {} is not available'.format(business_id)}
            return jsonify(response), 404


class ReviewManipulation(BaseView):
    """Method to manipulate business endpoints"""
    @jwt_required
    def post(self, business_id):
        """Endpoint to save the data to the database"""
        if not self.validate_json():
            data = request.get_json()
            review = data.get('review')
            current_user = get_jwt_identity()
            data_ = dict(review=review)
            if not self.validate_null(**data_):
                user_ = [user for user in users if current_user == user.email]
                if user_:
                    data = self.remove_extra_spaces(**data_)
                    for business in store:
                        if business_id == business.id:
                            if current_user == business.created_by:
                                response = {'message': 'The operation is forbidden for own business'}
                                return jsonify(response), 403
                            business.reviews.append(data['review'])
                            response = {'message': 'Review for business {} created'.format(business_id)}
                            return jsonify(response), 201
                        response = {'message': 'The business {} is not available'.format(business_id)}
                    return jsonify(response), 404
                response = {'message': 'Please login to continue'}
                return jsonify(response), 401
            return self.validate_null(**data_)
        return self.validate_json()
                        


business_view = BusinessManipulation.as_view('businesses')
biz.add_url_rule('', defaults={'business_id':None}, view_func=business_view, methods=['GET',])
biz.add_url_rule('', view_func=business_view, methods=['POST',])
biz.add_url_rule('/<int:business_id>', view_func=business_view, methods=['GET', 'PUT', 'DELETE',])
biz.add_url_rule('/<int:business_id>/reviews', view_func=business_view, methods=['GET'])

review_view = ReviewManipulation.as_view('reviews')
rev.add_url_rule('', view_func=review_view, methods=['POST'])
