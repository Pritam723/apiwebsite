from datetime import  datetime, timedelta
# from enum import Enum
import pandas as pd
import pytz
import base64
from codecs import encode
import os


DEFAULT_FILTERS = {
    "NONE" : None, # No filtering, will fetch all data.
    "LAST_ONE_YEAR" : "LAST_ONE_YEAR", # Will Filter Data for last 1-year ending today.
    "CURRENT_YEAR" : "CURRENT_YEAR", # Will Filter Data for current year. current year = today.year().
    "CURRENT_FINANCIAL_YEAR" : "CURRENT_FINANCIAL_YEAR", # Will Filter Data for current fy. current fy = today.fy().
    "CURRENT_FYQ" : "CURRENT_FYQ", # Will Filter Data for current fy & quarter. current fy & q = today.fy() & q().
    "CURRENT_MONTH" : "CURRENT_MONTH" # Will Filter Data for current month. current month = today.month().
}


# commonTableDataPoints = ["id","fileName","fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","uploadedBy","actualUploadDate","size"]
# datePoints = ["fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","actualUploadDate"]


def jsDateStrToTimeZoneAwareDate(fileDate):
    
    # 'fileDate': '2025-02-04T18:30:00.000Z'
    # Example: A naive datetime object (without timezone)
    # naive_dt = datetime(2025, 2, 5, 12, 30, 0)  # 12:30 PM without timezone

    naive_dt = datetime.strptime(fileDate, "%Y-%m-%dT%H:%M:%S.%fZ")
    naive_dt = naive_dt + timedelta(hours = 5, minutes = 30)
    # Define the correct timezone (e.g., Asia/Kolkata)
    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timezone_aware_dt = IST.localize(naive_dt)
    return timezone_aware_dt


def getFirstDayOfMonth(dt):
    return dt.replace(day=1)

def getLastDayOfMonth(dt):
    # Move to the first day of the next month, then subtract one day
    next_month = dt.replace(day=28) + timedelta(days=4)  # This ensures we're in the next month
    return next_month.replace(day=1) - timedelta(days=1)  # Move to last day of the current month


def getFinancialYear(dt):
    if dt.month >= 4:  # Financial year starts in April
        start_year = dt.year
        end_year = dt.year + 1
    else:
        start_year = dt.year - 1
        end_year = dt.year

    return f"{start_year}-{str(end_year)[-2:]}"  # Format as "YYYY-YY"

def getFinancialYearList():
    # Get the current financial year based on today's date
    current_fy = getFinancialYear(datetime.now())
    # Extracting the year from the input financial year string
    current_year, next_year = map(int, current_fy.split('-'))
    
    fy_list = []
    for i in range(15):
        fy_list.append(f"{current_year + 1}-{current_year % 100 + 2}")
        current_year -= 1
    
    return fy_list

def getQuarter(dt):
    # Define financial quarters based on the month
    if dt.month in (4, 5, 6):
        return "Q1"
    elif dt.month in (7, 8, 9):
        return "Q2"
    elif dt.month in (10, 11, 12):
        return "Q3"
    else:  # (1, 2, 3)
        return "Q4"

def formatDateWithSuffix(dt):
    day = dt.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    return f"{day}{suffix} {dt.strftime('%B %Y')}"


