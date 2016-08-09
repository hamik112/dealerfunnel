import csv
import MySQLdb
from common import *
db = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
cursor        = db.cursor()
f = open('yearmakes.csv')
csv_f = csv.reader(f)

for row in csv_f:
  if len(row) == 3: 
      dict = {}
      dict['year']  = row[0]
      dict['make']  = row[1]
      dict['model'] = row[2]
      common().insert('funnel_makesmodel', dict, cursor,db)
  
print 'Done'           