# -*- encoding: UTF-8 -*-
import os
import sys
import unittest

from eplus.appcfg_update import get_unniq_target_yaml, simulate_legacy_update
from eplus.environment import init, init_lib


class TestAppcfg(unittest.TestCase):

    def setUp(self):
        init()
        init_lib()

        # noinspection PyUnresolvedReferences,PyPackageRequirements
        import gcloud
        import fake
        gcloud._import_gcloud_main = lambda *args: fake
        sys.exit = lambda *args: None


    def test_main_is_callable(self):
        # noinspection PyUnresolvedReferences,PyPackageRequirements
        from gcloud import main
        main()


    def test_basic_e2e(self):

        sys.argv = ['appcfg_update', 'test.yaml']
        simulate_legacy_update()

        from fake import argv
        self.assertIn('gcloud', argv)
        self.assertEqual(['gcloud', 'app', 'deploy'], argv[:3])
        self.assertIn('--project=move_it_to_args', argv)


    def test_target_yaml(self):
        fn = get_unniq_target_yaml('app.yaml')
        self.assertFalse(os.path.isfile(fn))

