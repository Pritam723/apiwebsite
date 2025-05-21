from flask_sqlalchemy import SQLAlchemy
import uuid
from .modelUtilities import getJSCompatibleTimeStamp
from sqlalchemy.dialects.postgresql import ARRAY


db = SQLAlchemy()

def getModelClass(targetTableClass):
    # print("Here")
    import standardInterface.stardardInterfaceTables as STANDARD_INTERFACE_TABLES
    FIND_TABLE = None
    try:
        FIND_TABLE = f"STANDARD_INTERFACE_TABLES.{targetTableClass}.{targetTableClass}"
        return eval(FIND_TABLE)
    except Exception as e:
        print(e)
        print("Not able to find it..........")
        FIND_TABLE = f"{targetTableClass}"
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
    userId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=True)
    name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200), nullable=True)
    mobileNumber = db.Column(db.String(20), nullable=True)
    organization = db.Column(db.String(200), nullable=True)
    userCreatedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    lastModifiedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    isDeleted = db.Column(db.Boolean, nullable=True)
    isValidated = db.Column(db.Boolean, nullable=True)
    validationCode = db.Column(db.String(10), nullable=True)
    codeValidity = db.Column(db.DateTime(timezone=True), nullable=True)
    
class UserRoles(db.Model):
    __tablename__ = "UserRoles"   
    uniqueUserId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    roles = db.Column(ARRAY(db.String), nullable=False, default=[])



class PagePermissions(db.Model):
    __tablename__ = "PagePermissions"   
    uniquePageId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    readPermissions = db.Column(ARRAY(db.String), nullable=False, default=[])
    writePermissions = db.Column(ARRAY(db.String), nullable=False, default=[])




class Albums(db.Model):
    __tablename__ = "Albums"   
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    title = db.Column(db.String(800), nullable=False)
    year = db.Column(db.DateTime(timezone=True), nullable=True)
    cover = db.Column(db.String(200), nullable=False)
    noImages = db.Column(db.Integer, nullable=False, default=0)
    images = db.Column(ARRAY(db.String), nullable=True, default=[])  # List of strings/imagenames
    uploadedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    uploadedBy = db.Column(db.String(100), nullable=True)

    @classmethod
    def get_upload_path(cls):
        return "\images"
    
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'id': self.id,
            'title': self.title,
            'year': getJSCompatibleTimeStamp(self.year),
            'cover': self.cover,
            'noImages': self.noImages,
            # 'images': self.images,
            'uploadedOn': self.uploadedOn,
            # 'uploadedOn': getJSCompatibleTimeStamp(self.uploadedOn)   
       }
    
    
    @classmethod
    def get_upload_points(cls):
        return {}

    @classmethod
    def get_data_to_display(cls):
        return {}
    
    @classmethod
    def get_sort_in_use(cls):
        return {}
    
    @classmethod
    def get_filters_in_use(cls):
        return {}
    
    @classmethod
    def get_custom_uploaded_on_flag(cls):
        return False

    @classmethod
    def get_default_filter(cls):
        return None
    
    @classmethod
    def get_multiple_upload_flag(cls):
        return True


class Images(db.Model):
    __tablename__ = "Images"   
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    imageName = db.Column(db.String(200), nullable=False)
    imageWidth = db.Column(db.Integer, nullable=False, default=320)
    imageHeight = db.Column(db.Integer, nullable=False, default=213)
    partOfAlbum = db.Column(db.String(200), nullable=True)

class Tenders(db.Model):
    __tablename__ = "Tenders"   
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    description = db.Column(db.String(4000), nullable=False)
    nitRef = db.Column(db.String(200), nullable=False)
    bidStartDate = db.Column(db.DateTime(timezone=True), nullable=True)
    bidEndDate = db.Column(db.String(200), nullable=False)
    bidOpeningDate = db.Column(db.String(200), nullable=False)
    
    tenderFilesActual = db.Column(ARRAY(db.String), nullable=True, default=[])  # List of strings/files
    tenderFilesStored = db.Column(ARRAY(db.String), nullable=True, default=[])  # List of strings/files


    uploadedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    uploadedBy = db.Column(db.String(100), nullable=True)

    downloadedTimes = db.Column(db.Integer, nullable=False, default=0)

    @classmethod
    def get_upload_path(cls):
        return "\More\Tenders"
    
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'id': self.id,
            'description': self.description,
            'nitRef': self.nitRef,
            'bidStartDate': getJSCompatibleTimeStamp(self.bidStartDate),
            'bidEndDate': self.bidEndDate,
            'bidOpeningDate': self.bidOpeningDate,
            'tenderFilesActual': self.tenderFilesActual,
            'downloadedTimes': self.downloadedTimes,
            'uploadedBy': self.uploadedBy,
            'uploadedOn': getJSCompatibleTimeStamp(self.uploadedOn),
            'downloadedTimes': self.downloadedTimes 
       }
    
    
    @classmethod
    def get_upload_points(cls):
        return {}

    @classmethod
    def get_data_to_display(cls):
        return {}
    
    @classmethod
    def get_sort_in_use(cls):
        return {}
    
    @classmethod
    def get_filters_in_use(cls):
        return {}
    
    @classmethod
    def get_custom_uploaded_on_flag(cls):
        return False

    @classmethod
    def get_default_filter(cls):
        return None
    
    @classmethod
    def get_multiple_upload_flag(cls):
        return True




class HRDocuments(db.Model):
    __tablename__ = "HRDocuments"   
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    typeOfDocument = db.Column(db.String(200), nullable=False, unique=True)    
    uploadedOn = db.Column(db.DateTime(timezone=True), nullable=True)
    uploadedBy = db.Column(db.String(100), nullable=True)


    @classmethod
    def get_upload_path(cls):
        # return "\More\Upload Documents\HR Documents"
        # Use static path for this.
        return None
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
            'id': self.id,
            'typeOfDocument': self.typeOfDocument,
            'uploadedOn': getJSCompatibleTimeStamp(self.uploadedOn),
            'uploadedBy': self.uploadedBy,
       }
    
    
    @classmethod
    def get_upload_points(cls):
        return {}

    @classmethod
    def get_data_to_display(cls):
        return {}
    
    @classmethod
    def get_sort_in_use(cls):
        return {}
    
    @classmethod
    def get_filters_in_use(cls):
        return {}
    
    @classmethod
    def get_custom_uploaded_on_flag(cls):
        return False

    @classmethod
    def get_default_filter(cls):
        return None
    
    @classmethod
    def get_multiple_upload_flag(cls):
        return True