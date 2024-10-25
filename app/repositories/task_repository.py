from app.models.task import Task

class TaskRepository:
    @staticmethod
    def get_all_tasks():
        return Task.objects.all()

    @staticmethod
    def get_task_by_id(task_id):
        return Task.objects.get(id=task_id)

    @staticmethod
    def create_task(task_data):
        task = Task(**task_data)
        task.save()
        return task

    @staticmethod
    def update_task(task_id, task_data):
        task = Task.objects.get(id=task_id)
        task.update(**task_data)
        task.reload()
        return task

    @staticmethod
    def delete_task(task_id):
        task = Task.objects.get(id=task_id)
        task.delete()
