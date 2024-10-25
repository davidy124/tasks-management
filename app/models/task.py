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
            'status',
            'priority',
            'assignee',
            'due_date',
            {'fields': ['$title'], 'default_language': 'english'}  # Text index on title
        ]
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'priority': self.priority,
            'assignee': str(self.assignee.id) if self.assignee else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
