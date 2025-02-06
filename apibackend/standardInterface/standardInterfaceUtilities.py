from datetime import  datetime, timedelta

commonTableDataPoints = ["id","fileName","fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","uploadedBy","actualUploadDate","size"]
datePoints = ["fileDate","weekStartsEnds","month","quarter","year","fy","fileDateFromTo","uploadedOn","actualUploadDate"]
quarterInfos = {
    "Q1": [0, (4, 1), (6,30)],
    "Q2": [0, (7, 1), (9, 30)],
    "Q3": [0, (10, 1), (12, 31)],
    "Q4": [1, (1, 1), (3, 31)]
}


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


def preprocessData(product):

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
    # 'actualUploadDate': None,
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
        startDateObj = datetime.strptime(fileDate, "%Y-%m-%dT%H:%M:%S.%fZ")
        endDateObj = startDateObj  
    elif(weekStartsEnds):
        startDateObj = datetime.strptime(weekStartsEnds[0], "%Y-%m-%dT%H:%M:%S.%fZ")
        endDateObj = datetime.strptime(weekStartsEnds[1], "%Y-%m-%dT%H:%M:%S.%fZ")
    elif(month):
        dateObj = datetime.strptime(month, "%Y-%m-%dT%H:%M:%S.%fZ")
        startDateObj = getFirstDayOfMonth(dateObj)
        endDateObj = getFirstDayOfMonth(dateObj)
    elif(quarter and fy):
        
        quarterInfo = quarterInfos[quarter]
        startYear = int(fy.split('-')[0])
        # endYear = int(fy.split('-')[1])
        
        startDateObj = datetime(startYear + quarterInfo[0] ,quarterInfo[1][0], quarterInfo[1][1])
        endDateObj = datetime(startYear + quarterInfo[0] ,quarterInfo[2][0], quarterInfo[2][1])
        
    elif(year):
        dateObj = datetime.strptime(year, "%Y-%m-%dT%H:%M:%S.%fZ")
        startDateObj = dateObj.replace(day = 1, month = 1)
        endDateObj = dateObj.replace(day = 31, month = 12)
        
    elif(fy):
        startYear = int(fy.split('-')[0])
        endYear = int(fy.split('-')[1])
        startDateObj = datetime(startYear,4,1)
        endDateObj = datetime(endYear,3,31)
    elif(fileDateFromTo):
        startDateObj = datetime.strptime(fileDateFromTo[0], "%Y-%m-%dT%H:%M:%S.%fZ")
        endDateObj = datetime.strptime(fileDateFromTo[1], "%Y-%m-%dT%H:%M:%S.%fZ")
        
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
        product["uploadedOn"] = datetime.strptime(uploadedOn, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        product["uploadedOn"] = timeNow
    
    product["actualUploadDate"] = timeNow
    
    
    
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
    

