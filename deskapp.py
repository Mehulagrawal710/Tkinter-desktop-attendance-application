import tkinter as tk
from tkinter import *
from tkinter import filedialog

from functools import *
import copy

import numpy as np
import pandas as pd
import datetime as dt

m = Tk()
m.title("Codenscious Attendance System")
m.geometry('1200x600')

############################################
############# FUNCTIONALITY ################
def open_file():
	filename = filedialog.askopenfilename(initialdir="/", title="select a file")
	label = Label(m, text="")
	label.place(x=5, y=105)
	label.configure(text = filename)
	df = pd.read_csv(filename, comment="#", sep="\t")
	df['DaiGong'] = pd.to_datetime(df['DaiGong'], dayfirst = False, yearfirst = True)
	global main_data_frame
	main_data_frame = df

def reset():
	global box
	box.delete(0, END)

def initialize():
	pass

def two_fields():
	e3.place_forget()
	l3.place_forget()
	b2.place_forget()
	l1.place(x=10, y=300)
	l2.place(x=10, y=350)
	e1.place(x=150, y=300)
	e2.place(x=150, y=350)
	b1.place(x=100, y=400)

def one_field():
	e1.place_forget()
	e2.place_forget()
	l1.place_forget()
	l2.place_forget()
	b1.place_forget()
	l3.place(x=10, y=300)
	e3.place(x=150, y=300)
	b2.place(x=100, y=350)

def create_df(start_date, end_date, df):
    min_limit = pd.to_datetime(start_date+' 00:00:00', dayfirst = True, yearfirst = False)
    max_limit = pd.to_datetime(end_date+' 23:59:59', dayfirst = True, yearfirst = False)
    df = df[(df.DaiGong > min_limit) & (df.DaiGong < max_limit)]
    return df

def assign_per_day(p_copy, in_out_time):
    for key, value in in_out_time.items():
        if value['in_time'] == 0 and value['out_time'] == 0:
        	p_copy[key]['absent'] += 1
        else:
	        if value['in_time'] == 0:
	            value['in_time'] = am1030
	        if value['out_time'] == 0:
	            value['out_time'] = pm6000
	        if value['in_time'] < am1015 and pm0300 < value['out_time'] < pm0555:
	            p_copy[key]['half_days'] += 1
	        elif value['in_time'] < am1015 and value['out_time'] > pm0555:
	            p_copy[key]['full_days'] += 1
	        elif am1015 < value['in_time'] < pm0300 and pm0300 < value['out_time'] < pm0555:
	            p_copy[key]['half_days'] += 1
	        elif am1015 < value['in_time'] < pm0300 and value['out_time'] > pm0555:
	            p_copy[key]['half_days'] += 1
    return p_copy

def clear_in_out_time():
    for key, value in in_out_time.items():
        value['in_time'] = 0
        value['out_time'] = 0

def get_attendance():
	global scrollbar
	global box
	global day_count_box
	working_days = 0
	p_copy = copy.deepcopy(people)
	in_out_time = dict()
	for key, value in p_copy.items():
		in_out_time[key] = {'in_time': 0, 'out_time': 0}
	df = create_df(e1.get(), e2.get(), main_data_frame)
	if len(df)==0:
		box.delete('1.0', END)
		box.insert(END, 'No data available for this date\n')
	else:
		pre_date = df.iloc[0]['DaiGong'].strftime("%x")
		for index, row in df.iterrows():
		    if row['DaiGong'].strftime("%a") != 'Sun':
		        today_date = row['DaiGong'].strftime("%x")
		        if today_date != pre_date:
		        	working_days += 1
		        	p_copy = assign_per_day(p_copy, in_out_time)
		        	for key, value in in_out_time.items():
		        		value['in_time'] = 0
		        		value['out_time'] = 0
		        if row['DaiGong'].strftime("%X") < pm0300:
		            in_out_time[row['EnNo']]['in_time'] = row['DaiGong'].strftime("%X")
		        else:
		            in_out_time[row['EnNo']]['out_time'] = row['DaiGong'].strftime("%X")
		        pre_date = today_date
		if df.iloc[-1]['DaiGong'].strftime("%a")!='Sun':
			working_days += 1
			p_copy = assign_per_day(p_copy, in_out_time)
		stdt = pd.to_datetime(e1.get()+' 00:00:00', dayfirst = True, yearfirst = False)
		endt = pd.to_datetime(e2.get()+' 23:59:59', dayfirst = True, yearfirst = False)
		day_count_box.delete(0, END)
		day_count_box.insert(END, "{}, {}".format(stdt.strftime("%x"), stdt.strftime("%a")))
		day_count_box.insert(END, "to")
		day_count_box.insert(END, "{}, {}".format(endt.strftime("%x"), endt.strftime("%a")))
		day_count_box.insert(END, "\n")
		#day_count_box.insert(END, "Total days: {}".format(working_days+sun_count))
		day_count_box.insert(END, "Working days: {}".format(working_days))
		#day_count_box.insert(END, "Sundays: {}".format(sun_count))
		box.delete('1.0', END)
		for key, value in p_copy.items():
			box.insert(END, "Name: {}\n".format(value['name']))
			box.insert(END, "Full Days: {}\n".format(value['full_days']))
			box.insert(END, "Half Days: {}\n".format(value['half_days']))
			box.insert(END, "Absent: {}\n".format(value['absent']))
			box.insert(END, "---------------------------------------\n")
		scrollbar.config( command = box.yview )

