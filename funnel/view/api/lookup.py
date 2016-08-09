from dealerfunnel.funnel.view.base import *
from django.core import serializers
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.library.common import *
import json
import pdb
from dealerfunnel.funnel.library.dateformate import *
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
import operator
import time
from django.db import connection
from dealerfunnel.funnel.model_plugin.campaign_model import *
from pymongo import MongoClient
from bson.objectid import ObjectId
from dealerfunnel.funnel.model_plugin.yearmakemodel_model import yearmakemodel
import pymongo
class lookupapi:
      def getYear(self,request):
          dict              = []
          dict['year']      = yearmakemodel().getYear()
          return HttpResponse(json.dumps(dict))      
      def getMake(self,request):
          year              = int(request.GET['year'])
          dict              = {}
          dict['make']      = yearmakemodel().getMake(year)
          return HttpResponse(json.dumps(dict))
      def getModels(self,request):
          year              = int(request.GET['year'])
          make              = request.GET['make']
          dict              = {}
          dict['model']     = yearmakemodel().getModel(year,make)
          return HttpResponse(json.dumps(dict))                
                          