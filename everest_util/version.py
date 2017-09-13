"""
Module for handling static and semver versioning of docker images
"""
__author__ = 'tinglev@kth.se'

import re
from everest_util.regex import Regex

class VersionException(Exception):
    """
    Raised when an error occurs during processing
    """
    pass

class Version(object):
    """
    Static class
    """

    @staticmethod
    def get_sorted_valid_versions(versions):
        """
        Validates and sorts a list of static versions. Validation is performed against
        Regex.get_static_version_regex()
        Args:
            versions: an array of versions (for instance ['1.2.3_abc', '1.2', 'latest'])
        Returns:
            array: the list of versions sorted, with all invalid versions removed
        """
        versions_to_sort = [version for version in versions if Version._is_valid_static(version)]
        return sorted(versions_to_sort, cmp=Version._sort_compare)

    @staticmethod
    def get_best_semver_match(sorted_valid_versions, semver_string):
        """
        Returns the best match for a given semver version from a list of versions
        Args:
            sorted_valid_versions: a sorted list of valid versions
            semver_string: the semver string to process (for instance '~1.2')
        Returns:
            string: the version in the list that best matches the semver string
        Raises:
            VersionException: on invalid semver_string or if no match was found
        """
        if not Version._is_valid_semver(semver_string):
            raise VersionException('Semver version under service environment is invalid: "{}"'
                                .format(semver_string))
        for ver in sorted_valid_versions:
            max_build = Version._semver_max_build(semver_string)
            max_minor = Version._semver_max_minor(semver_string)
            if Version._get_major(ver) == Version._get_major(semver_string):
                if max_minor:
                    return ver
                if Version._get_minor(ver) == Version._get_minor(semver_string):
                    if max_build:
                        return ver
                    if Version._get_build(ver) == Version._get_build(semver_string):
                        return ver
        raise VersionException('No image found for requested version "{}"'
                            .format(semver_string))

    @staticmethod
    def _is_valid_semver(version_string):
        return re.match(Regex.get_semver_version_regex(), version_string)

    @staticmethod
    def _is_valid_static(version_string):
        return re.match(Regex.get_static_version_regex(), version_string)

    @staticmethod
    def _sort_compare(ver1, ver2):
        if Version._get_major(ver1) == Version._get_major(ver2):
            if Version._get_minor(ver1) == Version._get_minor(ver2):
                return Version._get_build(ver2) - Version._get_build(ver1)
            else:
                return Version._get_minor(ver2) - Version._get_minor(ver1)
        else:
            return Version._get_major(ver2) - Version._get_major(ver1)

    @staticmethod
    def _get_major(version):
        return int(Version._get_version_part(version, 0).lstrip('^').lstrip('~'))

    @staticmethod
    def _get_minor(version):
        return int(Version._get_version_part(version, 1))

    @staticmethod
    def _get_build(version):
        part = Version._get_version_part(version, 2)
        if '_' in part:
            return int(part.split('_')[0])
        return int(part)

    @staticmethod
    def _get_version_part(version, index):
        return version.split('.')[index]

    @staticmethod
    def _semver_max_minor(semver_string):
        return str.startswith(semver_string, '^')

    @staticmethod
    def _semver_max_build(semver_string):
        return str.startswith(semver_string, '~')
