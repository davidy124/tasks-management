from flask_restful import Resource, reqparse
from app.services.task_service import TaskService
from mongoengine.errors import ValidationError
import logging

logger = logging.getLogger(__name__)


class TaskResource(Resource):
    def get(self, task_id):
        logger.debug(f"GET request for task_id: {task_id}")
        try:
            task = TaskService.get_task_by_id(task_id)
            return task.to_dict(), 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 404
        except Exception as e:
            logger.error(f"Error getting task: {str(e)}")
            return {"message": "An error occurred"}, 500

    def put(self, task_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('due_date', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('priority', type=str)
        parser.add_argument('assignee', type=str)
        args = parser.parse_args(strict=True)

        try:
            task = TaskService.update_task(task_id, args)
            return task.to_dict(), 200
        except ValueError as e:
            return {"message": str(e)}, 404
        except ValidationError as e:
            return {"message": str(e)}, 400

    def delete(self, task_id):
        try:
            TaskService.delete_task(task_id)
            return {"message": "Task deleted successfully"}, 200
        except ValueError as e:
            return {"message": str(e)}, 404


class TaskListResource(Resource):
    def get(self):
        logger.debug("GET request for all tasks")
        try:
            tasks = TaskService.get_all_tasks()
            logger.info(f"Retrieved {len(tasks)} tasks")
            return [task.to_dict() for task in tasks], 200
        except Exception as e:
            logger.error(f"Error getting all tasks: {str(e)}", exc_info=True)
            return {"message": "An error occurred", "error": str(e)}, 500

    def post(self):
        logger.debug("POST request to create a new task")
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('description', type=str)
        parser.add_argument('due_date', type=str)
        parser.add_argument('status', type=str)
        parser.add_argument('priority', type=str)
        parser.add_argument('assignee', type=str)
        args = parser.parse_args(strict=True)

        try:
            task = TaskService.create_task(args)
            return task.to_dict(), 201
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"message": str(e)}, 400
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}", exc_info=True)
            return {"message": "An error occurred"}, 500
