import os 
import shutil
import os
from dotenv import load_dotenv
import shutil
import os
from datetime import datetime, timedelta
import pytz
import psycopg2
from psycopg2 import sql
import uuid

def jsDateStrToTimeZoneAwareDate(fileDate):
    return fileDate

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
    

def preprocessDataBeforeAddition(product):

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
    
    # # print(uploadedOn)

    
    if(fileDate):
        startDateObj = jsDateStrToTimeZoneAwareDate(fileDate)
        # # print(startDateObj)

        # # print(pd.to_datetime(fileDate))

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
        # 2023-24
        startYear = int(fy.split('-')[0])

        endYear = startYear + 1
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
    
    # # print(product)
    # # print("Done")

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
    


def pushToDB(targetClass, dest_path_db, currentUser, dest_fileName, now, previous_date, fileSize, DB_PARAMS):
    try:
        product =  {'id': None,
        'fileName': None,
        'fileDate': None,
        'weekStartsEnds': None,
        'month': None,
        'quarter': None,
        'year': None,
        'fy': None,
        'fileDateFromTo': None,
        'uploadedOn': None,
        'uploadedBy': None,
        'attachedFiles': None,
        'size': 0
       }
        
        #################### Change Parsing Logic Here ##############################

        product["fileDate"] = previous_date
        product["uploadedOn"] = now

        ################### Parsing Logic Ends here ################################

        preprocessDataBeforeAddition(product)

        filePath = f"\{dest_path_db}\{dest_fileName}"

        # product["id"] = "56599ebb-585a-4be1-af2c-6208f70e1dd4"
        # id will be auto generated uuid

        product["fileName"] = dest_fileName
        product["size"] = fileSize
        product["uploadedBy"] = currentUser
        product["isMigrated"] = False
        product["isDeleted"] = False
        product["filePath"] = filePath
        # Generate a UUID for the 'id' field
        product["id"] = str(uuid.uuid4())  # Convert UUID to string


        print(product)




        # Delete existing record with same fileDate
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            cur = conn.cursor()

            # delete_query = sql.SQL("""
            #     DELETE FROM {} WHERE fileDate = %s
            # """).format(sql.Identifier(targetClass))


            delete_query = sql.SQL("""
                DELETE FROM {table} WHERE {column} = %s
            """).format(
                table=sql.Identifier(targetClass),
                column=sql.Identifier('fileDate')
            )




            cur.execute(delete_query, [product["fileDate"]])
            conn.commit()
        except Exception as e:
            print("Error deleting existing record:", e)
            # Optionally: raise e or continue
        finally:
            cur.close()
            conn.close()

        # return

        ################ Insert into table #############################

        # Remove 'id' from insertion as it should be auto-generated
        columns = [key for key in product.keys()]
        values = [product[key] for key in columns]



        # Create query dynamically
        # Create SQL query dynamically
        query = sql.SQL("""
            INSERT INTO {} ({}) VALUES ({})
        """).format(
            sql.Identifier(targetClass),
            sql.SQL(", ").join(map(sql.Identifier, columns)),
            sql.SQL(", ").join(sql.Placeholder() * len(values))
        )


        # Connect to DB and execute the query
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            # print("Record inserted successfully")
            cur.close()
            conn.close()
        except Exception as e:
            print("Error inserting record:", e)
            # pass

    except Exception as e:
        print(e)
        # # print(data)
        # errorEntries.append((e,data))





####################################### Entry Point of the Script ################################################################

currentUser = "00091"
targetClass = "GenerationOutage"    
dest_path_db = "Reports\Daily Report\Generation Outage"

# Get the current working directory
current_dir = os.getcwd()

# Move one level up to reach the project root
env_path = os.path.abspath(os.path.join(current_dir, '..', '.env'))

# Load the .env file
load_dotenv(dotenv_path=env_path)

# Access your environment variables
dbname = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")

DB_PARAMS = {
    "dbname": dbname,
    "user": user,
    "password": password,
    "host": host,
    "port": port,  # Default PostgreSQL port
}



now = datetime.now()
# now = datetime.datetime(2020, 6, 1) #Testing edge cases/month end

previous_date = now - timedelta(days=1)

# print(now.year,now.year%100, str(now.month).zfill(2), str(now.day).zfill(2), now.hour, now.minute, now.second)
# print(previous_date.year,previous_date.year%100, str(previous_date.month).zfill(2), str(previous_date.day).zfill(2), previous_date.hour, previous_date.minute, previous_date.second)


now = now.replace(microsecond = 0, minute = 0, hour = 0, second = 0)
previous_date = previous_date.replace(microsecond = 0, minute = 0, hour = 0, second = 0)

# print(now)

# print(previous_date)



datetime_object = datetime.strptime(str(previous_date.month), "%m")
month_name = datetime_object.strftime("%b")
print((month_name))

folderName = f"{str(previous_date.year)}/{str(previous_date.month).zfill(2)} {month_name}'{str(previous_date.year)[2:]}"

# src_fileName = f"ER_Power Supply Position Report_{previous_date.strftime('%d%m%Y')}.pdf"
# dest_fileName = f"Power Supply Position Report_{previous_date.strftime('%d%m%Y')}.pdf"

src_fileName = 'ER-NPMC-{}-{}-{}.pdf'.format(str(previous_date.day).zfill(2),month_name,previous_date.year)
dest_fileName = 'ER-NPMC-{}-{}-{}.pdf'.format(str(previous_date.day).zfill(2),month_name,previous_date.year)

print(src_fileName)
print(dest_fileName)

year = previous_date.strftime("%Y")            # '2025'
month_display = previous_date.strftime("%m %b'%y")  # '04 Apr'25'


# Original network path (double backslashes OR raw string)
source = "\\\\10.3.100.24\\HTTP-Access\\Control_Room_Report\\NPMC\\{}\\{}\\".format(year, month_display) + src_fileName

fileSize = os.path.getsize(source) # In Bytes.

# Destination filename (rename while copying)
# destination = os.path.join(os.getcwd(), dest_fileName)


project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))

# Destination folder
destination_dir = os.path.join(
    project_root,
    "uploads", "Reports", "Daily Report", "Generation Outage"
)

# Ensure the folder exists
os.makedirs(destination_dir, exist_ok=True)

destination = os.path.join(destination_dir, dest_fileName)

# Perform the copy
shutil.copy2(source, destination)

print(f"Copied and renamed to: {destination}")


pushToDB(targetClass, dest_path_db, currentUser, dest_fileName, now, previous_date, fileSize, DB_PARAMS)


print("Done...")