
import json
import csv
import urllib.request
 
 
# Opening JSON file and loading the data
# into the variable data
school_url = "https://gpa.obec.go.th/reportdata/pp3-4_2566_province.json"
with urllib.request.urlopen(school_url) as url:
    sdata = json.loads(url.read().decode())
 
employee_data = sdata

 
# now we will open a file for writing
data_file = open('student.csv', 'w', encoding='utf-8')
 
# create the csv writer object
csv_writer = csv.writer(data_file)
 
# Counter variable used for writing 
# headers to the CSV file
count = 0
 
for emp in employee_data:
    if count == 0:
 
        # Writing headers of CSV file
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1
 
    # Writing data of CSV file
    csv_writer.writerow(emp.values())
 
data_file.close()