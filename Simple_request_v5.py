# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 21:16:08 2019

@author: rw38913
"""

import PySimpleGUI as sg
import pandas as pd
from pandas import DataFrame
from datetime import datetime, date, time, timedelta
import os
import io
from PIL import Image, ImageDraw, ImageTk, ImageFont
import base64
import subprocess
import sys
import sqlalchemy as sqla
import schedfuncs as sf

# connect to database
from sqlalchemy import create_engine
engine = create_engine('sqlite:///C:\\Python_Projects\\Advanced Request Form\\data5.db', echo=False)
conn=engine.connect()
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()

# JD Colors
green = '#367C2B'
yellow = '#FFDE00'
black = '#27251F'


# create two tables, users and schedule 
users = Table('users', metadata,
    Column('fullname', String(50)),
    Column('email', String(80))
    )

schedule = Table('schedule', metadata,
    Column('Created_On', String(50), nullable=False),
    Column('reason', String(50), nullable=False),
    Column('Fullname', String(50), nullable=False),
    Column('Start_Date', String(10), nullable=False),
    Column('End_Date', String(10), nullable=False)
    )

admin = Table('admin', metadata,
    Column('id', Integer, primary_key=True),          
    Column('duplicate_registrations', String(5)),
    )
metadata.create_all(engine)
#____________________________

# Button colors
bcolor = ('grey', 'white')
wcolor = ('white', 'white')

main_name_list =  ['Jim Walter',
             'Kevin Spacey',
             'Jarrod Burgandy',
             'Michael Haney',
             'Rob Willcheck',
             'Jeremy Jhonston']


main_reason_list = ['Vacation',
             'Training',
             'Work Travel',
             'FMLA',
             'Development',
             'Other']

name = main_name_list
reason = main_reason_list

#create dataframe to simulate databse with names and dates
data = {'Name': ['Joe Smith', 'Jason Leary','Bill Murray'],
        'Start_Date': ['2019/10/01', '2019/11/01','2019/12/01'],
        'End_Date': ['2019/10/15', '2019/11/15','2019/12/15']
        }
df = pd.DataFrame (data)
#Data_Table = pd.DataFrame(data)
Data_Table = df.values.tolist()
#headings = [Data_Table[0][x] for x in range(len(Data_Table[0]))]
headings = ['Name','Start Date', 'End Date']

# todays date for creation stamp
today1 = date.today()
today2 = today1.strftime("%m/%d/%Y")


# Stuff inside window
tab1_layout = [
    [sg.Text('The Scheduler')], 
    [sg.Combo(name, size=(30,4), enable_events=True, key='_name_')],
    [sg.Combo(reason, size=(30,4), enable_events=True, key='_reason_')],
    [sg.T('Start Date')],
          [sg.In('', size=(10,1), key='input1')],
          [sg.CalendarButton('Choose Start Date', target='input1', key='_date1_',format='%m/%d/%Y')],
    [sg.T('End Date')],
          [sg.In('', size=(10,1), key='input2')],
          [sg.CalendarButton('Choose End Date', target='input2', key='_date2_', format='%m/%d/%Y')],
    [sg.Button('Submit',button_color=('white', 'springgreen4'), font='Any 15', key='_subdate_')]]

# create a table to show names and dates with an export to CSV button
tab2_layout = [[sg.Table(values=Data_Table,headings=headings, background_color='lightblue',
                        auto_size_columns=True, justification='left', alternating_row_color='blue', key='_table_')],
          [sg.Button('Update', button_color=('white', '#00406B'), font='Any 15',  key='_update_'),sg.Button('Remove', button_color=('white', '#00406B'), font='Any 15',  key='_remove_'), sg.Button('Export', button_color=('white', '#00406B'), font='Any 15', pad=(1,1), key='_export_')]]



tab3_layout = [
    [sg.Text('Enter New Name'), sg.InputText()],
    [sg.Text('Enter New Email'), sg.InputText()],
    [sg.Button('Submit',button_color=('white', 'springgreen4'), font='Any 15', key='_subname_'), 
     sg.Button('Cancel', button_color=('white', 'springgreen4'), font='Any 15', key='_clear1_')],
[sg.Text('Name to Delete'), sg.InputText()],
[sg.Text('Email to Delete'), sg.InputText()],
[sg.Button('Submit',button_color=('white', '#367C2B'), border_width=None, font='Any 15', key='_delname_'), 
 sg.Button('Cancel', button_color=('white', '#00406B'), border_width=None, font='Any 15', key='_clear2_')],
    [sg.Text('Max out'), sg.InputText(key='maxout')],
    [sg.Button('Submit',button_color=('white', 'springgreen4'), font='Any 15', key='_maxout_')]]

# create the window
layout = [[sg.TabGroup([[sg.Tab('Scheduler', tab1_layout,  key='_mykey_'),
                         sg.Tab('Schedule', tab2_layout),
                         sg.Tab('Admin', tab3_layout)]],
                         key='_group2_', title_color='DarkSlateGray',
                         selected_title_color='black', tab_location='topleft')]]

window = sg.Window('Scheduler', default_element_size=(50,0)).Layout(layout)


# event loop to process events and get the values of inputs
while True:      
    event, values = window.Read() 
    print(event, values)       
    if event in (None, 'Exit'):      
        break  
    if event == '_subdate_':
        # check for douplicate dates, then reject or write to db (write name, start date, end date)
        #sf.check_date(startDate=values['input1'],endDate=values['input2'])
        sf.check_date(startDate=values['input1'],endDate=values['input2'],df=df)
        successful=sf.add_details(name=values['_name_'],reason=values['_reason_'],startDate=values['input1'],endDate=values['input2'])
        if not successful:
            #show message box indicating failure to add date
            pass
    if event == '_remove_':
        # delete existing registration from db
        pass
    if event == '_export_':
        # export to CSV file
        sf.export_as_csv()
        pass
    if event == '_subname_':
        # write new name and email to db (manager only)
        #insert_new_user()
        pass
    if event == '_clear1_':
        # clear out contents of add name section of form (manager only)
        #clear_display_view()
        pass
    if event == '_delname_':
        # delete name and email from db (no longer in role) (manager only)
        pass
    if event =='_clear2_':
        #clear out contents of delete section of form (manager only)
        #clear_display_view()
        pass
    elif event =='_maxout_':
        dup_reg=values['maxout']
        if len(values['_maxout']) and values['maxout'][-1] not in ('0123456789'):  # if last char entered not a digit
            window.Element('maxout').Update(values['maxout'][:-1])
        db=sqla.create_engine('sqlite:///C:\Python_Projects\Advanced Request Form\data4.db', echo=True)
        query=sqla.update(admin).values(duplicate_registrations=dup_reg).where(id==1)
        conn.execute(query)
        
     
        
# Values ---------
#vname = values['_name_']
#vreason = values['_reason_']
#vstartDate = values['input1']
#vendDate = values['input2']
# pop up confirming imputs
text_input = values[0]    
sg.Popup('You entered', text_input)
window.Close()