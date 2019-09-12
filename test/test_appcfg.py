# -*- encoding: UTF-8 -*-
import os
import unittest

from eplus.appcfg_update import get_unniq_target_yaml


class TestAppcfg(unittest.TestCase):

    def test_target_yaml(self):
        fn = get_unniq_target_yaml('app.yaml')
        self.assertFalse(os.path.isfile(fn))






