from models.models import StandardInterface 
from standardInterface.standardInterfaceUtilities import DEFAULT_FILTERS, MULTIPLE_UPLOADS, UPLOAD_POINTS_CHOICE, CUSTOM_UPLOADED_ON

class MonthlyDeviationReport(StandardInterface):
    __tablename__ = "MonthlyDeviationReport"

    @classmethod
    def get_upload_path(cls):
        return "\Reports\Monthly Deviation Report"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
        return ["SO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["MONTH"]
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": True, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": True, "actualUploadDate": False, "size": True }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": True, "fileDateFromTo": False, "uploadedOn": True, "uploadedBy": True, "actualUploadDate": False, "size":False }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": False, "Year": True, "Month": False, "Financial Year": True, "Financial Year & Quarter": True}
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