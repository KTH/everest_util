__author__ = 'tinglev@kth.se'

from setuptools import setup
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

pipfile = Project().parsed_pipfile
requirements = convert_deps_to_pip(pipfile['packages'], r=False)
#test_requirements = convert_deps_to_pip(pipfile['dev-packages'], r=False)

setup(name='everest_util',
      version='1.0',
      description='Utility library for KTHs CD/CI pipeline',
      url='http://github.com/KTH/everest_util',
      author='tinglev',
      author_email='tinglev@kth.se',
      license='MIT',
      packages=['everest_util'],
      zip_safe=False,
      install_requires=requirements)
