#!/usr/bin/python
#-*- coding: utf-8 -*-

##import library
import sys
import os
import logging
import datetime
import requests
import urllib
import argparse
import pandas as pd

##Set filename by datename
log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + 'pyhw3'
log_path = '{filename}.log'.format(filename = log_filename)
##Log basic
logging.basicConfig(
    filename = log_path,
    filemode = 'a+',
    level = logging.INFO,
    format = '%(asctime)s-[%(process)d][%(thread)d]|[%(levelname)s]|[%(filename)s:%(lineno)d][%(funcName)s]|%(message)s'
)

def crawler(keyword):
  '''
  Crawler the keyword in Shopee.com
  '''
  headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36','x-api-source': 'pc'}
  session = requests.Session()
  ##encode keyword(url)
  keyword = urllib.quote(keyword)
  logging.info('Keyword encoding...')
  base_url = 'https://shopee.tw/api/v4/search/search_items'
  ##set a dict，append {shopid, sold} in web data
  get_data_dic = {'shopid':[], 'sold':[]}
  get_data_list = []
  page = 0
  try:
    ##Set a loop X in 5，limit 300 products in 5 pages
    while page < 5: 
      ##Set newest = x*60 => one page default 60 items
      query = 'by=relevancy&keyword={0}&limit=60&newest={1}&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(keyword, page * 60)
      url = base_url + '?' + query
      requests_url = session.get(url, headers = headers)
      logging.info('Page{0} of URL has been requested successfully.'.format(page + 1))
      if requests_url.status_code == requests.codes.ok:
        web_data = requests_url.json()
        logging.info('Page{0} of Web Data has been downloaded.'.format(page + 1))
      try:
        if 'items' in web_data.keys():
          if page == 0 and len(web_data['items']) == 0:
            logging.info('Page{0} has no products.'.format(page + 1))
            print("Product not Found")
            break
          ##Keyword have found the products
          elif len(web_data['items']) != 0:
            ##Scratch shopid,sold in item_basic
            for item_list in web_data['items']:
              item = item_list['item_basic']
              ##Put data into a new dictionary
              get_data_dic['shopid'].append(item['shopid'])
              get_data_dic['sold'].append(item['sold'])
            logging.info('Page{0} has products.'.format(page + 1))
          else:
            logging.info('Page{0} has no products.'.format(page + 1))
            break
      except:
        logging.error("Unexpected error:{error}.".format(error = sys.exc_info()[0]))
      else:
        ##Put dictionary value into result list
        get_data_list.append(get_data_dic)
        ##loop += 1, or infinite loop
        page += 1
    logging.info('{amount} products exists'.format(amount = len(get_data_dic['shopid'])))
    logging.info('Total {amount} pages'.format(amount = len(get_data_list)))
  except:
    logging.error("Unexpected error:{error}.".format(error = sys.exc_info()[0]))
  else: 
    logging.info('Crawler Completed')
    return get_data_list

def dataframe(result_data):
  '''
  Put the result data into DataFrame
  '''
  if len(get_data_list) != 0 : 
    for page_item in range(0, len(get_data_list)): 
      ##Put all rows of data into dataframe
      all_items_df = pd.DataFrame(get_data_list[page_item]) 
    logging.info('Products put in DataFrame successfully.')
    ##Groupby shopid
    shop_items_groupby = all_items_df.groupby(by = ["shopid"]).sum() 
    logging.info('Products groupby successfully.')
    ##Descending columns of sold, and reset new index 
    items_sales_amount_sort = shop_items_groupby.sort_values(by = ['sold'], ascending = False).reset_index()
    logging.info('Products sort successfully.')
    items_result = items_sales_amount_sort.head(50)

    for items_rows in range(len(items_result)):
      ##Print rows of dataframe 
      output = 'The number {} shop is {} with sales amount {} '.format(items_rows + 1, items_result['shopid'][items_rows], items_result['sold'][items_rows])
      print(output)
    logging.info('Sort out Completed')
    logging.info('There are {} rows of data output.'.format(len(items_result)))
  else:
    logging.info('No item should put in DataFrame.')
    
def parse_args():
  '''
  Input the keyword 
  '''
  parser = argparse.ArgumentParser(prog = 'Crawler the keyword in Shopee.com')
  parser.add_argument('--keyword', '-k', type = str, action = 'append', nargs = '+', help = 'Please input the keyword.')
  return parser.parse_args()

def get_keyword(args):
  '''
  Get the keyword
  '''
  try:
    keyword = str(args.keyword[0][0])
    logging.info('Search {}...'.format(keyword))
  except:
    logging.error("Unexpected error:{error}.".format(error = sys.exc_info()[0]))
  return keyword

#Call main function
if __name__ == '__main__':
  args = parse_args()
  keyword = get_keyword(args)
  get_data_list = crawler(keyword)
  dataframe(get_data_list)
  