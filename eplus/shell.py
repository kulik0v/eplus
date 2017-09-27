# -*- encoding: UTF-8 -*-

from .embed import embed
from .environment import init, setup_local, tear_down_local, setup_remote


def shell_local():
    init()
    setup_local()
    embed()
    tear_down_local()


def shell_remote():
    init()
    setup_remote()
    embed()


if __name__ == '__main__':
    shell_local()
