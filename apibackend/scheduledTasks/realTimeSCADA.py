# import datetime
# import requests
# import os
# import pandas as pd

# def format_datetime(dt):
#     # Get the day with ordinal suffix (st, nd, rd, th)
#     day = dt.day
#     suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
#     # Handle Windows/Linux formatting for day
#     day_str = f"{day}{suffix}"

#     # Format the date and time
#     formatted_time = dt.strftime(f"%b %I:%M:%S %p")  # Format without day
#     return f"{day_str} {formatted_time}"  # Manually add day at the beginning


# def getSCADADATA():
#     try:
#         network_path = r"\\10.3.200.53\scada\Documents\er_data1.txt"

#         # Get last modified timestamp
#         timestamp = os.path.getmtime(network_path)

#         # Convert to datetime object
#         dt = datetime.datetime.fromtimestamp(timestamp)

#         df = pd.read_csv(network_path, header=None, index_col=0)

#         LAST_UPDATED = format_datetime(dt)
#         ER_DEMAND_MET = round(float(df.loc["ER_DEMAND_EWEB"][1]),2)
#         SCED_REV = int(df.loc["WBES_SCHEDREV_EWEB"][1])
#         ER_FREQ = round(float(df.loc["ER_FREQ_EWEB"][1]),2)

#         data = {"LAST_UPDATED" : LAST_UPDATED, "ER_DEMAND_MET" : ER_DEMAND_MET, "SCED_REV": SCED_REV, "ER_FREQ": ER_FREQ}

#         return(data)



#     except Exception as e:
#         data = { "LAST_UPDATED": "NOT ABLE TO REACH SERVER", "ER_DEMAND_MET": 0, "SCED_REV": -1, "ER_FREQ": 0}
#         return data
    
    
# if __name__ == "__main__":
#     url = "http://10.3.101.179:4001/testSocket"  # Update with your actual Flask server URL

#     data = getSCADADATA()

#     response = requests.post(url, json=data)

#     # Send POST request

#     # Print response from server
#     # print("Status Code:", response.status_code)
#     # print("Response:", response.text)