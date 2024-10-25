from app import db

class User(db.Document):
    username = db.StringField(required=True, unique=True, max_length=50)
    email = db.EmailField(required=True, unique=True)
    
    meta = {
        'collection': 'users',
        'indexes': [
            'username',
            'email'
        ]
    }

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email
        }
