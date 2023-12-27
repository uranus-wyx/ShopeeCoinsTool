#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import Tkinter as tk
import ttk
import tkMessageBox
import MySQLdb
import logging
from datetime import datetime
import time
import base64
from icon import img

_CurDateTime_ = datetime.fromtimestamp(time.time()).strftime("%Y%m%d-%H%M%S")

def InitialDebugLog():
    '''
    InitialDebugLog: Initial debug log
        Input Argu: 
            N/A
        Return: 
            N/A
    '''

    logging.basicConfig(
        filename = os.path.join(os.getcwd(), _CurDateTime_ + '_Update_Coins.log'),
        filemode = 'w', format = '%(asctime)s %(levelname)s line : %(lineno)d : %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level = logging.INFO
    )

class MySqlController():
    def __init__(self):
        self.conn = ""

    def ConnectMySqlDb(self, host, port, user_name, password, db_name):
        ''' 
        ConnectMySqlDb : Connect mysql db
            input Argu :
                host - host ip or domain name
                port - port
                user_name - user name
                password - password
                db_name - db name
            Return :
                N/A
        '''
        ##Update and insert data to database
        try:
            ##establishing the connection
            self.conn = MySQLdb.connect(host = host, port = port, user = user_name, passwd = password, charset = 'utf8', db = db_name)
            logging.info("Connect to DB.")

        except MySQLdb._exceptions.OperationalError:
            print("Connect to database failed.")
            logging.exception("Connect to database failed.")

        except:
            print("(%s:%s)" % (sys.exc_info()[0], sys.exc_info()[1]))
            logging.exception("Fail to update data in database.")

    def SendSqlCommand(self, sql_cmd):
        ''' 
        SendSqlCommand : Send sql command
            input Argu :
                sql_cmd - sql command
            Return :
                sql response result
        '''
        ##Update and insert data to database
        try:
            ##Creating a cursor object using the cursor() method
            cursor = self.conn.cursor()

            ##Execute sql command
            cursor.execute(sql_cmd)

            ##Commit
            self.conn.commit()

            ##return sql result
            return cursor.fetchall()

        except MySQLdb._exceptions.OperationalError:
            print("Connect to database failed.")
            logging.exception("Connect to database failed.")

        except:
            print("(%s:%s)" % (sys.exc_info()[0], sys.exc_info()[1]))
            logging.exception("Fail to update data in database.")

def UserOwnCoinsInDB(data_list):
    ''' 
    UserOwnCoinsInDB : Send sql command
        input Argu :
            data_list - data list
        Return : 
            N/A
    '''

    logging.info("---Start analysis data---")
    for user_id, coins_amount in data_list:
        
        try:

            logging.info("user_id: " + user_id)
            logging.info("coins_amount: " + coins_amount)

            ##Prepare part of user id to get database index (example: 123456789, you will get "6", "6" is this user coins saved DB index)
            coins_db_index = int(user_id[-4:-3])

            ##Prepare part of user id to get db table index (example: 123456789, you will get "6789", "6789" is this user coins saved DB table index)
            coins_table_index = user_id[-4:]

            if 0 <= coins_db_index <= 2:
                host_channel = "00"
            elif 3 <= coins_db_index <= 5:
                host_channel = "01"
            else:
                host_channel = "02"

            ##Connect to db host and it table
            mysql_controller = MySqlController()

            mysql_controller.ConnectMySqlDb(
                host="master.shopee_coins_" + host_channel + ".mysql.cloud.staging.shopee.io",
                port=6606, user_name="shopee_stag_all3",
                password="CZhBIu_2XAUALOGzsH2o",
                db_name="shopee_coins_v2_db_0000000" + str(coins_db_index)
                )

            coins_amount = int(coins_amount)
            ##Prepare update user all voucher status to disable sql command
            sql_cmd = "UPDATE `shopee_coins_v2_db_0000000%s`.`coin_v2_tab_0000%s` SET available_amount= '%s' WHERE userid = %s" % (coins_db_index,coins_table_index,coins_amount,user_id)
            logging.info("sql_cmd: %s" % sql_cmd)

            ##Execute sql command
            mysql_controller.SendSqlCommand(sql_cmd)
            print(user_id + " Update Successful")
            logging.info("---Success---")

        except:
            print("user_id: " + user_id + " Update Failed")
            print("(%s:%s)" % (sys.exc_info()[0], sys.exc_info()[1]))
            logging.error("Please check user ID: %s"  %user_id)
            logging.exception(sys.exc_info()[0])

    print("---Complete Update Coins---")

