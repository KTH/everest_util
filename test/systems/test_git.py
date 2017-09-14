__author__ = 'tinglev@kth.se'

import tempfile
import unittest
import shutil
import os
from everest_util.systems.git import Git, GitException

class GitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def test_0_git_clone(self):
        git = Git(self.temp_dir, 'https://github.com/KTH/everest_util')
        git.clone()

    def test_1_git_fetch(self):
        git = Git(self.temp_dir, 'https://github.com/KTH/everest_util')
        git.fetch()

    def test_2_git_reset(self):
        git = Git(self.temp_dir, 'https://github.com/KTH/everest_util')
        git.reset()

    def test_3_git_clean(self):
        git = Git(self.temp_dir, 'https://github.com/KTH/everest_util')
        git.clean()

    def test_4_asserts(self):
        self.assertTrue(os.path.isfile('{}/Pipfile'
                                       .format(self.temp_dir)))