def preprocessDataBeforeAddition(product, uploadPoints):

    # It expects a product object like following:
    # {'id': None,
    # 'fileName': None,
    # 'fileDate': '2025-02-04T18:30:00.000Z',
    # 'weekStartsEnds': ['2025-02-18T18:30:00.000Z', '2025-02-21T18:30:00.000Z'],
    # 'month': '2025-01-31T18:30:00.000Z',
    # 'quarter': 'Q3',
    # 'year': '2023-12-31T18:30:00.000Z',
    # 'fy': '2024-25',
    # 'fileDateFromTo': ['2025-02-19T18:30:00.000Z', None],
    # 'uploadedOn': '2025-02-04T18:30:00.000Z',
    # 'uploadedBy': None,
    # 'attachedFiles': None,
    # 'size': 0
    # }

    #commonTableDataPoints = ["id","fileName","fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","uploadedBy","actualUploadDate","size"]
    # datePoints = ["fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","actualUploadDate"]
    # See all the dataPoints in itself are self sufficient, apart from the Quarter Data. Quarter Data must be coupled with Financial Year.
    # uploadedOn and actualUploadDate are not depending on anything. By default value is datetime.now()
    # So, all should stay as single unit apart from Quarter and Year.
    # Careful about fy, it is coming as string '2023-24'
    
    timeNow = datetime.today()
    timeNow = timeNow.replace(microsecond=0)

    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timeNow = IST.localize(timeNow)

    startDateObj = timeNow
    endDateObj = timeNow
    
    fileDate = product.get("fileDate", None)
    weekStartsEnds = product.get("weekStartsEnds", None)
    month = product.get("month", None)
    quarter = product.get("quarter", None)
    year = product.get("year", None)
    fy = product.get("fy", None)
    fileDateFromTo = product.get("fileDateFromTo", None)
    uploadedOn = product.get("uploadedOn", None)
    actualUploadDate = product.get("actualUploadDate", None)
    
    # print(uploadedOn)

    
    if(fileDate):
        startDateObj = jsDateStrToTimeZoneAwareDate(fileDate)
        print(startDateObj)

        print(pd.to_datetime(fileDate))

        endDateObj = startDateObj  
    elif(weekStartsEnds):
        startDateObj = jsDateStrToTimeZoneAwareDate(weekStartsEnds[0])
        endDateObj = jsDateStrToTimeZoneAwareDate(weekStartsEnds[1])
    elif(month):
        dateObj = jsDateStrToTimeZoneAwareDate(month)
        startDateObj = getFirstDayOfMonth(dateObj)
        endDateObj = getFirstDayOfMonth(dateObj)
    elif(quarter and fy):
        quarterInfos = {
            "Q1": [0, (4, 1), (6,30)],
            "Q2": [0, (7, 1), (9, 30)],
            "Q3": [0, (10, 1), (12, 31)],
            "Q4": [1, (1, 1), (3, 31)]
        }
        quarterInfo = quarterInfos[quarter]
        startYear = int(fy.split('-')[0])
        # endYear = int(fy.split('-')[1])
        
        startDateObj = datetime(startYear + quarterInfo[0] ,quarterInfo[1][0], quarterInfo[1][1])
        endDateObj = datetime(startYear + quarterInfo[0] ,quarterInfo[2][0], quarterInfo[2][1])
        
    elif(year):
        dateObj = jsDateStrToTimeZoneAwareDate(year)
        startDateObj = dateObj.replace(day = 1, month = 1)
        endDateObj = dateObj.replace(day = 31, month = 12)
        
    elif(fy):
        startYear = int(fy.split('-')[0])
        endYear = int(fy.split('-')[1])
        startDateObj = datetime(startYear,4,1)
        endDateObj = datetime(endYear,3,31)
    elif(fileDateFromTo):
        startDateObj = jsDateStrToTimeZoneAwareDate(fileDateFromTo[0])
        endDateObj = jsDateStrToTimeZoneAwareDate(fileDateFromTo[1])
        
    product['startDateToFilter'] = startDateObj
    product['endDateToFilter'] = endDateObj
    
    product['weekStarts'] = startDateObj
    product['weekEnds'] = endDateObj
    
    product['fileDateFrom'] = startDateObj
    product['fileDateTo'] = endDateObj
    
    
    product["fileDate"] = startDateObj
    product["month"] = startDateObj
    product["year"] = startDateObj
    
    if(fy is None):
        product["fy"] = getFinancialYear(startDateObj)
    if(quarter is None):
        product["quarter"] = getQuarter(startDateObj)

    if(uploadedOn):
        product["uploadedOn"] = jsDateStrToTimeZoneAwareDate(uploadedOn)
    else:
        product["uploadedOn"] = timeNow
    
    # if(actualUploadDate):
    #     product["actualUploadDate"] = jsDateStrToTimeZoneAwareDate(actualUploadDate)
    # else:
    #     product["actualUploadDate"] = timeNow

    product["actualUploadDate"] = timeNow
    
    # It will always be this only. # Always update this one.
    product["lastUpdatedOn"] = timeNow
    
    # We don't want these following 2 to be saved in DB.
    product.pop('weekStartsEnds', None)
    product.pop('fileDateFromTo', None)
    product.pop('attachedFiles', None)
    
    # print(product)
    # print("Done")

    # The final product will look like:
    # {'id': None,
    # 'fileName': None,
    # 'fileDate': datetime.datetime(2025, 2, 4, 18, 30),
    # 'month': datetime.datetime(2025, 2, 4, 18, 30),
    # 'quarter': 'Q3',
    # 'year': datetime.datetime(2025, 2, 4, 18, 30),
    # 'fy': '2024-25',
    # 'uploadedOn': datetime.datetime(2025, 2, 4, 18, 30),
    # 'uploadedBy': None,
    # 'actualUploadDate': datetime.datetime(2025, 2, 5, 20, 31, 41),
    # 'size': 0,
    # 'startDateToFilter': datetime.datetime(2025, 2, 4, 18, 30),
    # 'endDateToFilter': datetime.datetime(2025, 2, 4, 18, 30),
    # 'weekStarts': datetime.datetime(2025, 2, 4, 18, 30),
    # 'weekEnds': datetime.datetime(2025, 2, 4, 18, 30),
    # 'fileDateFrom': datetime.datetime(2025, 2, 4, 18, 30),
    # 'fileDateTo': datetime.datetime(2025, 2, 4, 18, 30)}

    # See how few attributes are changed for better filtering/sorting of data.
    

