import pytest
from app.services.task_service import TaskService
from app.models.task import Task
from mongoengine import connect, disconnect


@pytest.fixture(scope='module', autouse=True)
def setup_test_db():
    # Connect to a test database
    connect('testdb', host='mongomock://localhost')
    yield
    # Disconnect and clear the database after tests
    disconnect()


@pytest.fixture(autouse=True)
def setup_test_collection():
    # Clear the collection before each test
    Task.objects.delete()


def test_get_all_tasks(mocker):
    # Arrange
    mock_tasks = [Task(title="Task 1"), Task(title="Task 2")]
    mock_repo = mocker.patch('app.repositories.task_repository.TaskRepository')
    mock_repo.get_all_tasks.return_value = mock_tasks

    # Act
    result = TaskService.get_all_tasks()

    # Assert
    assert list(result) == mock_tasks
    mock_repo.get_all_tasks.assert_called_once()


def test_get_task_by_id_success(mocker):
    # Arrange
    mock_task = Task(title="Test Task")
    mock_repo = mocker.patch('app.repositories.task_repository.TaskRepository')
    mock_repo.get_task_by_id.return_value = mock_task

    # Act
    result = TaskService.get_task_by_id("123")

    # Assert
    assert result == mock_task
    mock_repo.get_task_by_id.assert_called_once_with("123")


def test_get_task_by_id_not_found(mocker):
    # Arrange
    mock_repo = mocker.patch('app.repositories.task_repository.TaskRepository')
    mock_repo.get_task_by_id.side_effect = ValueError("Task not found")

    # Act & Assert
    with pytest.raises(ValueError):
        TaskService.get_task_by_id("123")
