from flask_restful import Resource
from flask import request
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
        logger.debug(f"PUT request for task_id: {task_id}")
        try:
            task_data = request.get_json()
            task = TaskService.update_task(task_id, task_data)
            return task.to_dict(), 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 404
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"message": str(e)}, 400
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            return {"message": "An error occurred"}, 500

    def delete(self, task_id):
        try:
            TaskService.delete_task(task_id)
            return {"message": "Task deleted successfully"}, 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 404
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return {"message": "An error occurred"}, 500

class TaskListResource(Resource):
    def get(self):
        logger.debug("GET request for tasks")
        search_term = request.args.get('search', '')
        user_id = request.args.get('userid', '')

        try:
            if user_id:
                tasks = TaskService.get_tasks_by_user(user_id)
                logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")
            elif search_term:
                tasks = TaskService.search_tasks_by_title(search_term)
                logger.info(f"Retrieved {len(tasks)} tasks matching '{search_term}'")
            else:
                tasks = TaskService.get_all_tasks()
                logger.info(f"Retrieved {len(tasks)} tasks")
            return [task.to_dict() for task in tasks], 200
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 400
        except Exception as e:
            logger.error(f"Error getting tasks: {str(e)}", exc_info=True)
            return {"message": "An error occurred", "error": str(e)}, 500

    def post(self):
        logger.debug("POST request to create a new task")
        try:
            task_data = request.get_json()
            task = TaskService.create_task(task_data)
            return task.to_dict(), 201
        except ValueError as e:
            logger.warning(str(e))
            return {"message": str(e)}, 400
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            return {"message": str(e)}, 400
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}", exc_info=True)
            return {"message": "An error occurred"}, 500
