from models.models import StandardInterface 
from standardInterface.standardInterfaceUtilities import DEFAULT_FILTERS, MULTIPLE_UPLOADS, UPLOAD_POINTS_CHOICE, CUSTOM_UPLOADED_ON

class GenerationOutage(StandardInterface):
    __tablename__ = "GenerationOutage"

    @classmethod
    def get_upload_path(cls):
        return "\Reports\Daily Report\Generation Outage"

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
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
                        "fy": False, "fileDateFromTo": False, "uploadedOn": False, "uploadedBy": True, "actualUploadDate": False, "size":False }
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": True, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": False, "uploadedBy": True, "actualUploadDate": False, "size": False }
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
        FILTERS_IN_USE = { "Date Range": False, "Year": True, "Month": False, "Financial Year": False, "Financial Year & Quarter": False}
        return FILTERS_IN_USE
    
    @classmethod
    def get_custom_uploaded_on_flag(cls):
        CUSTOM_UPLOADED_ON_FLAG = CUSTOM_UPLOADED_ON["TRUE"] # To Change it to False, Make it to CUSTOM_UPLOADED_ON["FALSE"]
        return CUSTOM_UPLOADED_ON_FLAG

    @classmethod
    def get_default_filter(cls):
        DEFAULT_FILTER = DEFAULT_FILTERS["CURRENT_YEAR"] # To change it, check all the available options of DEFAULT_FILTERS.
        return DEFAULT_FILTER
    
    @classmethod
    def get_multiple_upload_flag(cls):
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
        return ALLOW_MULTIPLE_UPLOAD
    









