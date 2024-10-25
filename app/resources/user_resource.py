from flask_restful import Resource, reqparse
from flask import request
from app.services.user_service import UserService
from mongoengine.errors import ValidationError
import logging

logger = logging.getLogger(__name__)


class UserResource(Resource):
    def get(self, user_id):
        logger.debug(f"GET request for user_id: {user_id}")
        try:
            user = UserService.get_user_by_id(user_id)
            return user.to_dict(), 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 404
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            return {"message": "An error occurred"}, 500

    def put(self, user_id):
        logger.debug(f"PUT request for user_id: {user_id}")
        try:
            user_data = request.get_json()
            user = UserService.update_user(user_id, user_data)
            return user.to_dict(), 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 404
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"message": str(e)}, 400
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            return {"message": "An error occurred"}, 500

    def delete(self, user_id):
        try:
            UserService.delete_user(user_id)
            return {"message": "User deleted successfully"}, 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 404
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            return {"message": "An error occurred"}, 500

class UserListResource(Resource):
    def get(self):
        logger.debug("GET request for users")
        search_term = request.args.get('search', '')
        try:
            if search_term:
                users = UserService.search_users_by_username(search_term)
                logger.info(f"Retrieved {len(users)} users matching '{search_term}'")
            else:
                users = UserService.get_all_users()
                logger.info(f"Retrieved {len(users)} users")
            return [user.to_dict() for user in users], 200
        except Exception as e:
            logger.error(f"Error getting users: {str(e)}", exc_info=True)
            return {"message": "An error occurred", "error": str(e)}, 500

    def post(self):
        logger.debug("POST request to create a new user")
        try:
            user_data = request.get_json()
            user = UserService.create_user(user_data)
            return user.to_dict(), 201
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"message": str(e)}, 400
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}", exc_info=True)
            return {"message": "An error occurred"}, 500
