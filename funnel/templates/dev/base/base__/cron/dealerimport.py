import MySQLdb
import hashlib
class dealerimport:
    def __init__(self):
        self.dealer = {}
    def connect_database(self,flag = 1):
        if flag == 1:
            self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer')
            self.cursor = self.db.cursor()
        else:
            self.db     = MySQLdb.connect('localhost','khalidfunnel','!7hGes20','admin_app')
            self.cursor = self.db.cursor()    
    def close_database(self):
        self.cursor.close()
        self.db.close()
    def getDealerFromConsumer(self):
        self.connect_database()
        sql =  "select * from dealers"
        self.cursor.execute(sql)
        self.dealer = self.cursor.fetchall() 
        self.close_database()
    def insert(self,table,dict,cursor,db):
        keylist            = []
        valuelist          = []
        for key,value in dict.iteritems():
            if value       != '':
                keylist.append(key)
                p          = "'" + str(value) + "'"
                valuelist.append(p)
        sql                = "INSERT INTO " + table + '('+','.join(keylist)+')'+'VALUES ('+','.join(valuelist)+')'
        
        cursor.execute(sql)
        db.commit()
        
        return               cursor.lastrowid    
    def convertstr(self,var):
        return var.replace("'","\\'")
    def stringtohash(self,val):
        return hashlib.sha224(val).hexdigest()
    def insertDealer(self):
        self.connect_database(2)
        for n in self.dealer:
            sql = "select * from funnel_dealer where consumer_dealerid = %s" % n[0]
            self.cursor.execute(sql)
            if self.cursor.rowcount == 0:
                   dict = {}
                   dict['consumer_dealerid'] = n[0]
                   dict['name']    = self.convertstr(n[1])
                   dict['address'] = n[2]
                   dict['city']    = n[3]
                   dict['state']   = n[4]
                   dict['zip']     = n[5]
                   dict['status']  = n[6]
                   temp = {"sale_contact":"","sale_title":"","sale_phone":"","service_contact":"","service_title":"","service_phone":"","trade_contact":"","trade_title":"","trade_phone":""} 
                   dict['contact_id']  = self.insert('funnel_dealer_contact',temp,self.cursor,self.db)
                   temp = {"sales_regular_hour_from":"","sales_sunday_hour_from":"","sales_saturday_hour_from":"","sales_regular_hour_to":"","sales_sunday_hour_to":"","sales_saturday_hour_to":"","service_regular_hour_from":"","service_sunday_hour_from":"","service_saturday_hour_from":"","service_regular_hour_to":"","service_sunday_hour_to":"","service_saturday_hour_to":""} 
                   dict['hour_id']  = self.insert('funnel_dealer_hour',temp,self.cursor,self.db)
                   temp = {"triggers_budget":0,"triggers_email":0,"triggers_pieces":0,"trigger_cost_per_pieces":0,"trigger_trade_cycle":0,"trigger_birthday":0,"trigger_new_purchase":0,"trigger_equity_position":0,"trigger_fst_service":0,"trigger_warranty_expiration":0,"trigger_overdue_services":0,"trigger_make_conquest":0,"trigger_crossover_conquest":0} 
                   dict['trigger_id']  = self.insert('funnel_dealer_trigger',temp,self.cursor,self.db)
                   temp = {"logo":"","manufacture":""} 
                   dict['logo_id']  = self.insert('funnel_dealer_logo',temp,self.cursor,self.db)
                   temp = {"forwardnumber":"","outofmarketdistance":"","color":""} 
                   dict['attr_id']  = self.insert('funnel_dealer_attr',temp,self.cursor,self.db)
                   id = self.insert('funnel_dealer',dict, self.cursor, self.db)
                   dict = {"keyid":self.stringtohash("dealer_%s" % id),"groupname":"Dealer","groupid":id}
                   self.insert('funnel_hash',dict, self.cursor, self.db)

cron = dealerimport()
cron.getDealerFromConsumer()
cron.insertDealer()
                                  