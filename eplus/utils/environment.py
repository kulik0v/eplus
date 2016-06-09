# -*- encoding: UTF-8 -*-

import os
import sys

GAE_SDK_ROOT = os.environ.get('GAE_SDK_ROOT', '/opt/google_appengine')
APP_YAML_FILE = os.path.isfile('app-local.yaml') and 'app-local.yaml' or 'app.yaml'


def init(sdk_root=None):
    if not sdk_root:
        sdk_root = os.environ.get('GAE_SDK_ROOT', '/opt/google_appengine')

    if 'google' in sys.modules:
        del sys.modules['google']

    if sdk_root not in sys.path:
        sys.path.append(sdk_root)

    from dev_appserver import fix_sys_path
    fix_sys_path()



def setup():
    pass




# noinspection PyPackageRequirements
def tear_down():
    try:
        # noinspection PyProtectedMember,PyPep8Naming
        from google.appengine.tools.api_server import _TearDownStubs as TearDownStubs
        # from google.appengine.tools.dev_appserver import TearDownStubs
    except ImportError:
        # noinspection PyPep8Naming,PyUnresolvedReferences
        from google.appengine.tools.old_dev_appserver import TearDownStubs

    TearDownStubs()
