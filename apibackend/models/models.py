from flask_sqlalchemy import SQLAlchemy
import uuid
from .modelUtilities import getJSCompatibleTimeStamp
from standardInterface.standardInterfaceUtilities import DEFAULT_FILTERS, MULTIPLE_UPLOADS, UPLOAD_POINTS_CHOICE, CUSTOM_UPLOADED_ON

db = SQLAlchemy()

def getModelClass(targetTableClass):
    return eval(targetTableClass)


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
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FILE_DATE"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": True, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": True, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": False, "Financial Year & Quarter": True}
        return FILTERS_IN_USE
    
    @classmethod
    def get_custom_uploaded_on_flag(cls):
        CUSTOM_UPLOADED_ON_FLAG = CUSTOM_UPLOADED_ON["TRUE"] # To Change it to False, Make it to CUSTOM_UPLOADED_ON["FALSE"]
        return CUSTOM_UPLOADED_ON_FLAG

    @classmethod
    def get_default_filter(cls):
        DEFAULT_FILTER = DEFAULT_FILTERS["NONE"] # To change it, check all the available options of DEFAULT_FILTERS.
        return DEFAULT_FILTER
    
    @classmethod
    def get_multiple_upload_flag(cls):
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["TRUE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    

