from datetime import date

file_path = 'C:/Users/rodri/Desktop/today.txt'
today = date.today().strftime("%A %d %B %Y")

with open(file_path, 'a') as f:
    f.write('\nGood morning Rodrick! Today is ' + today +  '\n')


# ubuntu
"""
import datetime

today_date = datetime.date.today().strftime("%A %d %B %Y")
now_time = datetime.datetime.now().time().strftime("%I : %M %p")
file_path = '/home/rodrick/Desktop/python-scheduling/greeting.txt'

with open(file_path, 'a') as f:
    f.write(f'Hello Rodrick!. The date is {today_date} and the time is {now_time}.\n')
"""