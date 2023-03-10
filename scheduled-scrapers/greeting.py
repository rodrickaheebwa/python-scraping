from datetime import date

file_path = 'C:/Users/rodri/Desktop/today.txt'
today = date.today().strftime("%A %d %B %Y")

with open(file_path, 'a') as f:
    f.write('\nGood morning Rodrick! Today is ' + today +  '\n')