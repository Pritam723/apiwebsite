def getJSCompatibleTimeStamp(dt):
    if(dt is None): return None
    return int(dt.timestamp() * 1000)