import urllib2
import urllib
import json
import unirest
class geocode:
    def __init__(self,zip1,zip2=''):
        self.zip1   = zip1
        self.zip2   = zip2
        self.key   = 'AIzaSyAPJzJJ2W3NhCo7jwaQJqvPdZdJoem27Ss'
    def isset(self,variable):
        return variable in locals() or variable in globals()
    def getlatlng(self):
        response = unirest.get("https://redline-redline-zipcode.p.mashape.com/rest/info.json/"+ str(self.zip1) +"/degrees",
        headers={
                "X-Mashape-Key": "VxqTwZsHqomshtOynyJnIUGYbyolp1eZz09jsnIqzhNjaepf1Y",
                "Accept": "application/json"
                })
        latlng = [0,0]                       
        if 'error_code' in response.body:
            return latlng
        else:
            latlng[0] = response.body['lat']
            latlng[1] = response.body['lng']
            return latlng
    
    def distance(self):
         response = unirest.get("https://redline-redline-zipcode.p.mashape.com/rest/distance.json/" + str(self.zip1) + "/" + str(self.zip2) + "/km",
         headers={
                   "X-Mashape-Key": "VxqTwZsHqomshtOynyJnIUGYbyolp1eZz09jsnIqzhNjaepf1Y",
                   "Accept": "application/json"
                 })
         if 'error_code' in response.body:
            return -1
         else:
            return response.body['distance']     
                    