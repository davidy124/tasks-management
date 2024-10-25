import pytest
from app.services.task_service import TaskService
from app.models.task import Task

def test_get_all_tasks(mocker):
    # Arrange
    mock_repo = mocker.patch('app.repositories.task_repository.TaskRepository')
    mock_tasks = [Task(title="Task 1"), Task(title="Task 2")]
    mock_repo.get_all_tasks.return_value = mock_tasks

    # Act
    result = TaskService.get_all_tasks()

    # Assert
    assert result == mock_tasks
    mock_repo.get_all_tasks.assert_called_once()

def test_get_task_by_id_success(mocker):
    # Arrange
    mock_repo = mocker.patch('app.repositories.task_repository.TaskRepository')
    mock_task = Task(title="Test Task")
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
