import pandas as pd
import datadotworld as dw
import tkinter as tk
from tkinter import ttk
import csv
from datetime import date
from datetime import timedelta

    # open and format data world sql query. 
file = open("C:/Users/Riesser/Documents/python_popup/dw_pull.txt")
line = file.read().replace("\n", " ") 

    #remove white space and create a string value
line = ' '.join(line.split())
file.close()

	#run query with "line" variable
results = dw.query('associatedpress/johns-hopkins-coronavirus-case-tracker', line)
df = results.dataframe
	
	#read temp file with data for testing
# df = pd.read_csv('temp.csv')
# df = df.drop('Unnamed: 0', 1)

    #create variable and column for today's date
today = date.today()
df['recorded_date'] = today


	# append dataset into older data
df.to_csv('C:/Users/Riesser/Documents/python_popup/df_storage.csv', mode='a', header=False)



	#remove duplicates from storage file 
df_clean = pd.read_csv('C:/Users/Riesser/Documents/python_popup/df_storage.csv')
df_clean = df_clean.drop('Unnamed: 0', 1)
df_clean = df_clean.drop_duplicates(keep = 'last')
df_clean.to_csv('C:/Users/Riesser/Documents/python_popup/df_storage.csv')

	#find yesterday and convert to datetime
yesterday = today - timedelta(days = 1) 
yesterday = pd.to_datetime(yesterday, format='%Y-%m-%d')

	#convert recorded date to string on both dataframes
df_clean['recorded_date'] = pd.to_datetime(df_clean['recorded_date'], format='%Y-%m-%d')
df['recorded_date'] = pd.to_datetime(df['recorded_date'], format='%Y-%m-%d')

	#filter df_clean 
df_clean = df_clean[df_clean['recorded_date'] == yesterday]
df_clean = df_clean.drop(['confirmed_per_100000', 'deaths', 'recorded_date'], 1)
df_clean.rename(columns={'confirmed':'confirmed_yesterday'}, inplace=True)
df_clean = df_clean.groupby(['state', 'county_name'])
df_clean = df_clean.max()
df_clean = df_clean.reset_index()


	#join df with df clean
df = df.merge(df_clean, how='left', left_on=['state', 'county_name'], right_on=['state', 'county_name'])

	#calculate daily difference
df['daily_difference'] = df['confirmed'] - df['confirmed_yesterday']
df = df.drop(['recorded_date'], 1)

#sort table by most new cases today. 
df = df.sort_values(by=['daily_difference'], ascending=False)


	#add new row to server as header row
new_row = pd.DataFrame({'state':'state', 'county_name':'county','confirmed':'confirmed','confirmed_per_100000':'per_capita','deaths':'deaths' ,'confirmed_yesterday':'yesterday','daily_difference':'new_today'}, index =[0] )
df = pd.concat([new_row, df[:]]).reset_index(drop = True)




	#start tkinter here
	# --- functions ---

def change(event, row, col):
    # get value from Entry
    value = event.widget.get()
    # set value in dataframe
    df.iloc[row,col] = value
    print(df)

	# --- main --    

root = tk.Tk()

	# create entry for every element in dataframe

rows, cols = df.shape

for r in range(rows):
    for c in range(cols):
        e = tk.Entry(root)
        e.insert(0, df.iloc[r,c])
        e.grid(row=r, column=c)
        # ENTER 
        e.bind('<Return>', lambda event, y=r, x=c: change(event,y,x))
        # ENTER on keypad
        e.bind('<KP_Enter>', lambda event, y=r, x=c: change(event,y,x))

	# start program


	#add code to shut down program after 30 seconds
	#root.after(60000, lambda: root.destroy()) # added 6/27/2020

root.mainloop()