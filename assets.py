import csv
from records import Municipality
import datetime

def write_to_csv(municipality : Municipality, filename):
    print("Writing csv for " + str(municipality.city))
    data = municipality.getJsonData()
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def get_timestamp():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

def is_date(text):
    try:
        datetime.datetime.strptime(text, "%m/%d/%y")
        return True
    except ValueError:
        return False
