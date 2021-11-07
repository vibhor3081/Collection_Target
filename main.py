 # This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import base64
import dateutil
import mysql.connector as sql
import os
import pandas as pd
import streamlit as st
import pymysql.cursors
import array as arr
import ruamel.yaml as yaml
import lib
import deetly as dl
import numpy as np


db_config = dict([
    ('hostname', 'canvasdb.caxvr8jox9y6.us-east-2.rds.amazonaws.com'),
    ('port', 3306),
    ('username', 'admin'),
    ('password', '77YnH0bqO8oHMYZGmu78'),
    ('database', 'Vriddhi')
])

DATA_DIR = 'DataFiles'

field_officer = "SF075-Dinesh Padye"

st.title("Target")

conn = sql.connect(host=db_config['hostname'], port=db_config['port'], user=db_config['username'], password=db_config['password'], database=db_config['database'])

Member_Data = pd.read_sql(f"SELECT MemNum, FieldOfficer, BranchName, Community FROM Curr_User_Member",
                                  conn)

Collection_Target = pd.read_sql(f"SELECT MemNum, CollDate_CurrWeek, CollDue_Reg_CurrWeek, Mem_CollFreq_IB FROM Curr_Accounts_2021_11_Member", conn)

Field_Officer_List = pd.read_sql(f"SELECT DISTINCT FieldOfficer FROM Curr_User_Member",
                                  conn)

option = st.selectbox('Select Field Officer', Field_Officer_List)

st.write('You selected:', option)

Account_Detail = pd.merge(Member_Data, Collection_Target, on = "MemNum", how = "right")

Account_Detail['CollDue_Reg_CurrWeek'] = Account_Detail['CollDue_Reg_CurrWeek'].astype(float)

table2 = pd.pivot_table(Account_Detail[Account_Detail['FieldOfficer'] == option], columns= ['BranchName'], values= 'CollDue_Reg_CurrWeek', margins= False, fill_value=0, aggfunc= 'sum')

st.table(table2)

if st.button("Get Detail"):

     Account_Detail_new = Account_Detail[Account_Detail['CollDue_Reg_CurrWeek'] > 0]

     st.table(Account_Detail_new[Account_Detail_new['FieldOfficer'] == option].dropna(subset = ['CollDue_Reg_CurrWeek']))



# with st.expander(""): ['FieldOfficer'] == field_officer]

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
