"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(70), nullable=False)
    last_name = db.Column(db.String(70), nullable=False)
    img_url = db.Column(
                db.String(2048), 
                nullable=False,
                default='https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'
            )
    posts = db.relationship('Post', backref='users', cascade='all, delete')
    
    def __repr__(self):
        u = self
        return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} img_url={u.img_url}>'
    
    def get_full_name(self):
        """Return full name"""
        return f'{self.first_name} {self.last_name}'
    
    full_name = property(fget=get_full_name)


class Post(db.Model):
    """Post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(70), nullable=False)
    content = db.Column(db.String(2200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at} user_id={p.user_id}>"