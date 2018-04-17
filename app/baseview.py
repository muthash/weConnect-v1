import re
import datetime
import uuid
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from email_validator import validate_email, EmailNotValidError
from flask_mail import Message
from app import mail


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
            validator_response = validate_email(email, check_deliverability=False)
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

    def random_string(self, string_length=8):
        """Return a random string of length string_length"""
        random = str(uuid.uuid4())
        random = random.replace("-", "")
        return random[:string_length]

    def remove_extra_spaces(self, **kwargs):
        """Maximum number of spaces between words should be one"""
        norm = {}
        for key in kwargs:
            strip_text = kwargs[key].strip()
            norm_string = re.sub(r'\s+', ' ', strip_text)
            norm[key] = norm_string
        return norm

    def send_reset_password(self, email, password):
        """Returns a random string of length string_length"""
        message = Message(
            subject='Weconnect Account Password Reset',
            recipients=[email],
            html='Your new password is: {}'.format(password) +
                 '<br><a href="https://github.com/muthash" target="_blank">Click here to reset password</a>'
        )
        mail.send(message)
    
    def normalize_email(self, email):
        """Lowercase the domain part of the email"""
        email_part = email.split('@')
        domain = email_part[1].lower()
        email = email_part[0]+domain
        return email

