# -*- coding: utf-8 -*
import os
import sys
import datetime
from datetime import datetime
import time
import shutil
sys.path.append('../')

import logging
from ReadSpreadSheet import *
from DBMethod import *

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

def MoveDebugLogToDs07():
    '''
    MoveDebugLogToDs07: Move debug log to ds07
        Input Argu: 
            N/A
        Return: 
            N/A
    '''
    dst_folder = r"\\ds07\1_Department\Marketplace - QA\AutoLogs\AutoUpdateCoinsAmount"

    ##Check if log folder exists
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    shutil.copy2(_CurDateTime_ + '_Update_Coins.log', dst_folder)

if __name__ == '__main__':

    ##Initial debug log for this tool
    InitialDebugLog()
    logging.info("===Start Update Coins===")

    ##Read sheet data
    update_data = ReadGoogleSheet('AUTO')

    ##Get data to list
    data_list = GetSheetDataToList(update_data)

    ##Change user coins in DB
    UserOwnCoinsInDB(data_list)

    ##Move debug log to DS07
    MoveDebugLogToDs07()

    logging.info("===Complete Update Coins===")
