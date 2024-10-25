from app.models.user import User
from mongoengine.errors import DoesNotExist

class UserRepository:
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.get(id=user_id)

    @staticmethod
    def create_user(user_data):
        user = User(**user_data)
        user.save()
        return user

    @staticmethod
    def update_user(user_id, user_data):
        user = User.objects.get(id=user_id)
        user.update(**user_data)
        user.reload()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.objects.get(id=user_id)
        user.delete()
