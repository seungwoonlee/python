import csv
 
f = open('csv-test.csv', 'rb')
rdr = csv.reader(f)
for line in rdr:
    print line
f.close() 


cities = ['Seoul', 'Suwon', 'Gumi']
f = open('csv-test2.csv', 'wb')
w = csv.writer(f)
for i in cities:
    w.writerows(['Seoul'])
f.close()