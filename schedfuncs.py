# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 12:03:02 2019

@author: rw38913
"""
import PySimpleGUI as sg
import pandas as pd
from pandas import DataFrame
from datetime import date, datetime, timedelta
import time
import csv
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk, ImageFont
import base64
import subprocess
import sys
import sqlalchemy as sqla
from sqlalchemy import create_engine

engine = create_engine('sqlite:///C:\Python_Projects\Advanced Request Form\data4.db', echo=True)
conn = engine.connect().connection


def create_table():
    c.execute(
        'CREATE TABLE IF NOT EXISTS usersdata(createDate TEXT, name TEXT,reason TEXT,startDate TEXT,endDate TEXT)')


def create_table2():
    d.execute('CREATE TABLE IF NOT EXISTS usersname(name TEXT,email TEXT)')


def create_table3():
    e.execute('CREATE TABLE IF NOT EXISTS reindexdate(name TEXT, date TEXT)')


def add_data(create, name, reason, startDate, endDate):
    ret_val = True
    # message=""
    engine.execute('INSERT INTO schedule(Created_On, Fullname, reason, Start_Date, End_Date ) VALUES (?,?,?,?,?)',
                   (create, name, reason, startDate, endDate))
    # conn.commit()
    return ret_val


def view_all_users():
    c.execute('SELECT * FROM usersdata')
    data = c.fetchall()
    # for row in data:
    # 	print(row)
    # return data
    for row in data:
        print(row)
        tree.insert("", tk.END, values=row)


# tab2_display.insert(tk.END,data)

def view_all_details():
    c.execute('SELECT * FROM usersdata')
    data = c.fetchall()
    # for row in data:
    # 	print(row)
    # return data
    for row in data:
        # print(row)
        # tree.insert("", tk.END, values=row)
        tab2_display.insert("", tk.END, row)


def get_single_date(startDate):
    # c.execute('SELECT * FROM usersdata WHERE name="{}"'.format(name))
    c.execute('SELECT * FROM usersdata WHERE startDate="{}"'.format(startDate))
    data = c.fetchall()
    # tab2_display.insert(tk.END,data)
    return data


def edit_single_user(name, new_name):
    c.execute('UPDATE usersdata SET name ="{}" WHERE name="{}"'.format(new_name, name
                                                                       ))
    conn.commit()
    data = c.fetchall()
    return data


def delete_single_user(name):
    c.execute('DELETE FROM usersdata WHERE name="{}"'.format(name))
    conn.commit()


def view_all_data():
    c.execute('SELECT * FROM usersdata')
    data = c.fetchall()


def add_details(name, reason, startDate, endDate):
    today1 = date.today()
    today2 = today1.strftime("%Y/%m/%d")
    create = str(today2)
    name = str(name)
    reason = str(reason)
    startDate = str(startDate)
    endDate = str(endDate)
    return add_data(create, name, reason, startDate, endDate)


def clear_text():
    entry_fname.delete('0', END)
    entry_lname.delete('0', END)
    entry_reason.delete('0', END)


def clear_display_result():
    tab1_display.delete('1.0', END)


def search_user_by_date():
    startDate = str(entry_search.get())
    # result = get_single_user(name)
    result = get_single_date(startDate)
    # c.execute('SELECT * FROM usersdata WHERE startDate="{}"'.format(startDate))
    # data = c.fetchall()
    # print(result)
    tab2_display.insert(tk.END, result)


def clear_display_view():
    tab2_display.delete('1.0', END)


def clear_entered_search():
    entry_search.delete('0', END)


def clear_tree_view():
    # tab2_display.delete('1.0',END)
    tree.delete('1.0', END)

###
#def export_as_csv():
    #timestr = time.strftime("%Y%m%d-%H%M%S")
   # filename = str(timestr)
   # myfilename = filename + '.csv'
   # with open(myfilename, 'w') as f:
   #     writer = csv.writer(f)
   #     connection = engine.raw_connection()
   #     conn.execute('SELECT * FROM schedule')
   #     cursor = connection.cursor()
   #     data = cursor.fetchall()
   #     writer.writerow(['create', 'reason', 'name', 'startDate', 'endDate'])
   #     writer.writerows(data)
   #     messagebox.showinfo(title="DTAC Request Form", message='"Exported As {}"'.format(myfilename))
###
def export_as_csv():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = str(timestr)
    myfilename = filename + '.csv'
    db=sqla.create_engine('sqlite:///C:\Python_Projects\Advanced Request Form\data4.db', echo=False)
    df=pd.read_sql('SELECT * FROM schedule',db)
    df.to_csv(r'C:\Python_Projects\Advanced Request Form\Simple_Request\Scheduler_Export.csv')

def insert_new_user():
    name = (entry_new_name.get())
    email = (entry_new_email.get())
    d.execute('INSERT INTO usersname (name, email) values (?,?)', (name, email))
    conn.commit()
    # values (new_name_raw_entry,new_email_raw_entry)
    entry_new_name.delete('0', END)
    entry_new_email.delete('0', END)
    messagebox.showinfo(title="DTAC Request Form", message="Submitted to DataBase")


def check_date(endDate, startDate, df):
    end_date_dt = datetime.strptime(endDate, '%m/%d/%Y')
    start_date_dt = datetime.strptime(startDate, '%m/%d/%Y')
    end_date = end_date_dt  # alias
    start_date = start_date_dt  # alias
    delta = end_date - start_date
    date_list = []
    # Create a list of the date ranges
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        date_list.append(day.strftime('%m/%d/%Y'))

    # Set an error if this would be the third time or more this date was added.
    duplicate_date_error = False
    duplicate_date_error_list = []
    for date_string in date_list:
        if len(df[df.Start_Date == date_string]) >= 2:
            duplicate_date_error = True
            duplicate_date_error_list.append(date_string)

        if duplicate_date_error:
            print('Found too many duplicate dates.  Listing failed dates below.')
            print(duplicate_date_error_list)
        else:
            return successful
    # This is where the dataframe is updated with the date list and written back to the database
    print('Added date list to database')
