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



    @classmethod
    def get_default_filter(cls):
        DEFAULT_FILTER = DEFAULT_FILTERS["NONE"] # To change it, check all the available options of DEFAULT_FILTERS.
        return DEFAULT_FILTER
    
    @classmethod
    def get_multiple_upload_flag(cls):
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    



class ShutdownAvailedList(StandardInterface):
    __tablename__ = "ShutdownAvailedList"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Outage\Shutdown Availed List"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FY"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": True, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": True, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": True, "Financial Year & Quarter": True}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD



class DayAheadForecastingError(StandardInterface):
    __tablename__ = "DayAheadForecastingError"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Forecasting\Day Ahead Forecasting Error"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FY"]
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
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": True, "Financial Year & Quarter": False}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    



class IntraDayForecastingError(StandardInterface):
    __tablename__ = "IntraDayForecastingError"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Forecasting\Intra Day Forecasting Error"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FY"]
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
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": True, "Financial Year & Quarter": False}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    


class WeekAheadForecastingError(StandardInterface):
    __tablename__ = "WeekAheadForecastingError"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Forecasting\Week Ahead Forecasting Error"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FY"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": True, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": True, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": True, "Financial Year & Quarter": False}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    




class WeekAheadRollingForecast(StandardInterface):
    __tablename__ = "WeekAheadRollingForecast"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Forecasting\Week Ahead Rolling Forecast"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FY"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": True, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": True, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": True, "Financial Year & Quarter": False}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    


class MonthAheadForecastingError(StandardInterface):
    __tablename__ = "MonthAheadForecastingError"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Forecasting\Month Ahead Forecasting Error"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FY"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": True, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": True, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": False, "Year": True, "Month": True, "Financial Year & Quarter": False}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    



class YearAheadForecastingError(StandardInterface):
    __tablename__ = "YearAheadForecastingError"

    @classmethod
    def get_upload_path(cls):
        return "\System Operation\Forecasting\Year Ahead Forecasting Error"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["YEAR"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": False, "quarter": False, "year": True,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": True, "quarter": False, "year": True,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": False, "actualUploadDate": False, "size": False }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": False, "Year": True, "Month": False, "Financial Year & Quarter": False}
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
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
class UserRoles(db.Model):
    __tablename__ = "UserRoles"   
    uniqueUserId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    roles = db.Column(ARRAY(db.String), nullable=False, default=[])



class PagePermissions(db.Model):
    __tablename__ = "PagePermissions"   
    uniquePageId = db.Column(db.String(200), primary_key=True, unique=True, nullable=False)
    readPermissions = db.Column(ARRAY(db.String), nullable=False, default=[])
    writePermissions = db.Column(ARRAY(db.String), nullable=False, default=[])
