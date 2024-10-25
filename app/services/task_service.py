from app.repositories.task_repository import TaskRepository
from datetime import datetime
from mongoengine.errors import DoesNotExist

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
        # Add creation time
        task_data['created_at'] = datetime.utcnow()
        task_data['updated_at'] = task_data['created_at']
        return TaskRepository.create_task(task_data)

    @staticmethod
    def update_task(task_id, task_data):
        try:
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
