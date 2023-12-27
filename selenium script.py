#!/usr/bin/python
#-*- coding: utf-8 -*-

##Import library
import sys
import os
import time
from datetime import datetime
import logging
import traceback
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ScreenshotException

##Solving Windows default encode "ascii"
reload(sys)
sys.setdefaultencoding('utf-8')

##Set path
path = 'C:\Users\yuni.wu\Documents\Selenium HW'
os.chdir(path)
os.getcwd()

##Set filename by datename
log_filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + 'selenium_hw_log'
log_path = '{filename}.log'.format(filename = log_filename)

##Log basic
logging.basicConfig(
    filename = log_path,
    filemode = 'a+',
    level = logging.INFO,
    format = '%(asctime)s-[%(process)d][%(thread)d]|[%(levelname)s]|[%(filename)s:%(lineno)d][%(funcName)s]|%(message)s'
)

##Create dictionary to fill in path
shopee_path = { 
    ##Home Pop up banner
    'popup_close_window' : '//div[@data-cy="shopee_popup_close_button"]',
    ##HomePage
    'login_url' : '//a[@data-cy="login_button_home_page"]',
    'login_username' : '//div[@data-cy="username_home_page"]',
    ##Login Page
    'loginkey' : '//input[@data-cy="authentication-pc/account_input_raw_account_login_page"]',
    'password' : '//input[@data-cy="authentication-pc/password_input_raw_account_login_page"]',
    'login_button' : '//button[@data-cy="authentication-pc/login_button_login_page"]',
    ##Product Detail Page
    'buy_now_button' : '//button[@data-cy="buy_now_button_product_detail_page"]',
    'sold_out_banner' : '//div[@data-cy="item_sold_out_label_pdp""]',
    ##Checkout
    'checkout_button' : '//button[@data-cy="checkout_button_cart_page"]',
    'popup_container' : 'toast-container',
    ##Payment
    'cod_payment_button' : '//button[@data-cy="select_payment_icon_checkout_page"]',
    'cod_payment_label' : '//div[@class="_-packages-checkout-page-pc-src-components-PaymentMethodView-style__currentType"]',
    ##Place Order
    'place_order_button' : '//button[@data-cy="place_order_button_checkout_page"]',
    ##Check Order Completed
    'To_pay_label' : '//div[@data-cy="order_list_page_order_card_header_status"]',
    'To_shipped_label' : '//div[@data-cy="order_list_page_order_card_header_status"]'
}

