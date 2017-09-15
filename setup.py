__author__ = 'tinglev@kth.se'

from setuptools import setup
from pipenv.project import Project

lockfile = Project().lockfile_content
requirements = [package for (package, _) in lockfile['default'].iteritems()]

setup(name='everest_util',
      version='1.1',
      description='Utility library for KTHs CD/CI pipeline',
      url='http://github.com/KTH/everest_util',
      author='Jens Tinglev',
      author_email='tinglev@kth.se',
      license='MIT',
      packages=['everest_util', 'everest_util.systems', 'everest_util.entities'],
      zip_safe=False,
      install_requires=requirements)
