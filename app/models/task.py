from app import db
from datetime import datetime

class Task(db.Document):
    title = db.StringField(required=True, max_length=200)
    description = db.StringField(max_length=1000)
    due_date = db.DateTimeField()
    status = db.StringField(choices=['todo', 'in_progress', 'done'], default='todo')
    priority = db.StringField(choices=['low', 'medium', 'high'], default='medium')
    assignee = db.ReferenceField('User')
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()

    meta = {
        'collection': 'tasks',
        'indexes': [
            'title',
            'status',
            'priority',
            'assignee',
            'due_date'
        ]
    }
