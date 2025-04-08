from datetime import datetime

def getDatetime():
    #Grabs current datetime
    current_datetime = datetime.now()

    #Formats the datetime into Year-Month-Day Hour-Min-Sec
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_datetime