def UpdateCoins():

    data_list =[]
    country = country_list.get()
    user_id = entry_user_id.get()
    coins_amount = entry_coins_amount.get()

    result = tkMessageBox.askokcancel(title = "", message="Country: {}, User ID: {}, Coins Amount: {} ".format(country, user_id, coins_amount))
    
    if result:
        logging.info("Click Confirm Button")

        if country == "":
            tkMessageBox.showerror(title="Error", message="Please choose country")
            print("Please choose country")
            logging.info("Please choose country")
        
        else:
            if coins_amount:
                ##For VN, available_amount rate is 1:100 ; Example:If available_amount is 30 then coins will be 3000
                if country == "VN":
                    print("For VN, coins rate is 1:100")
                    print("Enter Coins: {}".format(coins_amount))
                    coins_amount = int(coins_amount) / 100
                    coins_amount = str(coins_amount)
                    logging.info("For VN, coins rate is 1:100, calculating = {}".format(coins_amount))
                    print("Calculating Coins: {}".format(coins_amount))

                elif country in ("PH","TH","TW"):
                    print("For PH, TH, TW, coins rate is 1:0.01")
                    print("Enter Coins: {}".format(coins_amount))
                    coins_amount = int(coins_amount) * 100
                    coins_amount = str(coins_amount)
                    logging.info("For PH, TH, TW, coins rate is 1:0.01, calculating = {}".format(coins_amount))
                    print("Calculating Coins: {}".format(coins_amount))
                else:
                    logging.info("Other country, coins rate is 1:1, calculating = {}".format(coins_amount))
                    print("Other country, coins rate is 1:1")
                    print("Enter Coins: {}".format(coins_amount))
                    print("Calculating Coins: {}".format(coins_amount))

            data_list.append((user_id, coins_amount))

            try:
                if str.isdigit(user_id) and int(coins_amount) > 0:
                    UserOwnCoinsInDB(data_list)
                    tkMessageBox.showinfo(title="Complete", message="Country: {}, User ID: {}, Coins Amount: {} ".format(country, user_id, entry_coins_amount.get()))
                    print("Country: {}, User ID: {}, Coins Amount: {} ".format(country, user_id, entry_coins_amount.get()))
                    logging.info("Country: {}, User ID: {}, Coins Amount: {} ".format(country, user_id, entry_coins_amount.get()))
                    print("=====Done=====")
                
                elif country in ("VN") and int(coins_amount) <= 0:
                    tkMessageBox.showerror(title="Error", message="For VN rate 1:100, Coins amount must larger than 100")
                    print("For VN rate 1:100, Coins amount must larger than 100")
                    logging.info("For VN rate 1:100, Coins amount must larger than 100")
                
                elif country not in ("VN") and int(coins_amount) <= 0:
                    tkMessageBox.showerror(title="Error", message="Coins amount must larger than 0")
                    print("Coins amount must larger than 0")
                    logging.info("Coins amount must larger than 0")

                elif str.isdigit(user_id) == False:
                    tkMessageBox.showerror(title="Error", message="User ID must be digit")
                    print("User ID must be digit")
                    logging.info("User ID must be digit")
                
                else:
                    tkMessageBox.showerror(title="Error", message="Something wrong!!")
                    print("Failed to update coins amount")
                    logging.exception("Failed to update coins amount")

            except:
                tkMessageBox.showerror(title="Error", message="Something wrong!!")
                print("Failed to update coins amount")
                logging.exception("Failed to update coins amount")
    else:
        logging.info("Click cancel button")

window = tk.Tk()
window.title('Update Shopee Coins')
#fix the window size
window.resizable(False, False)
#get the width of current window
windowWidth = 500
#get the height of current window
windowHeight = 300
#get the width and height of the screen
screenWidth,screenHeight = window.maxsize()
geometryParam = '%dx%d+%d+%d'%(windowWidth, windowHeight, (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)
window.geometry(geometryParam)

#change icon
tmp = open("tmp.ico","wb+")
tmp.write(base64.b64decode(img))
tmp.close()
window.iconbitmap("tmp.ico")
os.remove("tmp.ico")

#build the label
label = tk.Label(window,                 #which window
                 text = 'Update Coins Amount',
                 bg = '#EEBB00',         #background color
                 font = ('Arial', 12),   #font and size
                 width = 32, height = 2) #label size

label_country = tk.Label(window,          
                 text = 'Country', 
                 font = ('Arial', 10),   
                 width = 15, height = 2)

label_user_id = tk.Label(window,
                 text = 'User ID', 
                 font = ('Arial', 10),
                 width = 15, height = 2)

label_coins_amount = tk.Label(window,
                 text = 'Coins Amount', 
                 font = ('Arial', 10),
                 width = 15, height = 2)

#build list
# user_id_list = ttk.Combobox(window, 
#                             values=[101746025,101703546,101746023], 
#                             height = 10)
# user_id_list.current(1)

#build a button
button = tk.Button(window,           #which window
                   text = 'Update',  #text display
                   command = UpdateCoins) #execute command

#enter value section
country_list = ttk.Combobox(window, 
                            values=["AR","BR","CL","CO","ES","ID","MX","MY","PH","PL","TH","TW","VN"], 
                            height = 10)

entry_user_id = tk.Entry(window,     
                 width = 20) 

entry_coins_amount = tk.Entry(window,   
                 width = 20)

#Place the element
label.pack()
label_country.pack()
country_list.pack()
label_user_id.pack()
##user_id_list.pack()
entry_user_id.pack()
label_coins_amount.pack()
entry_coins_amount.pack()
button.pack()

def OpenWindow():
    ##Initial debug log for this tool
    InitialDebugLog()
    logging.info("===Start Update Coins===")
    window.mainloop()
    logging.info("===Finish Update Coins===")

if __name__ == '__main__':
    OpenWindow()