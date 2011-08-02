from jinja2 import Template
from .__version__ import __version__

SETUP_FILE_TEMPLATE = Template("""import os
import itertools
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), {% for part in projname_parts%}"{{part}}",{% endfor %} "__version__.py")) as version_file:
    exec version_file.read()

setup(name="{{projname}}",
      classifiers = [
          "Programming Language :: Python :: {{pyversion}}",
          ],
      description="{{description}}",
      license="{{license_name}}",
      author="{{author}}",
      author_email="{{author_email}}",
      version=__version__,
      packages=find_packages(exclude=["tests"]),
      install_requires=[],
      scripts=[],
      namespace_packages=[{% for ns_package in ns_packages%}"{{ns_package}}",{% endfor %}]
      )

""")


DOCTEST_TEST_FILE_TEMPLATE = Template("""from unittest import TestCase
import os
import doctest

class ReadMeDocTest(TestCase):
    def test__readme_doctests(self):
        readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.rst"))
        self.assertTrue(os.path.exists(readme_path))
        result = doctest.testfile(readme_path, module_relative=False)
        self.assertEquals(result.failed, 0, "%s tests failed!" % result.failed)
""")
