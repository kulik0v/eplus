# -*- encoding: UTF-8 -*-

from .utils.find_embed import embed
from .utils.environment import init, tear_down


def main():
    print 'QQ'
    init()
    embed()
    tear_down()


if __name__ == '__main__':
    main()
