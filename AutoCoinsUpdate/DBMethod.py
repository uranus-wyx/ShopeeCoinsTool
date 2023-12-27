import logging
import MySQLdb
from ReadSpreadSheet import *
from datetime import datetime

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
