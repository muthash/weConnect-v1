""" The create_app function wraps the creation of a new Flask object, and
    returns it after it's loaded up with configuration settings
    using app.config
"""
from flask import jsonify
from flask_api import FlaskAPI
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from instance.config import app_config

jwt = JWTManager()
mail = Mail()


def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    jwt.init_app(app)
    mail.init_app(app)

    from app.auth.views import auth
    from app.auth.views import blacklist
    from app.business.views import biz, rev

    @app.errorhandler(400)
    def bad_request(error):
        """Error handler for a bad request"""
        return jsonify(dict(error='The Server did not understand' +
                                  'the request')), 400

    @app.errorhandler(404)
    def not_found(error):
        """Error handler for not found page"""
        return jsonify(dict(error='The Resource is not available')), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Error handler for wrong method to an endpoint"""
        return jsonify(dict(error='The HTTP request Method' +
                                  ' is not allowed')), 405

    @app.errorhandler(500)
    def server_error(error):
        """Error handler for a server failure"""
        return jsonify(dict(error='The server encountered an internal error' +
                                  ' and was unable to' +
                                  ' complete your request')), 500

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """Check if token is blaclisted before allowing access to a route"""
        jti = decrypted_token['jti']
        return jti in blacklist

    app.register_blueprint(auth)
    app.register_blueprint(biz)
    app.register_blueprint(rev)

    return app