def preprocessDataBeforeUpdate(product, uploadPoints):

    # It expects a product object like following:
    # {'id': None,
    # 'fileName': None,
    # 'fileDate': '2025-02-04T18:30:00.000Z',
    # 'weekStartsEnds': ['2025-02-18T18:30:00.000Z', '2025-02-21T18:30:00.000Z'],
    # 'month': '2025-01-31T18:30:00.000Z',
    # 'quarter': 'Q3',
    # 'year': '2023-12-31T18:30:00.000Z',
    # 'fy': '2024-25',
    # 'fileDateFromTo': ['2025-02-19T18:30:00.000Z', None],
    # 'uploadedOn': '2025-02-04T18:30:00.000Z',
    # 'uploadedBy': None,
    # 'attachedFiles': None,
    # 'size': 0
    # }

    # Expects uploadPoints: {'fileDate': True, 'uploadedOn': True}

    #commonTableDataPoints = ["id","fileName","fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","uploadedBy","actualUploadDate","size"]
    # datePoints = ["fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","actualUploadDate"]
    # See all the dataPoints in itself are self sufficient, apart from the Quarter Data. Quarter Data must be coupled with Financial Year.
    # uploadedOn and actualUploadDate are not depending on anything. By default value is datetime.now()
    # So, all should stay as single unit apart from Quarter and Year.
    # Careful about fy, it is coming as string '2023-24'
    
    timeNow = datetime.today()
    timeNow = timeNow.replace(microsecond=0)

    IST = pytz.timezone("Asia/Kolkata")
    # Localize the naive datetime to IST
    timeNow = IST.localize(timeNow)

    startDateObj = timeNow
    endDateObj = timeNow
    
    if(uploadPoints.get("fileDate", True)):
        fileDate = product.get("fileDate", None)
    else:
        fileDate = None
    if(uploadPoints.get("weekStartsEnds", True)):
        weekStartsEnds = product.get("weekStartsEnds", None)
    else:
        weekStartsEnds = None
    if(uploadPoints.get("month", True)):
        month = product.get("month", None)
    else:
        month = None    
    if(uploadPoints.get("quarter", True)):
        quarter = product.get("quarter", None)
    else:
        quarter = None   
    if(uploadPoints.get("year", True)):
        year = product.get("year", None)
    else:
        year = None   
    if(uploadPoints.get("fy", True)):
        fy = product.get("fy", None)
    else:
        fy = None   
    if(uploadPoints.get("fileDateFromTo", True)):
        fileDateFromTo = product.get("fileDateFromTo", None)
    else:
        fileDateFromTo = None 
    if(uploadPoints.get("uploadedOn", True)):
        uploadedOn = product.get("uploadedOn", None)
    else:
        uploadedOn = None
    
    if(fileDate):
        startDateObj = jsDateStrToTimeZoneAwareDate(fileDate)
        print(startDateObj)

        print(pd.to_datetime(fileDate))

        endDateObj = startDateObj  
    elif(weekStartsEnds):
        startDateObj = jsDateStrToTimeZoneAwareDate(weekStartsEnds[0])
        endDateObj = jsDateStrToTimeZoneAwareDate(weekStartsEnds[1])
    elif(month):
        dateObj = jsDateStrToTimeZoneAwareDate(month)
        startDateObj = getFirstDayOfMonth(dateObj)
        endDateObj = getFirstDayOfMonth(dateObj)
    elif(quarter and fy):
        quarterInfos = {
            "Q1": [0, (4, 1), (6,30)],
            "Q2": [0, (7, 1), (9, 30)],
            "Q3": [0, (10, 1), (12, 31)],
            "Q4": [1, (1, 1), (3, 31)]
        }
        quarterInfo = quarterInfos[quarter]
        startYear = int(fy.split('-')[0])
        # endYear = int(fy.split('-')[1])
        
        startDateObj = datetime(startYear + quarterInfo[0] ,quarterInfo[1][0], quarterInfo[1][1])
        endDateObj = datetime(startYear + quarterInfo[0] ,quarterInfo[2][0], quarterInfo[2][1])
        
    elif(year):
        dateObj = jsDateStrToTimeZoneAwareDate(year)
        startDateObj = dateObj.replace(day = 1, month = 1)
        endDateObj = dateObj.replace(day = 31, month = 12)
        
    elif(fy):
        startYear = int(fy.split('-')[0])
        endYear = int(fy.split('-')[1])
        startDateObj = datetime(startYear,4,1)
        endDateObj = datetime(endYear,3,31)
    elif(fileDateFromTo):
        startDateObj = jsDateStrToTimeZoneAwareDate(fileDateFromTo[0])
        endDateObj = jsDateStrToTimeZoneAwareDate(fileDateFromTo[1])
        
    product['startDateToFilter'] = startDateObj
    product['endDateToFilter'] = endDateObj
    
    product['weekStarts'] = startDateObj
    product['weekEnds'] = endDateObj
    
    product['fileDateFrom'] = startDateObj
    product['fileDateTo'] = endDateObj
    
    
    product["fileDate"] = startDateObj
    product["month"] = startDateObj
    product["year"] = startDateObj
    
    
    product["fy"] = getFinancialYear(startDateObj)
    product["quarter"] = getQuarter(startDateObj)

    if(uploadedOn):
        product["uploadedOn"] = jsDateStrToTimeZoneAwareDate(uploadedOn)
    else:
        product["uploadedOn"] = timeNow
    
    # It will always be this only. # Always update this one.
    product["lastUpdatedOn"] = timeNow
    
    # We don't want these following 2 to be saved in DB.
    product.pop('weekStartsEnds', None)
    product.pop('fileDateFromTo', None)
    product.pop('attachedFiles', None)
    
    # print(product)
    # print("Done")

    # The final product will look like:
    # {'id': None,
    # 'fileName': None,
    # 'fileDate': datetime.datetime(2025, 2, 4, 18, 30),
    # 'month': datetime.datetime(2025, 2, 4, 18, 30),
    # 'quarter': 'Q3',
    # 'year': datetime.datetime(2025, 2, 4, 18, 30),
    # 'fy': '2024-25',
    # 'uploadedOn': datetime.datetime(2025, 2, 4, 18, 30),
    # 'uploadedBy': None,
    # 'actualUploadDate': datetime.datetime(2025, 2, 5, 20, 31, 41),
    # 'size': 0,
    # 'startDateToFilter': datetime.datetime(2025, 2, 4, 18, 30),
    # 'endDateToFilter': datetime.datetime(2025, 2, 4, 18, 30),
    # 'weekStarts': datetime.datetime(2025, 2, 4, 18, 30),
    # 'weekEnds': datetime.datetime(2025, 2, 4, 18, 30),
    # 'fileDateFrom': datetime.datetime(2025, 2, 4, 18, 30),
    # 'fileDateTo': datetime.datetime(2025, 2, 4, 18, 30)}

    # See how few attributes are changed for better filtering/sorting of data.



