#!/usr/bin/env python3

## **DESC: This module is for ingesting Legacy customer data from "customers.csv" file to staging table edw.customer_stg in MYSQL**

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
        And define a cursor for records processing.|
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
def getcsv():
    '''
        Read the Legacy customer data from customer csv file and build a dataframe.
    '''
    print('**MSG: Reading customer csv data**')
    custdata = pd.read_csv('customers.csv', index_col=False, delimiter=',', parse_dates=['account_date'])
    print(custdata.head(2))
    return custdata


#****
def insert_customer(custdata, cnx, cursor):
    '''
        Set up iterator for all the rows of customer data frame and insert those to edw.customer_stg table
    '''
 
    print('**MSG: Inserting data to customer_stg**')
    
    # count total rows inserted
    rcnt = 0          
    
    for i,row in custdata.iterrows():
        add_cust = ("INSERT INTO `edw`.`customer_stg`"
                        "(`customeremail`, `firstname`, `lastname`, `city`, `state`, `accountdate`)"
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                       )

        try:
                cursor.execute(add_cust,tuple(row))
                rcnt = rcnt + 1
        except mysql.connector.Error as e:
                print('**ERR: Error inserting rows: ', e)
    
    print('**MSG: Total Rows inserted to customer_stg: ', rcnt)


#****
config = get_config()
cnx, cursor = setup_connection(config)
cust_df = getcsv()
insert_customer(cust_df, cnx, cursor)

cnx.commit()
cursor.close()
cnx.close()