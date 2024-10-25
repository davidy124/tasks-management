from flask import Flask, request, jsonify
from flask_restful import Api
from flask_mongoengine import MongoEngine
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config import Config
import logging
from mongoengine import connect, connection

load_dotenv()

db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    if os.getenv('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = True

    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    @app.before_request
    def log_request_info():
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())

    @app.after_request
    def log_response_info(response):
        app.logger.debug('Response Status: %s', response.status)
        app.logger.debug('Response Headers: %s', response.headers)
        app.logger.debug('Response Data: %s', response.data)
        return response

    @app.errorhandler(connection.ConnectionFailure)
    def handle_connection_error(e):
        app.logger.error(f"MongoDB connection error: {str(e)}")
        return jsonify({"message": "Database connection error"}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify({"message": "An unexpected error occurred"}), 500

    try:
        app.logger.info("Attempting to connect to the database")
        app.logger.debug(f"MongoDB settings: {app.config['MONGODB_SETTINGS']}")
        db.init_app(app)
        with app.app_context():
            db.connection.server_info()
        app.logger.info("Successfully connected to the database")
    except Exception as e:
        app.logger.error(f"Failed to connect to the database: {str(e)}")

    from app.resources.task_resource import TaskResource, TaskListResource
    from app.resources.user_resource import UserResource, UserListResource

    api = Api(app, prefix='/api')
    api.add_resource(TaskListResource, '/tasks')
    api.add_resource(TaskResource, '/tasks/<string:task_id>')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:user_id>')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        try:
            with app.app_context():
                db.connection.server_info()
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "environment": os.getenv('FLASK_ENV', 'development')
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 500

    @app.route('/api/test', methods=['GET'])
    def test_endpoint():
        return jsonify({"message": "Test endpoint working"}), 200

    return app
