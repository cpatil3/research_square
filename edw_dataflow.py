#!/usr/bin/env python3

## **DESC: This module is for loading customer and transaction staging data to data warehouse tables customer_dim, product_dim and order_f MYSQL**

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
def insert_customer(cnx, cursor):
    '''
        Load data from customer_stg to customer_dim
    '''
 
    print('**MSG: Inserting data to customer_dim**')
    
    add_cust = ("Insert into edw.customer_dim(customeremail, firstname, lastname, city, state, accountdate) "
                 "select * from edw.customer_stg; "
               )
    
    try:
        cursor.execute(add_cust)
        
    except mysql.connector.Error as err:
        print(err)   
        
    else:
        print('**MSG: Total Rows inserted to customer_dim: ', cursor.rowcount)



#****
def insert_product(cnx, cursor):
    '''
        Load data from transaction_stg to product_dim
    '''
 
    print('**MSG: Inserting data to product_dim**')
    
    add_prod = ("Insert into edw.product_dim(product, color, item_size) "
                "select distinct product, color, item_size from edw.transaction_stg; "
               )
    
    try:
        cursor.execute(add_prod)
        
    except mysql.connector.Error as err:
        print(err)   
        
    else:
        print('**MSG: Total Rows inserted to product_dim: ', cursor.rowcount)



#****
def insert_order(cnx, cursor):
    '''
        Load data from transaction_stg to order_f
    '''
 
    print('**MSG: Inserting data to order_f**')
    
    add_order = ("insert into edw.order_f(tranid, custid, order_date, line_num, productid, quantity, total_price) "
                "select t.tranid, c.custid, t.order_date, t.line_num, p.productid, t.quantity, t.total_price "
                    "from edw.transaction_stg t "
                    "inner join edw.customer_dim c on t.customer_email = c.customeremail "
                    "inner join edw.product_dim p   on t.product = p.product ; "
               )
    
    try:
        cursor.execute(add_order)
        
    except mysql.connector.Error as err:
        print(err)   
        
    else:
        print('**MSG: Total Rows inserted to order_f: ', cursor.rowcount)


#****
config = get_config()
cnx, cursor = setup_connection(config)
insert_customer(cnx, cursor)
cnx.commit()
insert_product(cnx, cursor)
cnx.commit()
insert_order(cnx, cursor)
cnx.commit()
cursor.close()
cnx.close()
