"""
Class for getting changes from a git repository
"""
__author__ = 'tinglev@kth.se'

import os
import logging
from everest_util.process import Process

class GitException(Exception):
    """
    Exception raised when something goes wrong during git fetching
    """
    pass

class Git(object):
    """
    Class for interfacing with git
    """

    def __init__(self, repo_path, git_url):
        """
        Constructor
        Args:
            repo_path: local directory path to place git repo when fetched
            gir_url: the url to the git repo (for instance 'gita.sys.kth.se/Infosys/dizin')
        """
        self.log = logging.getLogger(__name__)
        self.git_url = git_url
        self.repo_path = repo_path
        self.log.debug('Git module initialized with git url "%s" and repo path "%s"',
                       self.git_url, self.repo_path)

    def create_repo_dir_if_missing(self):
        """
        Creates the local repo directory if it's missing
        Returns:
            Nothing
        """
        if not os.path.isdir(self.repo_path):
            self.log.debug('Git repo path was missing - creating it..')
            os.makedirs(self.repo_path)

    def clone(self):
        """
        Clones the given git repo to disk. Also creates the local repo directory
        if it is currently missing.
        Returns:
            string: the output from the git clone command
        """
        self.create_repo_dir_if_missing()
        return Process.run_with_output('git clone git@{} {}'
                                        .format(self.git_url,
                                                self.repo_path))

    def reset(self):
        """
        Resets the local git repository
        Returns:
            string: the ouput from the git reset command
        """
        return Process.run_with_output('git --work-tree={0} --git-dir={0}/.git reset '
                                       '--hard FETCH_HEAD'
                                       .format(self.repo_path))

    def fetch(self):
        """
        Fetches the latest version of the remote git repo
        Returns:
            string: the output from the git fetch command
        """
        return Process.run_with_output('git --work-tree={0} --git-dir={0}/.git fetch origin master'
                                       .format(self.repo_path))

    def clean(self):
        """
        Cleans the local git repo
        Returns:
            string: the output from the git clean command
        """
        return Process.run_with_output('git --work-tree={0} --git-dir={0}/.git clean -df'
                                       .format(self.repo_path))

    def get_latest_changes(self):
        """
        Chains clone, fetch, reset and clean to get all the latest changes from the remote
        git repo
        Returns:
            string: the combined output of all the git commands run
        Raises:
            GitException: when an error is encountered during one of the git commands
        """
        try:
            return '{}{}{}{}'.format(self.clone(), self.fetch(), self.reset(), self.clean())
        except Exception as exc:
            raise GitException('Failed to fetch git changes', ex=exc)