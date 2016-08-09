import datetime
import calendar
import time  
class dateformateclass:
    def __init__(self):
        self.FORMATE1 = ['Y','M','D']
        self.FORMATE2 = ['M','D','Y']
        self.FORMATE3 = ['D','M','Y']
        self.GLUE1    = '-' # - 
        self.GLUE2    = '/' # /
    def getdateformate(self,date):
        lst = {}
        lst['d'] = date.strftime("%d")
        lst['a'] = date.strftime("%a")
        lst['A'] = date.strftime("%a")
        lst['w'] = date.strftime("%w")
        lst['b'] = date.strftime("%b")
        lst['B'] = date.strftime("%B")
        lst['m'] = date.strftime("%m")
        lst['y'] = date.strftime("%y")
        lst['Y'] = date.strftime("%Y")
        lst['H'] = date.strftime("%H")
        lst['I'] = date.strftime("%I")
        lst['p'] = date.strftime("%p")
        lst['U'] = date.strftime("%U")
        return lst
    def getTimeStamp(self,datetime):
        return int(time.mktime(datetime.timetuple()) * 1000)     
    def date_obj(self,str):
        split = str.split('-')
        return datetime.date(int(split[0]),int(split[1]),int(split[2]))
    def datetime_obj(self,str):
        split = str.split(' ')
        date  = split[0]
        time  = split[1]
        date_split = date.split('-')
        time_split = time.split(':')
        return datetime.datetime(int(date_split[0]),int(date_split[1]),int(date_split[2]),int(time_split[0]),int(time_split[1]))
    def getdate_obj(self,year,month,day):
        return datetime.date(int(year),int(month),int(day))
    def backdate(self,start,end):
        date           = {}
        diff           = self.datediff(end,start)
        date['end']    = start - datetime.timedelta(1)
        date['start']  = date['end'] - datetime.timedelta(diff) 
        return date
    
    def getformate(self,date,formate,glue):
        dict = {}
        i    = 0
        formated = date.split(glue)
        for n in formated:
            dict[formate[i]] = n
            i = i+1
        return datetime(int(dict['Y']),int(dict['M']),int(dict['D']),0,0)
    
    def getformatewithtime(self,datetime,formate,glue):
        dict = {}
        i    = 0
        timeformate = datetime.split(" ")
        formated    = timeformate[0].split(glue)
        time        = timeformate[1].split(":")
        for n in formated:
            dict[formate[i]] = n
            i = i+1
        return datetime(int(dict['Y']),int(dict['M']),int(dict['D']),int(time[0]),int(time[1]))
    def datediff(self,a,b):
        delta = a - b
        return delta.days
    
    def strday(self,val):
        v = int(val)
        flag =  True
        list = ['','st','nd','rd']
        if v >= 1 and v <=3:
            flag = False
            return str(v) + list[v]
        if v >= 21 and v <=23:
            flag = False
            k = v % 20 
            return str(v) + list[k]
        if flag:
            return str(v) + 'th'
        
    def date_sequence(self,start,end):
        start_date = start
        end_date   = end
        diff = end_date - start_date
        n    = 0 
        items = []
        strdate = []
        rdata = []
        for i in range(diff.days + 1):
            list = []
            date = start_date + datetime.timedelta(i)
            list.append(date)
            list.append(date)
            day = date.strftime('%b') + ' '+self.strday(date.strftime('%d'))
            items.append(list)
            strdate.append(day)
        rdata.append(items)
        rdata.append(strdate)
        return rdata
    
    def date_week(self,start,end):
        items = []
        strdate = []
        rdata = []
        s =  start
        s_d  = s.strftime('%b') + ' '+self.strday(s.strftime('%d')) 
        e =  end
        e_d  = e.strftime('%b') + ' '+self.strday(e.strftime('%d')) 
        w =  s + datetime.timedelta(6)
        w_d  = w.strftime('%b') + ' '+self.strday(w.strftime('%d'))
        while(w <= e):
            item = []
            item.append(s)
            item.append(w)
            items.append(item)
            strdate.append(s_d + ' To '+w_d)
            s    = w + datetime.timedelta(1)
            s_d  = s.strftime('%b') + ' '+self.strday(s.strftime('%d')) 
            w    = s + datetime.timedelta(6)
            w_d  = w.strftime('%b') + ' '+self.strday(w.strftime('%d'))
        if w > s:
           item = []
           item.append(s)
           item.append(e)
           items.append(item)
           strdate.append(s_d + ' To '+e_d) 
        rdata.append(items)
        rdata.append(strdate)
        return rdata
    def date_month(self,start,end):
        items = []
        strdate = []
        rdata = []
        s =  start
        e =  end
        start = s
        end   = e  
        counter = start
        while(counter<=e):
            item = []
            maxDay = calendar.monthrange(counter.year, counter.month)[1]
            if counter.month == start.month and counter.year == start.year:
                chunkStart = datetime.date(counter.year,counter.month,counter.day)
            else:
                chunkStart = datetime.date(counter.year,counter.month, day=1)
            if counter.month == end.month and counter.year == end.year:
                chunkEnd = datetime.date(counter.year,counter.month,end.day)
            else:
                chunkEnd = datetime.date(counter.year,counter.month,maxDay)
            counter += datetime.timedelta(days=maxDay)
            item.append(chunkStart)
            item.append(chunkEnd)
            items.append(item)
            strdate.append(chunkStart.strftime("%b") + ' '+chunkStart.strftime("%Y"))
        rdata.append(items)
        rdata.append(strdate)
        return rdata  
   
            