class Selenium_HW:

    def WebDriver(self):
        '''
        Initial WebDriver
        '''
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        driver = webdriver.Chrome(chrome_options = options)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
    
    def ExceptionHandling(self, error_message):
        '''
        Handling selenium exceptions
        '''
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print ('exc_type:', exc_type)
        print ('exc_value:', exc_value)
        print ('exc_traceback:', exc_traceback)
        ##Log error message
        logging.exception(error_message)
        self.Screenshot()
        self.driver.quit()
        exit()

    def Screenshot(self):
        '''
        Take a screenshot
        '''
        screenshot_filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + 'selenium_hw_screenshot.png'
        screenshot_path = '{filename}'.format(filename = screenshot_filename)
        try:
            self.driver.get_screenshot_as_file(screenshot_path)
            logging.info('Take screenshot')
        except ScreenshotException as screenshot_error:
            logging.info('Can not take screenshot')
            self.ExceptionHandling(screenshot_error)
        
    def CheckElementExist(self, path):
        '''
        Check element exist
        '''
        try:
            ##Find path exist or not
            exist_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, path)))
            logging.info('{path} exist'.format(path = path))
        except NoSuchElementException as non_element_error:
            logging.error('{path} not exists'.format(path = path))
            self.ExceptionHandling(non_element_error)
        except Exception as except_error:
            logging.error('Something wrong in {path} '.format(path = path))
            self.ExceptionHandling(except_error)
        time.sleep(random.randint(3, 5))
        return exist_element
    
    def CheckElementNotExist(self, path):
        '''
        Check element not exist
        '''
        try:
            ##Find path not exist
            not_exist_element = self.wait.until_not(EC.visibility_of_element_located((By.CLASS_NAME, path)))
            logging.info('{path} not exist'.format(path = path))
        except NoSuchElementException as non_element_error:
            logging.error('{path} not exists'.format(path = path))
            self.ExceptionHandling(non_element_error)
        except Exception as except_error:
            logging.error('Something wrong in {path} '.format(path = path))
            self.ExceptionHandling(except_error)
        return not_exist_element
           
    def ClickElementAction(self, path):
        '''
        Check button clickable
        '''
        try:
            ##Find path and click it
            click_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, path)))
            click_element.click()
            logging.info('Click {path}'.format(path = path))
        except ElementClickInterceptedException as intercepted_error:
            logging.error('{path} not clickable'.format(path = path))
            self.ExceptionHandling(intercepted_error)
        except Exception as except_error:
            logging.error('Something wrong in {path} '.format(path = path))
            self.ExceptionHandling(except_error)
        return 
    
    def InputValue(self, text_field, value):
        '''
        Input value
        '''
        try:
            ##Find path and input value
            input_element = self.driver.find_element_by_xpath(text_field).send_keys(value)
            logging.info('Input {value} in {text_field}'.format(value = value, text_field = text_field))
        except NoSuchElementException as non_element_error:
            logging.error('{path} not exist'.format(path = path))
            self.ExceptionHandling(non_element_error)
        except Exception as except_error:
            logging.error('Something wrong in {path} '.format(path = path))
            self.ExceptionHandling(except_error)
        return input_element
    
    def TextPresent(self, path, text):
        '''
        Check text in element
        '''
        try:
            ##Find text in path 
            text_exist_element = self.wait.until(EC.text_to_be_present_in_element((By.XPATH, path), text))
            logging.info('Text exist in {path}'.format(path = path))
        except NoSuchElementException as non_element_error:
            logging.error('{path} not exist'.format(path = path))
            self.ExceptionHandling(non_element_error)
        except Exception as except_error:
            logging.error('Something wrong in {path} '.format(path = path))
            self.ExceptionHandling(except_error)  
        return text_exist_element

    def GotoHomePage(self):
        '''
        Go to main url
        '''
        logging.info('===== Start GotoHomePage =====')
        shopee_url = "https://staging.shopee.tw/"
        self.driver.get(shopee_url)
        logging.info('===== Finish GotoHomePage =====')

    def HomePagePopup(self):
        '''
        Close Home page pop up banner
        '''
        logging.info('===== Start HomePagePopup =====')
        ##Check popup close button
        if self.CheckElementExist(shopee_path['popup_close_window']):
            ##Click popup close button
            self.ClickElementAction(shopee_path['popup_close_window'])
            logging.info('Close pop up banner')
            print('Close pop up banner')
        else:
            logging.info('There is no popup banner')
            print('There is no popup banner')
        logging.info('===== Finish HomePagePopup =====')
    
    def GoToLoginPage(self):
        '''
        Landing login page from home page
        '''
        logging.info('===== Start GoToLoginPage =====')
        ##Check login button in homepage 
        self.CheckElementExist(shopee_path['login_url'])
        ##Click login button in homepage 
        self.ClickElementAction(shopee_path['login_url'])
        logging.info('===== Finish GoToLoginPage =====')

    def LoginPage(self, username, password):
        '''
        Login with username and password
        '''
        logging.info('===== Start LoginPage =====')
        ##Input account
        self.CheckElementExist(shopee_path['loginkey'])
        self.InputValue(shopee_path['loginkey'], username)
        logging.info('Input username')
        ##Input password
        self.CheckElementExist(shopee_path['password'])
        self.InputValue(shopee_path['password'], password)
        logging.info('Input password')
        ##Check login button
        self.CheckElementExist(shopee_path['login_button'])
        ##Click login button
        self.ClickElementAction(shopee_path['login_button'])
        logging.info('===== Finish LoginPage =====')
    
    def CheckLoginStatus(self, username):
        '''
        Check Login upper right on Home Page
        '''
        ##After login, jump to homepage
        logging.info('===== Start CheckLoginStatus =====')
        ##Close homepagepopup
        self.HomePagePopup()
        ##Check login name on the upper right corner in homepage
        self.CheckElementExist(shopee_path['login_username'])
        self.TextPresent(shopee_path['login_username'], username)
        logging.info('Login successfully')
        print('Login Successfully')
        logging.info('===== Finish CheckLoginStatus =====')
        
    def ProductDetailPage(self):
        '''
        Landing product detail page and click buy now button
        '''
        logging.info('===== Start ProductDetailPage =====')
        ##Directly to product detail page
        PDP_url = 'https://staging.shopee.tw/Disneyland-ticket-i.200706157.101086804'
        self.driver.get(PDP_url)
        logging.info('Landing Product Detail Page')
        ##Buy_now button cannnot be clicked, product sold out.
        if self.CheckElementNotExist(shopee_path['sold_out_banner']) == False:
            logging.info('This product sold out')
            print('This product sold out')
            pass  
        else:
            ##Check buy now button
            self.CheckElementExist(shopee_path['buy_now_button'])
            ##Click buy now button
            self.ClickElementAction(shopee_path['buy_now_button'])
            logging.info('Click Buy Now botton successfully')
            print('Click Buy Now botton successfully')
        logging.info('===== Finish ProductDetailPage =====')

    def CartPage(self):
        '''
        Click checkout button in cart
        '''
        logging.info('===== Start Checkout =====')
        ##Wait the pop up window "商品已加入購物車" invisibility, and continue
        self.CheckElementNotExist(shopee_path['popup_container'])
        time.sleep(random.randint(5, 10))
        ##Check checkout button
        self.CheckElementExist(shopee_path['checkout_button'])
        ##Click checkout button
        self.ClickElementAction(shopee_path['checkout_button'])
        logging.info('Checkout Successfully')
        print('Checkout Successfully')
        logging.info('===== Finish Checkout =====')
        
    def ChoosePaymentMethod(self):
        '''
        Choose payment method
        '''
        logging.info('===== Start ChoosePaymentMethod =====')
        ##Default payment method, COD
        if self.TextPresent(shopee_path['cod_payment_label'], '貨到付款'):
            logging.info('Payment method, COD')
            print('Payment choose already')
            pass
        else:
            ##Check Cod button
            self.CheckElementExist(shopee_path['cod_payment_button'])
            ##Click COD button
            self.ClickElementAction(shopee_path['cod_payment_button'])
            logging.info('Choose COD')
            print('Choose COD')
        logging.info('===== Finish ChoosePaymentMethod =====')

    def PlaceOrder(self):
        '''
        Place the order 
        '''
        ##Scroll down the page
        self.driver.execute_script("window.scrollTo(0,1000)")
        logging.info('Scrolling down')
        print('Scrolling down')
        ##Check place order button
        self.CheckElementExist(shopee_path['place_order_button'])
        ##Click place order button
        self.ClickElementAction(shopee_path['place_order_button'])
        logging.info('Place order successfully')
        print('Place order successfully') 
        logging.info('===== Finish PlaceOrder =====')

    def CheckOrderCompleted(self):
        '''
        Check order purchased completely
        '''
        ##Check if the order in 'To Pay'
        if self.TextPresent(shopee_path['To_pay_label'], '待付款'):
            print('Successfully Purchase, "To Pay"')
            logging.info('Successfully Purchase, "To Pay"')
        ##Check if the order in 'To Shipped'
        elif self.TextPresent(['To_shipped_label'], '待出貨'):
            print('Successfully Purchase, "To Shipped"')
            logging.info('Successfully Purchase, "To Shipped"')
        ##Check if the order not in 'To Pay' or 'To Shipped'
        else:
            print('Failed Purchase')
            logging.info('Failed Purchase')
        logging.info('===== Finish CheckOrderCompleted =====')
        self.driver.quit()
        return

if __name__ == '__main__':
    Selenium = Selenium_HW()
    Selenium.WebDriver()
    ##Go to Home Page
    Selenium.GotoHomePage()
    ##Close Home Page Pop Up Banner
    Selenium.HomePagePopup()
    ##Go to Login Page
    Selenium.GoToLoginPage()
    ##Login with Account
    Selenium.LoginPage('y_test_004', 'Aa123456')
    ##Check login status
    Selenium.CheckLoginStatus('y_test_004')
    ##Go to Product Detail Page and Click Buy Now Button
    Selenium.ProductDetailPage()
    ##Checkout Order in Cart Page
    Selenium.CartPage()
    ##Choose Payment
    Selenium.ChoosePaymentMethod()
    ##Place Order
    Selenium.PlaceOrder()
    ##Check Order Completed
    Selenium.CheckOrderCompleted()
    logging.info('===== FINISH =====')
