__author__ = 'tinglev@kth.se'

from setuptools import setup, find_packages

requirements = [
      'flask',
      'requests',
      'coloredlogs',
      'pyyaml'
]

setup(
      name='everest_util',
      version='1.1',
      description='Utility library for KTHs CD/CI pipeline',
      url='http://github.com/KTH/everest_util',
      author='Jens Tinglev',
      author_email='tinglev@kth.se',
      license='MIT',
      packages=find_packages(exclude=['test']),
      zip_safe=False,
      install_requires=requirements
)
