from flask_sqlalchemy import SQLAlchemy
import uuid
from .modelUtilities import getJSCompatibleTimeStamp

db = SQLAlchemy()

def getModelClass(targetTableClass):
    return eval(targetTableClass)


class Task(db.Model):
    __tablename__ = 'Tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    newCol = db.Column(db.String(10), nullable=True)

class StandardInterface(db.Model):
    __abstract__ = True
    
    # id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    fileName = db.Column(db.String(200), nullable=True)
    fileDate = db.Column(db.DateTime(timezone=True), nullable=True)
    weekStarts = db.Column(db.DateTime(timezone=True), nullable=True)
    weekEnds = db.Column(db.DateTime(timezone=True), nullable=True)
    month = db.Column(db.DateTime(timezone=True), nullable=True)
    quarter = db.Column(db.String(10), nullable=True)
    year = db.Column(db.DateTime(timezone=True), nullable=True)
    fy = db.Column(db.String(10), nullable=True)
    fileDateFrom = db.Column(db.DateTime(timezone=True), nullable=True)
    fileDateTo = db.Column(db.DateTime(timezone=True), nullable=True)
    uploadedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    uploadedBy = db.Column(db.String(100), nullable=True)
    actualUploadDate = db.Column(db.DateTime(timezone=True), nullable=True)
    lastUpdatedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    startDateToFilter = db.Column(db.DateTime(timezone=True), nullable=True)
    endDateToFilter = db.Column(db.DateTime(timezone=True), nullable=True)
    size = db.Column(db.String(30), nullable = True)
    filePath = db.Column(db.String(200), nullable=True)
    isMigrated = db.Column(db.Boolean, nullable=True)
    isDeleted = db.Column(db.Boolean, nullable=True)


    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'id': self.id,
           'fileName': self.fileName,
            'fileDate' : getJSCompatibleTimeStamp(self.fileDate),
            'weekStartsEnds' : [getJSCompatibleTimeStamp(self.weekStarts), getJSCompatibleTimeStamp(self.weekEnds)],
            'month' : getJSCompatibleTimeStamp(self.month),
            'quarter': self.quarter,
            'year': getJSCompatibleTimeStamp(self.year),
            'fy': self.fy,
            'fileDateFromTo': [getJSCompatibleTimeStamp(self.fileDateFrom), getJSCompatibleTimeStamp(self.fileDateTo)],
            'uploadedOn': getJSCompatibleTimeStamp(self.uploadedOn),
            'uploadedBy': self.uploadedBy,
            'size': self.size,
            'filePath': self.filePath,
            'isMigrated': self.isMigrated,     
       }


class PeakHour(StandardInterface):
    __tablename__ = "PeakHours"

    @classmethod
    def get_upload_path(cls):
        return "\Scheduling\Peak Hours and Season Declaration"

    @classmethod
    def get_read_permissions(cls):
        return ["SO_ADMIN"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
# class Test(db.Model):
#     __tablename__ = 'Tests'
#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     title = db.Column(db.String(200), nullable=False)
#     done = db.Column(db.Boolean, nullable=False)

