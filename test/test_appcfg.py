# -*- encoding: UTF-8 -*-
import os
import unittest

from eplus.appcfg_update import get_unniq_target_yaml


class TestAppcfg(unittest.TestCase):

    def test_shutterstock_image(self):
        fn = get_unniq_target_yaml('app.yaml')
        self.assertFalse(os.path.isfile(fn))






