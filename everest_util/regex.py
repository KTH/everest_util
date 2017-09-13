"""
Module containing various regex patterns used with the everest ecosystem
"""
__author__ = 'tinglev@kth.se'

class Regex(object):
    """
    Static class containing the regex patterns
    """

    @staticmethod
    def get_label_and_env_regex():
        """
        Matches the label and value of an environment variable

        Valid examples:
            ABC=123
            ABC="HELLO SPACE"
        """
        return r'[^\s#="]+=(([^\s#="]+)|(".+"))$'

    @staticmethod
    def get_cellus_registry_cluster():
        """
        Matches the cluster name from a cellus-registry directory path

        Valid example:
            ../deploy/dizin/[cluster]/..
        """
        return r'^.+/deploy/.+/(.+)/.+$'

    @staticmethod
    def get_env_var_dereference_regex():
        """
        Matches an environment variable dereferencing

        Valid example:
            ${ABC}
        """
        return r'^\$\{([a-zA-Z0-9_]+)\}$'

    @staticmethod
    def get_image_and_registry_regex():
        """
        Matches an image reference, used in docker-stack file (among others)

        Valid example:
            private.registry.kth.se/dizin:1.2.23_abcdefg
        """
        return r'^(.+)/(.+):(.+)$'

    @staticmethod
    def get_image_parts_regex():
        """
        Matches the name and version of an image

        Valid example:
            /dizin:1.2.23_abcdefg
        """
        return r'^(.+/){0,1}(.+):(.+)$'

    @staticmethod
    def get_semver_version_regex():
        """
        Matches a semver version notation for and image

        Valid examples:
            ^1.2.23_abcdefg
            ~0.19.1
        """
        return r'^[\~\^]{1}(0|[1-9][0-9]*)\.([0-9]+)\.([0-9]+)((_.*){0,1})$'

    @staticmethod
    def get_static_version_regex():
        """
        Matches a normal image version on the format major.minor.build_optionalhash

        Valid examples:
            1.2.34_abcdefgh
            0.1.123
        """
        return r'^(0|[1-9][0-9]*)\.([0-9]+)\.([0-9]+)((_.*){0,1})$'
