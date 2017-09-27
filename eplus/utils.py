# -*- encoding: UTF-8 -*-

import os


def which(program):
    def is_exe(fxpath):
        return os.path.isfile(fxpath) and os.access(fxpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None



def find_sdk():
    env_sdk = os.environ.get('GAE_SDK_ROOT')
    if env_sdk:
        return env_sdk

    dev_appserver_path = which('dev_appserver.py')

    check_path = os.path.join(
        os.path.dirname(dev_appserver_path),
        '..',
        'platform',
        'google_appengine'
    )
    try:
        os.stat(check_path)
        return check_path
    except OSError:
        pass

    check_path = os.path.join(
        os.path.dirname(dev_appserver_path),
        'google',
        'appengine'
    )
    try:
        os.stat(check_path)
        return dev_appserver_path
    except OSError:
        pass



