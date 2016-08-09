import MySQLdb
>>> from customer_analysis import *
>>> db = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
>>> cur = db.cursor()
>>> customer_analysis(3,db,cur).run()
