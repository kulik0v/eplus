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


    # find by gcloud
    gcloud_path = which('gcloud')
    if gcloud_path:
        gcloud_path = os.path.realpath(gcloud_path)

        check_path = os.path.join(
            os.path.dirname(gcloud_path),
            '..',
            'platform',
            'google_appengine'
        )
        try:
            os.stat(check_path)
            return check_path
        except OSError:
            pass



    devappserver_path = which('dev_appserver.py')
    if devappserver_path:
        devappserver_path = os.path.realpath(devappserver_path)

        # installed as a part of gcloud from zip file
        check_path = os.path.join(
            os.path.dirname(devappserver_path),
            '..',
            'platform',
            'google_appengine'
        )
        try:
            os.stat(check_path)
            return check_path
        except OSError:
            pass


        # old app engine sdk (1.9.xx) installed from zip file
        check_path = os.path.join(
            os.path.dirname(devappserver_path),
            'google',
            'appengine'
        )
        try:
            os.stat(check_path)
            return os.path.dirname(devappserver_path)
        except OSError:
            pass



