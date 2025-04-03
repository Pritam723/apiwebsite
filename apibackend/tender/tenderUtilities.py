
from datetime import  datetime, timedelta
# from enum import Enum
import pytz
import base64
from codecs import encode
import os



class ResponseException(Exception):
    pass



# Useful while Saving data to FileSystem.
def saveWithUniqueName(uploadFolder, file):
    print(uploadFolder)
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