def get_time():
	global scrollbar
	global box
	global day_count_box
	pardt = pd.to_datetime(e3.get()+' 00:00:00', dayfirst = True, yearfirst = False)
	day_count_box.delete(0, END)
	day_count_box.insert(END, "{}, {}".format(pardt.strftime("%x"), pardt.strftime("%a")))
	p_copy = copy.deepcopy(people)
	in_out_time = dict()
	for key, value in p_copy.items():
		in_out_time[key] = {'in_time': 0, 'out_time': 0}
	df = create_df(e3.get(), e3.get(), main_data_frame)
	if len(df)==0:
		box.delete('1.0', END)
		box.insert(END, 'No data available for this date\n')
	else:
		for index, row in df.iterrows():
		    if row['DaiGong'].strftime("%X") < pm0300:
		        in_out_time[row['EnNo']]['in_time'] = row['DaiGong'].strftime("%X")
		    else:
		        in_out_time[row['EnNo']]['out_time'] = row['DaiGong'].strftime("%X")
		
		box.delete('1.0', END)
		for key, value in in_out_time.items():
			box.insert(END, "Name: " + p_copy[key]['name'] + "\n")
			if value['in_time']==0 and value['out_time']==0:
				box.insert(END, "Absent\n")
			else:
				if value['in_time']!=0:
					box.insert(END, "In Time: {}\n".format(value['in_time']))
				else:
					box.insert(END, "In Time: *not punched*\n")
				if value['out_time']!=0:
					box.insert(END, "Out Time: {}\n".format(value['out_time']))
				else:
					box.insert(END, "Out Time: *not punched*\n")
			box.insert(END, "---------------------------------------\n")
		scrollbar.config( command = box.yview )

############################################
######## GLOBAL INITIALIZATIONS ############
people = dict()
file = open('people.txt', 'r')
data  = file.read()
l = data.split("\n")
for entry in l:
	en, name = entry.split(",")
	people[int(en)] = {'name': name, 'full_days':0, 'half_days':0, 'absent':0}

main_data_frame = None
start_date = None
end_date = None
particular_date = None

scrollbar = Scrollbar(m)
box = Text(m, yscrollcommand = scrollbar.set)
box.place(height=550, width=500, x=600, y=20)
scrollbar.place(height=550, x=1100, y=20)

day_count_box = Listbox(m)
day_count_box.place(height=300, width=200, x=380, y=180)

pm0300 = pd.to_datetime('01-01-2019 15:00:00').strftime("%X")
am1015 = pd.to_datetime('01-01-2019 10:15:00').strftime("%X")
am1030 = pd.to_datetime('01-01-2019 10:30:00').strftime("%X")
pm0555 = pd.to_datetime('01-01-2019 17:55:00').strftime("%X")
pm6000 = pd.to_datetime('01-01-2019 18:00:00').strftime("%X")

############################################
################# GUI ######################
browse_file_button = Button(m, text="browse", command=open_file)
browse_file_button.place(height=50, width=70, x=50, y=50)

browse_file_button = Button(m, text="Reset", command=reset)
browse_file_button.place(height=50, width=70, x=150, y=50)

v = IntVar()
rb1 = Radiobutton(m, text='Check attendance between to dates', variable=v, value=1, command=two_fields)
rb2 = Radiobutton(m, text='Check In/Out time on a particular date', variable=v, value=2, command=one_field)
rb1.place(x=10, y=200)
rb2.place(x=10, y=230)

e1 = tk.Entry(m)
e2 = tk.Entry(m)
l1 = tk.Label(m, text='Start Date(dd-mm-yyyy): ')
l2 = tk.Label(m, text='End Date(dd-mm-yyyy): ')
b1 = tk.Button(m, text="Get Attendance", command=get_attendance)

e3 = tk.Entry(m)
l3 = tk.Label(m, text='Date(dd-mm-yyyy): ')
b2 = tk.Button(m, text="Get In/Out Time", command=get_time)

m.mainloop()