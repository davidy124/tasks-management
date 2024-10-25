from app.repositories.task_repository import TaskRepository
from app.services.user_service import UserService
from app.models.user import User
from datetime import datetime
from mongoengine.errors import DoesNotExist, ValidationError
from bson import ObjectId

class TaskService:
    @staticmethod
    def get_all_tasks():
        return TaskRepository.get_all_tasks()

    @staticmethod
    def get_task_by_id(task_id):
        try:
            return TaskRepository.get_task_by_id(task_id)
        except DoesNotExist:
            raise ValueError(f"Task with id {task_id} not found")

    @staticmethod
    def create_task(task_data):
        # Check if assignee exists and convert to User object
        if 'assignee' in task_data:
            try:
                assignee_id = task_data['assignee']
                user = UserService.get_user_by_id(assignee_id)
                task_data['assignee'] = user
            except ValueError:
                raise ValueError(f"Assignee with id {assignee_id} not found")

        # Parse due_date if provided
        if 'due_date' in task_data:
            try:
                task_data['due_date'] = datetime.strptime(task_data['due_date'], "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                raise ValueError("Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)")

        # Add creation time
        task_data['created_at'] = datetime.utcnow()
        task_data['updated_at'] = task_data['created_at']
        return TaskRepository.create_task(task_data)

    @staticmethod
    def update_task(task_id, task_data):
        try:
            # Check if assignee exists and convert to User object
            if 'assignee' in task_data:
                try:
                    assignee_id = task_data['assignee']
                    user = UserService.get_user_by_id(assignee_id)
                    task_data['assignee'] = user
                except ValueError:
                    raise ValueError(f"Assignee with id {assignee_id} not found")

            # Parse due_date if provided
            if 'due_date' in task_data:
                try:
                    task_data['due_date'] = datetime.strptime(task_data['due_date'], "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    raise ValueError("Invalid date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)")

            # Update the 'updated_at' field
            task_data['updated_at'] = datetime.utcnow()
            return TaskRepository.update_task(task_id, task_data)
        except DoesNotExist:
            raise ValueError(f"Task with id {task_id} not found")

    @staticmethod
    def delete_task(task_id):
        try:
            TaskRepository.delete_task(task_id)
        except DoesNotExist:
            raise ValueError(f"Task with id {task_id} not found")

    @staticmethod
    def search_tasks_by_title(search_term):
        return TaskRepository.search_tasks_by_title(search_term)

    @staticmethod
    def get_tasks_by_user(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            return TaskRepository.get_tasks_by_user(user)
        except ValueError:
            raise ValueError(f"User with id {user_id} not found")
