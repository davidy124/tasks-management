from app.repositories.user_repository import UserRepository
from mongoengine.errors import DoesNotExist

class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return UserRepository.get_user_by_id(user_id)
        except DoesNotExist:
            raise ValueError(f"User with id {user_id} not found")

    @staticmethod
    def create_user(user_data):
        return UserRepository.create_user(user_data)

    @staticmethod
    def update_user(user_id, user_data):
        try:
            user = UserRepository.get_user_by_id(user_id)
            return UserRepository.update_user(user_id, user_data)
        except DoesNotExist:
            raise ValueError(f"User with id {user_id} not found")

    @staticmethod
    def delete_user(user_id):
        try:
            UserRepository.delete_user(user_id)
        except DoesNotExist:
            raise ValueError(f"User with id {user_id} not found")

    @staticmethod
    def search_users_by_username(search_term):
        return UserRepository.search_users_by_username(search_term)
