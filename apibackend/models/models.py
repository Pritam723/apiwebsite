from flask_sqlalchemy import SQLAlchemy
import uuid
from .modelUtilities import getJSCompatibleTimeStamp
from sqlalchemy.dialects.postgresql import ARRAY


db = SQLAlchemy()

def getModelClass(targetTableClass):
    print("Here")
    import standardInterface.stardardInterfaceTables as STANDARD_INTERFACE_TABLES
    FIND_TABLE = f"STANDARD_INTERFACE_TABLES.{targetTableClass}.{targetTableClass}"
    print("Got the table")
    print(FIND_TABLE)
    return eval(FIND_TABLE)



# All the Classes Inheriting this should be inside standardInterface.stardardInterfaceTables
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



class User(db.Model):
    __tablename__ = "User"   
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    userId = db.Column(db.String(200), nullable=True)
    password = db.Column(db.String(500), nullable=True)
    eid = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    department = db.Column(db.String(200), nullable=True)
    mobileNumber = db.Column(db.String(20), nullable=True)
    organization = db.Column(db.String(200), nullable=True)
    userCreatedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    lastModifiedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    isDeleted = db.Column(db.Boolean, nullable=True)



class UserRoles(db.Model):
    __tablename__ = "UserRoles"   
    uniqueUserId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    roles = db.Column(ARRAY(db.String), nullable=False, default=[])



class PagePermissions(db.Model):
    __tablename__ = "PagePermissions"   
    uniquePageId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    readPermissions = db.Column(ARRAY(db.String), nullable=False, default=[])
    writePermissions = db.Column(ARRAY(db.String), nullable=False, default=[])