import re
import datetime
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from email_validator import validate_email, EmailNotValidError


class BaseView(MethodView):
    """Base view method"""
    def validate_json(self):
        """Returns false if request is json"""
        if request.get_json(silent=True) is None:
            response = {'message':'The Request should be JSON format'}
            return jsonify(response), 400
        return False

    def check_email(self, email):
        try:
            validator_response = validate_email(email)
            email = validator_response["email"]
            return False
        except EmailNotValidError as error:
            response = {'message': str(error)}
            return jsonify(response), 400

    def validate_null(self, **kwargs):
        """Returns a list with null fields"""
        messages = []
        for key in kwargs:
            if kwargs[key] is None:
                message = 'Please enter your {}'.format(key)
                messages.append(message)
            if kwargs[key] is not None:
                strip_text = re.sub(r'\s+', '', kwargs[key])
                if not strip_text:
                    message = 'Please enter your {}'.format(key)
                    messages.append(message)
        if messages:
            response = {'message': messages}
            return jsonify(response), 400
        return False

    def generate_token(self, user, username, expires=datetime.timedelta(hours=1)):
        """Return access token and response to user"""
        response = {
            'message': 'Login successfull. Welcome {}'.format(username),
            'access_token': create_access_token(identity=user, expires_delta=expires)
        }
        return jsonify(response), 200

    def remove_extra_spaces(self, user_input):
        """Maximum number of spaces between words should be one"""
        strip_text = user_input.strip()
        return re.sub(r'\s+', ' ', strip_text)