import os
import itertools
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "pyproject", "__version__.py")) as version_file:
    exec(version_file.read())

setup(name="pyproject",
      classifiers = [
          "Programming Language :: Python :: 2.7",
          ],
      description="Tool for creating new python packages",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      install_requires=[
          "Jinja2",
      ],
      zip_safe=False,
      entry_points = dict(
          console_scripts = [
              "start_python_project = pyproject.entry_point:main_entry_point",
              "bump_version = pyproject.bump_version:main_entry_point",
              ]
          ),

      namespace_packages=[]
      )
