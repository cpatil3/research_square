#!/usr/bin/env python3

## **DESC: This module is for ingesting Transaction data from "transactions.jason" file to staging table edw.transaction_stg in MYSQL**

#Create connection with MYSQL
import mysql.connector
from mysql.connector import errorcode

#import jason library
import json

#import pandas library for working with dataframes
import pandas as pd

#import datetime module for dates manipulation
from datetime import datetime

#****
def get_config():
    config = {}
    jfile = open('config.json')
    config = json.load(jfile)
    
    return config

#****
def setup_connection(config):
    '''
        This function is to set up connection with MYSQL 'edw' database.
        And define a cursor for records processing.
    '''

    try:
        cnx = mysql.connector.connect(**config)
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('**ERR: Invalid id or password**')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(err.errno)
                print('**ERR: Wrong dbname or db does not exists**')
        else:
                print(err)
    else:
            print('**MSG: Connection to db successful**')
            cursor = cnx.cursor()
            return cnx, cursor



#****
def get_jasondata():
    '''
        This function is to read the transaction jason file
    '''
    jfile = open('transactions.json')
    jdata = json.load(jfile)
    
    # print(list(jdata2)[0:10])
    print('**MSG: Total Transactions: ', len(jdata))
    return jdata


#****
def insert_trans(jdata, cnx, cursor):
    '''
        Set up iterator for all the key values in Transaction jason data and insert those to edw.transaction_stg table
    '''
 
    print('**MSG: Inserting data to transaction_stg**')
    
    # count total rows inserted
    rcnt = 0          
    
    add_tran = ("INSERT INTO `edw`.`transaction_stg` "
                   "(`tranid`, `customer_email`, `order_date`, `line_num`, `product`, `quantity`, `color`, `item_size`, `total_price`)"
                   "VALUES (%(tranid)s, %(customer_email)s, %(order_date)s, %(line_num)s, %(product)s, %(quantity)s, %(color)s, %(item_size)s, %(total_price)s)"
                )

    cn = 0
    for i in jdata:
        cn = 1
        for j in jdata[i]['line_items']:
            try:
                data_tran = {"tranid": i, "customer_email": jdata[i]['customer_email'], "order_date": jdata[i]['order_date'],
                             "line_num": cn, "product": j, "quantity": jdata[i]['line_items'][j]['quantity'], 
                             "color": jdata[i]['line_items'][j]['color'], "item_size": jdata[i]['line_items'][j]['item_size'], 
                             "total_price": jdata[i]['line_items'][j]['total_price']
                            }
                cursor.execute(add_tran, data_tran)
                rcnt = rcnt + 1
            except mysql.connector.Error as err:
                print(err)
            else: 
                cn = cn + 1
                
    print('**MSG: Total Rows inserted to transaction_stg: ', rcnt)



#****
config = get_config()
cnx, cursor = setup_connection(config)
jdata = get_jasondata()
insert_trans(jdata, cnx, cursor)
cnx.commit()
cursor.close()
cnx.close()