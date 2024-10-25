import unittest
from unittest.mock import patch, MagicMock
from app.services.task_service import TaskService
from app.models.task import Task
from mongoengine import connect, disconnect
import mongomock


class TestTaskService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up a mock database connection
        connect('mongoenginetest', host='mongomock://localhost', mongo_client_class=mongomock.MongoClient)

    @classmethod
    def tearDownClass(cls):
        # Disconnect the mock database
        disconnect()

    def setUp(self):
        # Clear the mock database before each test
        Task.objects.delete()

    @patch('app.repositories.task_repository.TaskRepository.get_all_tasks')
    def test_get_all_tasks(self, mock_get_all_tasks):
        # Arrange
        mock_tasks = [Task(title="Task 1"), Task(title="Task 2")]
        mock_get_all_tasks.return_value = mock_tasks

        # Act
        result = TaskService.get_all_tasks()

        # Assert
        self.assertEqual(result, mock_tasks)
        mock_get_all_tasks.assert_called_once()

    @patch('app.repositories.task_repository.TaskRepository.get_task_by_id')
    def test_get_task_by_id_success(self, mock_get_task_by_id):
        # Arrange
        mock_task = Task(title="Test Task")
        mock_get_task_by_id.return_value = mock_task

        # Act
        result = TaskService.get_task_by_id("123")

        # Assert
        self.assertEqual(result, mock_task)
        mock_get_task_by_id.assert_called_once_with("123")

    @patch('app.repositories.task_repository.TaskRepository.get_task_by_id')
    def test_get_task_by_id_not_found(self, mock_get_task_by_id):
        # Arrange
        mock_get_task_by_id.side_effect = ValueError("Task not found")

        # Act & Assert
        with self.assertRaises(ValueError):
            TaskService.get_task_by_id("123")

    @patch('app.repositories.task_repository.TaskRepository.create_task')
    def test_create_task(self, mock_create_task):
        # Arrange
        task_data = {"title": "New Task"}
        mock_task = Task(title="New Task")
        mock_create_task.return_value = mock_task

        # Act
        result = TaskService.create_task(task_data)

        # Assert
        self.assertEqual(result, mock_task)
        mock_create_task.assert_called_once()
        # You might want to add more assertions here to check the task_data


if __name__ == '__main__':
    unittest.main()
