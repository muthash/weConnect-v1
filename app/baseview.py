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
    @staticmethod
    def validate_json():
        """Returns false if request is json"""
        if request.get_json(silent=True) is None:
            response = {'message': 'The Request should be JSON format'}
            return jsonify(response), 400
        return False

    @staticmethod
    def check_email(email):
        try:
            validator_response = validate_email(email,
                                                check_deliverability=False)
            email = validator_response["email"]
            return False
        except EmailNotValidError as error:
            response = {'message': str(error)}
            return jsonify(response), 400

    @staticmethod
    def validate_null(**kwargs):
        """Returns a list with null fields"""
        messages = []
        for key in kwargs:
            strip_text = True
            if kwargs[key] is not None:
                strip_text = re.sub(r'\s+', '', kwargs[key])
            if not strip_text:
                    message = f'The {key} should not be empty'
                    messages.append(message)
            if kwargs[key] is None:
                message = f'The {key} should not be missing'
                messages.append(message)
        if messages:
            response = {'message': messages}
            return jsonify(response), 400
        return False

    @staticmethod
    def generate_token(user, username,
                       expires=datetime.timedelta(hours=1)):
        """Return access token and response to user"""
        response = {
            'message': f'Login successfull. Welcome {username}',
            'access_token': create_access_token(identity=user,
                                                expires_delta=expires)
        }
        return jsonify(response), 200

    @staticmethod
    def random_string(string_length=8):
        """Return a random string of length string_length"""
        random = str(uuid.uuid4())
        random = random.replace("-", "")
        return random[:string_length]

    @staticmethod
    def remove_extra_spaces(**kwargs):
        """Maximum number of spaces between words should be one"""
        norm = {}
        for key in kwargs:
            strip_text = kwargs[key].strip()
            norm_string = re.sub(r'\s+', ' ', strip_text)
            norm[key] = norm_string
        return norm

    @staticmethod
    def send_reset_password(email, password):
        """Returns a random string of length string_length"""
        message = Message(
            subject='Weconnect Account Password Reset',
            recipients=[email],
            html=f'Your new password is: {password}'
        )
        mail.send(message)

    @staticmethod
    def normalize_email(email):
        """Lowercase the domain part of the email"""
        email_part = email.split('@')
        domain = email_part[1].lower()
        email = email_part[0]+'@'+domain
        return email

    @staticmethod
    def check_password(password):
        if re.match(r"(?=\D*\d)(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])[A-Za-z0-9]{8,}$", password):
            return False
        response = {'message': 'Password should contain at least eight ' +
                               'characters with at least one digit, one ' +
                               'uppercase letter and one lowercase letter'}
        return jsonify(response), 400
