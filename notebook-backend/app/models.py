# app/models.py
from app import db
from datetime import datetime

class Folder(db.Model):
    __tablename__ = 'folders'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    notes_html = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    images = db.relationship('Image', backref='folder', cascade='all, delete-orphan', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'notes_html': self.notes_html or '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'image_count': len(self.images)
        }

class Image(db.Model):
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    url = db.Column(db.String(500), nullable=False)
    folder_id = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'url': self.url,
            'folder_id': self.folder_id,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }