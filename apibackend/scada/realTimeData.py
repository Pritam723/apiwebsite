from flask import jsonify

import datetime
import requests
import os
import pandas as pd

def format_datetime(dt):
    # Get the day with ordinal suffix (st, nd, rd, th)
    day = dt.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    
    # Handle Windows/Linux formatting for day
    day_str = f"{day}{suffix}"

    # Format the date and time
    formatted_time = dt.strftime(f"%b %I:%M:%S %p")  # Format without day
    return f"{day_str} {formatted_time}"  # Manually add day at the beginning

def realTimeSCADAData():

    try:
        # m = 0/0
        network_path = r"\\10.3.200.53\scada\Documents\\er_data1.txt"

        # Get last modified timestamp
        timestamp = os.path.getmtime(network_path)

        # Convert to datetime object
        dt = datetime.datetime.fromtimestamp(timestamp)

        df = pd.read_csv(network_path, header=None, index_col=0)

        LAST_UPDATED = format_datetime(dt)
        ER_DEMAND_MET = round(float(df.loc["ER_DEMAND_EWEB"][1]),2)
        SCED_REV = int(df.loc["WBES_SCHEDREV_EWEB"][1])
        ER_FREQ = round(float(df.loc["ER_FREQ_EWEB"][1]),2)

        WB_DEMAND_EWEB = round(float(df.loc["WB_DEMAND_EWEB"][1]),2)
        BH_DEMAND_EWEB = round(float(df.loc["BH_DEMAND_EWEB"][1]),2)
        JH_DEMAND_EWEB = round(float(df.loc["JH_DEMAND_EWEB"][1]),2)
        OD_DEMAND_EWEB = round(float(df.loc["OD_DEMAND_EWEB"][1]),2)
        SI_DEMAND_EWEB = round(float(df.loc["SI_DEMAND_EWEB"][1]),2)
        DVC_DEMAND_EWEB = round(float(df.loc["DVC_DEMAND_EWEB"][1]),2)


        WB_DRAWL_SCHEDULE_EWEB = round(float(df.loc["WB_DRAWL_SCHEDULE_EWEB"][1]),2)
        BH_DRAWL_SCHEDULE_EWEB = round(float(df.loc["BH_DRAWL_SCHEDULE_EWEB"][1]),2)
        JH_DRAWL_SCHEDULE_EWEB = round(float(df.loc["JH_DRAWL_SCHEDULE_EWEB"][1]),2)
        OD_DRAWL_SCHEDULE_EWEB = round(float(df.loc["OD_DRAWL_SCHEDULE_EWEB"][1]),2)
        SI_DRAWL_SCHEDULE_EWEB = round(float(df.loc["SI_DRAWL_SCHEDULE_EWEB"][1]),2)
        DVC_DRAWL_SCHEDULE_EWEB = round(float(df.loc["DVC_DRAWL_SCHEDULE_EWEB"][1]),2)


        data = {"counterData" : {"LAST_UPDATED" : LAST_UPDATED, "ER_DEMAND_MET" : ER_DEMAND_MET, "SCED_REV": SCED_REV, "ER_FREQ": ER_FREQ},
                "demandData": {"LAST_UPDATED" : LAST_UPDATED,"WB": WB_DEMAND_EWEB, "BH": BH_DEMAND_EWEB, "JH": JH_DEMAND_EWEB, "OD": OD_DEMAND_EWEB, "SI": SI_DEMAND_EWEB, "DVC": DVC_DEMAND_EWEB},
                "drawlData": {"LAST_UPDATED" : LAST_UPDATED,"WB": WB_DRAWL_SCHEDULE_EWEB, "BH": BH_DRAWL_SCHEDULE_EWEB, "JH": JH_DRAWL_SCHEDULE_EWEB, "OD": OD_DRAWL_SCHEDULE_EWEB, "SI": SI_DRAWL_SCHEDULE_EWEB, "DVC": DVC_DRAWL_SCHEDULE_EWEB}}

        return jsonify(data)
            
    except Exception as e:
    
        data = {"counterData" : { "LAST_UPDATED": "NOT ABLE TO REACH SERVER", "ER_DEMAND_MET": 0, "SCED_REV": -1, "ER_FREQ": 0},
                        "demandData": {"LAST_UPDATED": "NOT ABLE TO REACH SERVER", "WB": 0, "BH": 0, "JH": 0, "OD": 0, "SI": 0, "DVC": 0},
                        "drawlData": {"LAST_UPDATED": "NOT ABLE TO REACH SERVER", "WB": 0, "BH": 0, "JH": 0, "OD": 0, "SI": 0, "DVC": 0}}

        return jsonify(data)