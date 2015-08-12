# -*- encoding: UTF-8 -*-

import os
import sys


GAE_SDK_ROOT = os.environ.get('GAE_SDK_ROOT', '/opt/google_appengine')
APP_YAML_FILE = 'app-local.yaml'


if 'google' in sys.modules:
    del sys.modules['google']

sys.path.append(GAE_SDK_ROOT)
from dev_appserver import fix_sys_path
fix_sys_path()



import yaml
from google.appengine.api import apiproxy_stub_map
from google.appengine.api import appinfo



app_root = os.path.dirname(__file__)


dbpath = "../var/datastore.sqlite"
search_index = "../var/index"
blobstore_path = "../var/blobs"


# os.environ['APP_SETTINGS'] = 'local'


with open(APP_YAML_FILE, 'r') as f:
    app_yaml = yaml.load(f)
    app_environ = app_yaml.get(appinfo.ENV_VARIABLES)
    if app_environ:
        os.environ.update(app_environ)


# load app.yaml config
app_ext_info = appinfo.LoadSingleAppInfo(file(APP_YAML_FILE, 'r'))
app_id = 'dev~%s' % app_ext_info.application


# set the app ID to make stubs happy, esp. datastore
os.environ['APPLICATION_ID'] = app_id
os.environ['AUTH_DOMAIN'] = 'localhost'
os.environ['SERVER_NAME'] = 'localhost'
os.environ['SERVER_PORT'] = '8080'



# from google.appengine.tools.devappserver2.devappserver2 import _get_storage_path
# dbpath = _get_storage_path(app_id=app_id)
# print 'dbpath:%s' % dbpath


# Init the proxy map and stubs
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()


from google.appengine.api.app_identity import app_identity_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'app_identity_service',
    app_identity_stub.AppIdentityServiceStub()
)

from google.appengine.api.capabilities import capability_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'capability_service',
    capability_stub.CapabilityServiceStub()
)

# DB
from google.appengine.datastore import datastore_sqlite_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'datastore_v3',
    datastore_sqlite_stub.DatastoreSqliteStub(app_id, dbpath)
)

# Memcache
from google.appengine.api.memcache import memcache_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'memcache',
    memcache_stub.MemcacheServiceStub()
)

# Task queues
from google.appengine.api.taskqueue import taskqueue_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'taskqueue',
    taskqueue_stub.TaskQueueServiceStub()
)

# URLfetch service
from google.appengine.api import urlfetch_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'urlfetch',
    urlfetch_stub.URLFetchServiceStub()
)

# Search service
from google.appengine.api.search import simple_search_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'search',
    simple_search_stub.SearchServiceStub(index_file=search_index)
)



from google.appengine.api.blobstore import file_blob_storage
blob_storage = file_blob_storage.FileBlobStorage(blobstore_path, app_id)

from google.appengine.api.blobstore import blobstore_stub
apiproxy_stub_map.apiproxy.RegisterStub(
    'blobstore',
    blobstore_stub.BlobstoreServiceStub(blob_storage)
)



# from google.appengine.api.xmpp import xmpp_service_stub
# apiproxy_stub_map.apiproxy.RegisterStub(
#     'xmpp',
#     xmpp_service_stub.XmppServiceStub()
# )




def on_exit(self):

    try:
        from google.appengine.tools.dev_appserver import TearDownStubs
    except ImportError:
        from google.appengine.tools.old_dev_appserver import TearDownStubs

    TearDownStubs()
    print 'TearDownStubs'
    self.exit_now = True

try:
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
except ImportError:
    # noinspection PyUnresolvedReferences
    from IPython.frontend.terminal.interactiveshell import TerminalInteractiveShell

TerminalInteractiveShell.ask_exit = on_exit



######################

import json
import uuid
import logging
import urllib
from conf import settings

from google.appengine.api import urlfetch


# from services.models import *
# from admin.handlers import QueryFetcher



logging.getLogger().setLevel(logging.DEBUG)


# import logging
# logging.basicConfig(level=logging.DEBUG,
# format='%(asctime)s %(name)s %(levelname)s %(message)s',
# datefmt='%H:%M:%S',
# stream=sys.stderr
# )


# import logging
# logging.basicConfig(level=logging.DEBUG,
# format='%(asctime)s %(name)18s %(levelname)-6s %(message)s',
# datefmt='%H:%M:%S',
# filename=os.path.abspath('./../debug.log'),
# filemode='w')
