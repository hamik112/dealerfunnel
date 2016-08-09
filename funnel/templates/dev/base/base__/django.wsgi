import os, sys
sys.path.append('/var/www/vhosts/dealerfunnel.com/dealerfunnel')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dealerfunnel.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
