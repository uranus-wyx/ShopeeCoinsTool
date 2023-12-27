# -*- coding: utf-8 -*
import sys
import gspread
import logging
import datetime
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from oauth2client.service_account import ServiceAccountCredentials

##access to google sheets and return all values
def get_credentials(spreadsheet_name):
    """
    get_credentials: get google credentials
        Input Argu: 
                spreadsheet_name - AUTO
            Return:
                N/A
    """
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        logging.info("Get google sheet authorization.")
        spreadsheet = client.open(spreadsheet_name)
        logging.info("Open google sheet.")
        print("Open google sheet")

        return spreadsheet
    except:
        logging.exception("Failed to get spread sheet.")
        print("Failed to get spread sheet")

##Read rows in sheets
def ReadGoogleSheet(sheet_name):
    """
    ReadGoogleSheet: read google sheet
        Input Argu: 
                sheet_name - [Auto] Coins update 
                (https://docs.google.com/spreadsheets/d/1vASv7vq5Jc2CGs9Rj0szFxkGoh5VSrrpkTvkEJCAkd4/edit?usp=sharing)
            Return: 
                data rows
    """
    try:
        sheet = get_credentials('[Auto] Coins update').worksheet(sheet_name)
        logging.info("Open spreadsheet.")
        rows = sheet.get_all_values()
        logging.info("Get all values.")
        logging.info("Total data has %s rows" %len(rows))
        return rows
    except:
        logging.exception("Cannot access to sheet values.")

def GetSheetDataToList(update_data):
    """
    GetSheetDataToList: get data from google sheet
        Input Argu: 
                update_data - rows return from ReadGoogleSheet
            Return: 
                N/A
    """
    update_data = update_data[2:]

    data_list = []

    for data in update_data:

        if "" in data[0:6]:
            logging.info("Field %s is blank." % data[0:6])
            continue
        
        if data[0] == "VN":
            data[3] = int(data[3])/100
            data[3] = str(data[3])
        
        if data[0] in ("PH","TH","TW"):
            data[3] = int(data[3])*100
            data[3] = str(data[3])

        data_list.append((data[2],data[3]))
        logging.info("Country: %s, User: %s, Coins Amount: %s" % (data[0],data[2],data[3]))

    print("Complete get update data into list")
    logging.info("Complete get update data into list")

    return data_list