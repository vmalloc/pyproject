import os
from setuptools import setup
with open(os.path.join(os.path.dirname(__file__), "pyproject", "__version__.py"), "rb") as version_file:
    exec(version_file.read())

setup(name="pyproject",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: 2.6",
          ],
      description="Tool for creating new python packages",
      license="BSD",
      author="Rotem Yaari",
      author_email="vmalloc@gmail.com",
      url="http://github.com/vmalloc/pyproject",
      version=__version__,
      packages=["pyproject"],
      entry_points = dict(
        console_scripts = [
              "start_python_project = pyproject.start:main_entry_point",
              "bump_version = pyproject.bump:main_entry_point",
              ]
        ),
      install_requires=["jinja2"]
      )
