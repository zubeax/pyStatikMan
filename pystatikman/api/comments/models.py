__author__ = 'Axel Zuber'

from pystatikman.api.base import BaseModel, db
from marshmallow import Schema, fields

class Comment(BaseModel):
    """
    Comment class that defines how comment objects are stored in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=False)
    parent = db.Column(db.String(200), unique=False, index=True)
    author = db.Column(db.String(120), unique=False)
    email = db.Column(db.String(120), unique=False)
    origindomain = db.Column(db.String(200), unique=False)
    commenttext = db.Column(db.String(1024), unique=False)
    status = db.Column(db.String(30), unique=False)

    def __init__(self, slug, parent, author, email, origindomain, commenttext ):
        self.slug = slug
        self.parent = parent
        self.author = author
        self.email = email
        self.origindomain = origindomain
        self.commenttext = commenttext

    def as_dict(self):
        comment_dict = {}
        for c in self.__table__.columns:
            comment_dict[c.name] = getattr(self, c.name)
        return comment_dict

    def __repr__(self):
        return '<Comment %r>' % self.commenttext


class CommentSchema(Schema):
    """
    Serializer for the Comment class.
    """
    id = fields.Str()
    slug = fields.Str()
    parent = fields.Str()
    author = fields.Str()
    email = fields.Str()
    origindomain = fields.Str()
    commenttext = fields.Str()
    status = fields.Str()

    class Meta:
        fields = ('id', 'slug', 'parent', 'author', 'email', 'origindomain', 'commenttext', 'status', 'date_created' )