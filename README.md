# Shopee
#### Designed a tool that reducing 90% times to test, optimizing the efficiency of automation testing by 95%.

#### I have been a software engineer. I took responsibility for transferring the testing process automatically. Applying Python, SQL, Go language, and other development tools to establish a cycle to optimize the quality of the website and application.

### Scratch Data
1. [Selenium](https://github.com/uranus-wyx/shopee/blob/main/selenium%20script.py)
2. [WebCrawler](https://github.com/uranus-wyx/shopee/blob/main/crawler.py)

### Design Tools and Solutions

- ### [AutoUpdateCoins](https://github.com/uranus-wyx/shopee/tree/main/AutoCoinsUpdate)
We need to test function in Coins over 15 countries, and it took us time to wait and operate preconditions manually.
To solve the problem that Coins involved permissions and limitations, I figure out a method that can help our team to reduce time and effort to set preconditions automatically.

     Method 1. Auto Update Coins Amount(GoogleSheet ➢ [py.file](https://github.com/uranus-wyx/shopee/blob/main/AutoCoinsUpdate/AutoCoinsUpdate.py))

        Step1. Input data in GoogleSheet
        Step2. Get ServiceAccountCredentials(Get google sheet authorization.)
        Step3. Read GoogleSheet.
        Step4. Get sheet data to a list.
        Step5. Connect SQLDB and change value in certain position.
        Step6. Log data into Debug.log to track if there was any problem.
        Step7. Deploy this function on Jenkins, it would trigger automaically once a day.
    
     Method 2. Manual Update Coins Amount(GUI ➢ [py.file](https://github.com/uranus-wyx/shopee/blob/main/AutoCoinsUpdate/UpdateCoinsAmount.py))

        Step1. Use Tkinter to create an interface
        Step2. Input value which users want to change its country, coins_amount.
        Step3. Click "submit"
        Step4. Connect SQLDB and change value.
        Step5. Debug Log Data.

* ### TimeZone  
When the backend Platform updated to the new one, all country time has limited with timezone. 
However, I want to solve this problem by transferring timezone to Taiwan's time(GMT+8)

#### Step1. Initial Function
```
def GetCurrentDateTime(format_string, days=0, minutes=0, seconds=0, is_tw_time=0):
    ''' GetCurrentDateTime : Get current date time or Get future/pass date time
            Input argu :
                format_string - datetime format string
        Note : None
    '''

    if is_tw_time:
        region = "TW"
    else:
        region = Config._TestCaseRegion_
    dumplogger.info("Time zone: " + region)

    ##Set timezone
    regional_time_zone = pytz.timezone(Config._TimeZone_[region])
    datetime_string = (regional_time_zone.normalize(datetime.datetime.now(pytz.utc) + datetime.timedelta(days=days, minutes=minutes, seconds=seconds))).strftime(format_string)
    dumplogger.info("Time: " + datetime_string)
    return datetime_string
```

#### Step2. Action Function
```
def InputPromoTime(arg):
    '''
    InputPromoTime : Input promo time
            Input argu :
                start_time - the time of start
                end_time - the time of end
            Return code :
                1 - success
                0 - fail
                -1 - error
    '''
    ret = 1
    start_time = arg["start_time"]
    end_time = arg["end_time"]

    ##Input start time with calculate value by start time
    if start_time:
        start_time_string = XtFunc.GetCurrentDateTime("%Y-%m-%d %H:%M:%S", 0, int(start_time), 0, is_tw_time=1)
        xpath = Util.GetXpath({"locate": "start_time_field"})
        BaseUICore.Click({"method": "xpath", "locate": xpath, "message": "Click start time field", "result": "1"})

        popup_field_xpath = Util.GetXpath({"locate": "start_time_field"})
        BaseUILogic.KeyboardAction({"actiontype":"delete", "locate":popup_field_xpath, "result": "1"})
        BaseUICore.Input({"method": "xpath", "locate": popup_field_xpath, "string": start_time_string, "message": "Input start time", "result": "1"})

        ##send selenium key event
        BaseUICore.SendSeleniumKeyEvent({"action_type":"enter", "string": "", "result": "1"})

    ##Input end time with calculate value by end time
    if end_time:
        end_time_string = XtFunc.GetCurrentDateTime("%Y-%m-%d %H:%M:%S", 0, int(end_time), 0, is_tw_time=1)
        xpath = Util.GetXpath({"locate": "end_time_field"})
        BaseUICore.Click({"method": "xpath", "locate": xpath, "message": "Click end time field", "result": "1"})

        popup_field_xpath = Util.GetXpath({"locate": "end_time_field"})
        BaseUILogic.KeyboardAction({"actiontype":"delete", "locate":popup_field_xpath, "result": "1"})
        BaseUICore.Input({"method": "xpath", "locate": popup_field_xpath, "string": end_time_string, "message": "Input end time", "result": "1"})

        ##send selenium key event
        BaseUICore.SendSeleniumKeyEvent({"action_type": "enter", "string": "", "result": "1"})

    OK(ret, int(arg['result']), 'AdminNewSellerDiscountPage.InputPromoTime')
```

#### Step3. Apply to XML (execute file)
```
<AdminNewSellerDiscountPage.InputPromoTime start_time="5" end_time="10" result="1"/>
```

* ### HttpAPI   
When the backend Platform updated to the new one, I can use API to upload data without 95% time. This process can reduce error and breakthrough the new rules to achieve the successful rate.

#### Step1. Initial Function

```
---Initial HttpAPI and Store Cookie (login data)---
    HttpAPICore.InitialHttpAPI({"session": "unused", "json_data": "common/SellerDiscount/create_seller_discount", "result": "1"})
    HttpAPICore.GetAndSetHttpAPIData({"collection": collection, "result": "1"})
    AdminNewPromotionAPI.StoreNewAdminPromotionCookie({"result": "1"})
    AdminNewPromotionAPI.AssignDataForSellerDiscount({"start_time": start_time, "end_time": end_time, "shop_id": shop_id, "title":title, "result": "1"})
    APICommonMethod.ChangePayloadDictToStr({"result": "1"})
    HttpAPICore.SendHttpRequest({"http_method": "post", "result": "1"})

---Inherit HttpAPI and Send Request---
    HttpAPICore.InitialHttpAPI({"session": "inherit", "json_data": "", "result": "1"})
    HttpAPICore.GetAndSetHttpAPIData({"collection": "upload_product", "result": "1"})
    ***save sth.***
    HttpAPICore.SendHttpRequest({"http_method": "post", "result": "1"})
    APICommonMethod.CheckAPIResponseCode({"result": "1"})
    HttpAPICore.DeInitialHttpAPI({"result": "1"})
```
#### Step2. Apply to XML (execute file)
```
<AdminNewPromotionAPI.CreateSellerDiscount start_time="1" end_time="200" shop_id="********" title="auto test buyer cancel for pc" result="1"/>
```
