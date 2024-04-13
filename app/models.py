from beanie import Document
from pydantic import BaseModel
from typing import Optional

from datetime import datetime
import pytz

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import relationship
# from app.database.database import PostgresBase

from sqlalchemy.ext.declarative import declarative_base    
PostgresBase = declarative_base()


class Videos(PostgresBase):
    __tablename__ = "videos"

    video_id = Column(String, unique=True, nullable=False, primary_key=True)
    video_name = Column(String, unique=True, nullable=False)
    video_status = Column(String, unique=True, nullable=False)
    predictions = Column(String, unique=True, nullable=False)
    date_created = Column(DateTime, default=datetime.now(pytz.timezone("Asia/Singapore")))

    def __repr__(self):
        return f'<{self.video_id}: Status {self.video_status}>'
    
    def __init__(self, video_id, video_name):
        self.video_id = video_id
        self.video_name = video_name
        self.video_status = "processing"
        self.predictions = ""
    
    def serialize(self):
        return {
            "video_id": self.id,
            "firstName": self.firstname,
            "lastName": self.lastname,
            "email": self.email,
            "salt": self.salt, 
            "password": self.password,
            "role": self.role,
            "date_created": self.date_created,
        }
