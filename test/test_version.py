__author__ = 'tinglev@kth.se'

import unittest
from mock import patch
from everest_util.version import Version, VersionException

class VersionTests(unittest.TestCase):

    def test_semver_max_build(self):
        self.assertTrue(Version._semver_max_build('~1.0.0_abc'))
        self.assertFalse(Version._semver_max_build('^1.0.0_abc'))
        self.assertFalse(Version._semver_max_build('1.0.0_abc'))

    def test_semver_max_minor(self):
        self.assertTrue(Version._semver_max_minor('^1.0.0_abc'))
        self.assertFalse(Version._semver_max_minor('~1.0.0_abc'))
        self.assertFalse(Version._semver_max_minor('1.0.0_abc'))

    def test_is_valid_static(self):
        self.assertTrue(Version._is_valid_static('1.0.0_abc'))
        self.assertTrue(Version._is_valid_static('0.1.0_abc1234'))
        self.assertTrue(Version._is_valid_static('2.1.0'))
        self.assertFalse(Version._is_valid_static('2.1'))
        self.assertFalse(Version._is_valid_static('~2.1'))
        self.assertFalse(Version._is_valid_static('2'))
        self.assertFalse(Version._is_valid_static('abc'))

    def test_is_valid_semver(self):
        self.assertFalse(Version._is_valid_semver('1.0.0_abc'))
        self.assertFalse(Version._is_valid_semver('0.1.0_abc1234'))
        self.assertFalse(Version._is_valid_semver('2.1.0'))
        self.assertFalse(Version._is_valid_semver('2.1'))
        self.assertFalse(Version._is_valid_semver('~2.1'))
        self.assertFalse(Version._is_valid_semver('2'))
        self.assertFalse(Version._is_valid_semver('abc'))
        self.assertFalse(Version._is_valid_semver('^0.1'))
        self.assertTrue(Version._is_valid_semver('^1.1.1_abc1234'))
        self.assertTrue(Version._is_valid_semver('~0.1.10'))
        self.assertFalse(Version._is_valid_semver('^~1.1.1_abc1234'))
        self.assertFalse(Version._is_valid_semver('~~1.1.1_abc1234'))

    def test_get_version_part(self):
        self.assertEqual(Version._get_version_part('1.0.0', 0), '1')
        self.assertEqual(Version._get_version_part('1.0.0', 1), '0')
        self.assertEqual(Version._get_version_part('1.0.2', 2), '2')
        self.assertEqual(Version._get_version_part('~0.0.2', 0), '~0')
        self.assertEqual(Version._get_version_part('^10.0.2', 0), '^10')
        self.assertEqual(Version._get_version_part('^10.0.2', 2), '2')
        self.assertEqual(Version._get_version_part('^10.0.2_abc1234', 2), '2_abc1234')

    def test_get_major(self):
        self.assertEqual(Version._get_major('^10.0.2'), 10)
        self.assertEqual(Version._get_major('10.0.2'), 10)
        self.assertEqual(Version._get_major('~10.0.2_abc1234'), 10)

    def test_get_build(self):
        self.assertEqual(Version._get_build('10.0.1'), 1)
        self.assertEqual(Version._get_build('~10.0.1'), 1)
        self.assertEqual(Version._get_build('10.0.1_abc1235'), 1)

    def test_get_sorted_valid_versions(self):
        versions = ['1.0.0', '2.6.0', '1.0.1', '2.5.1', '10.4.3', '0.5.6', 'invalid']
        result = Version.get_sorted_valid_versions(versions)
        expected = ['10.4.3', '2.6.0', '2.5.1', '1.0.1', '1.0.0', '0.5.6']
        self.assertEqual(result, expected)

    def test_get_best_semver_match(self):
        sorted_versions = ['10.4.3', '2.6.0', '2.5.1', '1.0.1', '1.0.0', '0.5.6']
        semver = '^2.0.0'
        result = Version.get_best_semver_match(sorted_versions, semver)
        self.assertEqual(result, '2.6.0')
        semver = '~2.5.0'
        result = Version.get_best_semver_match(sorted_versions, semver)
        self.assertEqual(result, '2.5.1')
        semver = '^2.5.0'
        result = Version.get_best_semver_match(sorted_versions, semver)
        self.assertEqual(result, '2.6.0')
        semver = '^0.0.0'
        result = Version.get_best_semver_match(sorted_versions, semver)
        self.assertEqual(result, '0.5.6')
