from jinja2 import Template

__version__ = "0.0.1"

SETUP_FILE_TEMPLATE = Template("""
from distutils.core import setup

from {{projname}} import __version__ as VERSION

def _find_packages(root_package):
    root_dir = os.path.dirname(__file__)
    package_root = os.path.abspath(os.path.join(root_dir, root_package))
    yield root_package
    for directory, dirnames, filenames in os.walk(package_root):
        if "__init__.py" not in filenames:
            del dirnames[:]
        else:
            relative_package = os.path.relpath(directory, package_root).replace(os.path.sep, ".")
            if relative_package == '.':
                continue
            yield root_package + "." + relative_package


setup(name="{{projname}}",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python :: {{pyversion}}",
          ],
      description="{{description}}",
      #license="Proprietary",
      author="{{author}}",
      author_email="{{author_email}}",
      #url="your.url.here",
      version=VERSION,
      packages=list(_find_packages("{{projname}}")),
      scripts=[],
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