def getQueryRange(filterOptions):
    # filterOptions looks like:
    # {'filterBy': 'Date Range', 'filterRange': None or [None, None], 'filterFY': None, 'filterQuarter': None, 'defaultFiltering': 'CURRENT_YEAR'}
    
    print(filterOptions)

    filterBy = filterOptions["filterBy"]
    filterRange = filterOptions["filterRange"]
    filterFY = filterOptions["filterFY"]
    filterQuarter = filterOptions["filterQuarter"]
    defaultFiltering = filterOptions["defaultFiltering"]
 
    # print(defaultFiltering)
    # print(DEFAULT_FILTERS["CURRENT_YEAR"])


    if((filterBy is None) or ((filterRange is None) and (filterFY is None) and (filterQuarter is None))):
        # Then simply check defaultFiltering.
        startDateObj = None
        endDateObj = None

        if(defaultFiltering is None):
            return None, None
        elif(defaultFiltering == DEFAULT_FILTERS["LAST_ONE_YEAR"]):
            # Get today's date
            endDateObj = datetime.today()
            # Get the date one year back
            startDateObj = endDateObj - timedelta(days = 365)

            startDateObj = startDateObj.replace(hour=0,minute=0,second=0,microsecond=0)
            endDateObj = endDateObj.replace(hour=0,minute=0,second=0,microsecond=0)

        elif(defaultFiltering == DEFAULT_FILTERS["CURRENT_YEAR"]):
            # Get today's date
            endDateObj = datetime.today()
            # Get the date one year back
            startDateObj = endDateObj.replace(day=1,month=1,hour=0,minute=0,second=0,microsecond=0)
            endDateObj = endDateObj.replace(day=31,month=12,hour=0,minute=0,second=0,microsecond=0)
        
        elif(defaultFiltering == DEFAULT_FILTERS["CURRENT_FINANCIAL_YEAR"]):
            dt = datetime.today()

            year = dt.year
            # Financial year starts from April 1st
            if dt.month >= 4:  # If it's April or later, current FY started this year
                startDateObj = datetime(year, 4, 1)
                endDateObj = datetime(year + 1, 3, 31)
            else:  # If it's Jan-March, current FY started last year
                startDateObj = datetime(year - 1, 4, 1)
                endDateObj = datetime(year, 3, 31)

            # print(startDateObj, endDateObj)
                
        elif(defaultFiltering == DEFAULT_FILTERS["CURRENT_FYQ"]):
            dt = datetime.today()
            year = dt.year
            quarters = [
                (datetime(year, 1, 1), datetime(year, 3, 31)),   # Q4: Jan - Mar
                (datetime(year, 4, 1), datetime(year, 6, 30)),   # Q1: Apr - Jun
                (datetime(year, 7, 1), datetime(year, 9, 30)),   # Q2: Jul - Sep
                (datetime(year, 10, 1), datetime(year, 12, 31)), # Q3: Oct - Dec
            ]

            for startDate, endDate in quarters:
                if startDate <= dt <= endDate:
                    startDateObj = startDate
                    endDateObj = endDateObj
                    break

        elif(defaultFiltering == DEFAULT_FILTERS["CURRENT_MONTH"]):
            startDateObj = datetime.today()

            # First day of next month
            next_month = startDateObj.replace(day=28) + timedelta(days=4)
            days_in_month = (next_month.replace(day=1) - timedelta(days=1)).day

            endDateObj = endDateObj.replace(day = days_in_month)


        if(startDateObj is not None):
            startDateObj = startDateObj.replace(hour=0,minute=0,second=0,microsecond=0)
        if(endDateObj is not None):
            endDateObj = endDateObj.replace(hour=23,minute=59,second=59,microsecond=0)

        return startDateObj, endDateObj
    else:
        # Means filterBy is Not None. Also Atleast one of filterRange,filterFY,filterQuarter is Not None.
        # At a time only 1 can be not None.

        startDateObj = None
        endDateObj = None

        if(filterRange is not None):
            if(filterBy == "Date Range" and type(filterRange) is list):
                if(filterRange[0] is not None):
                    startDateObj = jsDateStrToTimeZoneAwareDate(filterRange[0])
                if(filterRange[1] is not None):
                    endDateObj = jsDateStrToTimeZoneAwareDate(filterRange[1])
            else:
                dateObj = jsDateStrToTimeZoneAwareDate(filterRange)
                if(filterBy == "Year"):
                    startDateObj = dateObj.replace(month = 1, day = 1)
                    endDateObj = dateObj.replace(month = 12, day = 31)
                elif(filterBy == "Month"):
                    startDateObj = dateObj.replace(day = 1)
                    # First day of next month
                    next_month = startDateObj.replace(day=28) + timedelta(days=4)
                    days_in_month = (next_month.replace(day=1) - timedelta(days=1)).day
                    endDateObj = dateObj.replace(day = days_in_month)

        else:
            # So, filterRange is None. We can have FY Filter with Quarter = None.
            # Or, we may have FY Filter with Quarter = "Q1" or "Q2" or "Q3" or "Q4".
            # FY is in string "2023-24" like this.

            if(filterFY is None):
                return None, None

            if(filterQuarter is None):
                # Return entire range of the FY.
                # Split the financial year string (e.g., "2023-24" → 2023 and 2024)
                start_year = int(filterFY.split('-')[0])
                end_year = int(start_year) + 1

                # Define the start and end dates
                startDateObj = datetime(start_year, 4, 1)  # April 1st of the start year
                endDateObj = datetime(end_year, 3, 31)     # March 31st of the end year
            else:
                # Extract the start year from the financial year string
                start_year = int(filterFY.split('-')[0])
                end_year = int(start_year) + 1
                
                # Define quarter start and end dates
                quarter_dates = {
                    "Q1": (datetime(start_year, 4, 1), datetime(start_year, 6, 30)),  # Apr - Jun
                    "Q2": (datetime(start_year, 7, 1), datetime(start_year, 9, 30)),  # Jul - Sep
                    "Q3": (datetime(start_year, 10, 1), datetime(start_year, 12, 31)), # Oct - Dec
                    "Q4": (datetime(end_year, 1, 1), datetime(end_year, 3, 31))  # Jan - Mar (next calendar year)
                }

                startDateObj, endDateObj = quarter_dates.get(filterQuarter, (None, None))  # Return None if invalid quarter
            
        if(startDateObj is not None):
            startDateObj = startDateObj.replace(hour=0,minute=0,second=0,microsecond=0)
        if(endDateObj is not None):
            endDateObj = endDateObj.replace(hour=23,minute=59,second=59,microsecond=0)

        return startDateObj, endDateObj
        


# Useful while Saving data to FileSystem.
def saveWithUniqueName(uploadFolder, file):
    os.makedirs(uploadFolder, exist_ok=True)
    fileName = file["fileName"]
    base, ext = os.path.splitext(fileName)  # Split filename and extension
    filepath = os.path.join(uploadFolder, fileName)
    counter = 1
    print(filepath)

    # Check if file exists and generate a unique name
    while os.path.exists(filepath):
        filepath = os.path.join(uploadFolder, f"{base} ({counter}){ext}")
        counter += 1

    base64_str = file["base64Data"].split(';base64')[1] # No need to worry ';' is not a valid base64 Character.
    bytes_obj = encode(base64_str, 'utf-8')
    binary_obj = base64.decodebytes(bytes_obj)

    with open(filepath, "wb") as fh:
        fh.write(binary_obj)

    return os.path.basename(filepath)  # Return saved file name