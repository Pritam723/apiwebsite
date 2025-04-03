from models.models import StandardInterface 
from standardInterface.standardInterfaceUtilities import DEFAULT_FILTERS, MULTIPLE_UPLOADS, UPLOAD_POINTS_CHOICE, CUSTOM_UPLOADED_ON

class FTCDocuments(StandardInterface):
    __tablename__ = "FTCDocuments"

    @classmethod
    def get_upload_path(cls):
<<<<<<< HEAD
        return "\Scheduling\Final Schedule"
=======
        return "\Market Operation/FTC/FTC Documents"
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac

    @classmethod
    def get_read_permissions(cls):
        return ["ALL"]
    @classmethod
    def get_write_permissions(cls):
<<<<<<< HEAD
        return ["SO_ADMIN", "MO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["FILE_DATE"]
=======
        return ["MO_ADMIN"]
    
    @classmethod
    def get_upload_points(cls):
        UPLOAD_POINTS = UPLOAD_POINTS_CHOICE["NONE"]
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
        return UPLOAD_POINTS

    @classmethod
    def get_data_to_display(cls):
<<<<<<< HEAD
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": True, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": False, "uploadedBy": True, "actualUploadDate": False, "size": True }
=======
        DATA_TO_DISPLAY = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": False, "uploadedBy": False, "actualUploadDate": False, "size": False }
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
        return DATA_TO_DISPLAY
    
    @classmethod
    def get_sort_in_use(cls):
<<<<<<< HEAD
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": True, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": False, "uploadedBy": True, "actualUploadDate": False, "size": True }
=======
        SORT_IN_USE = { "id": False, "fileName": True, "fileDate": False, "weekStartsEnds": False, "month": False, "quarter": False, "year": False,
                        "fy": False, "fileDateFromTo": False, "uploadedOn": False, "uploadedBy": False, "actualUploadDate": False, "size":False }
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
        return SORT_IN_USE
    
    @classmethod
    def get_filters_in_use(cls):
<<<<<<< HEAD
        FILTERS_IN_USE = { "Date Range": True, "Year": True, "Month": True, "Financial Year": True, "Financial Year & Quarter": False}
=======
        FILTERS_IN_USE = { "Date Range": False, "Year": False, "Month": False, "Financial Year": False, "Financial Year & Quarter": False}
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
        return FILTERS_IN_USE
    
    @classmethod
    def get_custom_uploaded_on_flag(cls):
<<<<<<< HEAD
        CUSTOM_UPLOADED_ON_FLAG = CUSTOM_UPLOADED_ON["TRUE"] # To Change it to False, Make it to CUSTOM_UPLOADED_ON["FALSE"]
=======
        CUSTOM_UPLOADED_ON_FLAG = CUSTOM_UPLOADED_ON["FALSE"] # To Change it to False, Make it to CUSTOM_UPLOADED_ON["FALSE"]
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
        return CUSTOM_UPLOADED_ON_FLAG

    @classmethod
    def get_default_filter(cls):
        DEFAULT_FILTER = DEFAULT_FILTERS["NONE"] # To change it, check all the available options of DEFAULT_FILTERS.
        return DEFAULT_FILTER
    
    @classmethod
    def get_multiple_upload_flag(cls):
        ALLOW_MULTIPLE_UPLOAD = MULTIPLE_UPLOADS["FALSE"]  # To Change it to False, Make it to MULTIPLE_UPLOADS["FALSE"]
<<<<<<< HEAD
        return ALLOW_MULTIPLE_UPLOAD
    









=======
        return ALLOW_MULTIPLE_UPLOAD
>>>>>>> 536a4e26584e5c3a61bfd407bf2bf328acc838ac
