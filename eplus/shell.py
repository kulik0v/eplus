# -*- encoding: UTF-8 -*-

from .embed import embed
from .environment import init, setup_local, tear_down_local, setup_remote, init_lib
from .appcfg_update import simulate_legacy_update


def shell_local():
    init()
    setup_local()
    embed()
    tear_down_local()


def shell_remote():
    init()
    setup_remote()
    embed()


def appcfg_update():
    init()
    init_lib()
    simulate_legacy_update()


if __name__ == '__main__':
    shell_local()
