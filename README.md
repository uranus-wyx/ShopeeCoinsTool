# Work Experience

#### I have been a software engineer. I took responsibility for transferring the testing process automatically. Applying Python, SQL, Go language, and other development tools to establish a cycle to optimize the quality of the website and application.

### Scratch Data
1. [Selenium](https://github.com/uranus-wyx/shopee/blob/main/selenium%20script.py)
2. [Crawler](https://github.com/uranus-wyx/shopee/blob/main/crawler.py)

### Design Tools 

*  [AutoUpdateCoins](https://github.com/uranus-wyx/shopee/tree/main/AutoCoinsUpdate)

We need to test function in Coins over 15 countries, and it took us time to wait and operate preconditions manually.
To solve the problem that Coins involved permissions and limitations, I figure out a method that can help our team to reduce time and effort to set preconditions automatically.

#### Method 1. Auto Update Coins Amount(GoogleSheet ➢ [py.file](https://github.com/uranus-wyx/shopee/blob/main/AutoCoinsUpdate/AutoCoinsUpdate.py))

    Step1. Input data in GoogleSheet
    Step2. Get ServiceAccountCredentials(Get google sheet authorization.)
    Step3. Read GoogleSheet.
    Step4. Get sheet data to a list.
    Step5. Connect SQLDB and change value in certain position.
    Step6. Log data into Debug.log to track if there was any problem.
    Step7. Deploy this function on Jenkins, it would trigger automaically once a day.
    
#### Method 2. Manual Update Coins Amount(GUI ➢ [py.file](https://github.com/uranus-wyx/shopee/blob/main/AutoCoinsUpdate/UpdateCoinsAmount.py))

    Step1. Use Tkinter to create an interface
    Step2. Input value which users want to change its country, coins_amount.
    Step3. Click "submit"
    Step4. Connect SQLDB and change value.
    Step5. Debug Log Data.
