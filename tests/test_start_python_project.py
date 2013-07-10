from tempfile import mkdtemp
from unittest import TestCase
import pyproject
from pyproject.factory import create_package
import os
import shutil
import uuid

class StartPythonPrjectTest(TestCase):
    def setUp(self):
        super(StartPythonPrjectTest, self).setUp()
        self.parent_path = mkdtemp()
        self.addCleanup(shutil.rmtree, self.parent_path)
        self.package_name = str(uuid.uuid1()).replace("-", "_")
        self.path = os.path.join(self.parent_path, self.package_name)
        create_package(
            self.path,
            {
                "author_fullname": "John Doe",
                "year": 2005,
                "github_username": "vmalloc",
                "author_email": "johndoe@mail.com",
                "url": "some_url",
                "name": self.package_name,
                "license_name": "BSD3",
                "description": "Some description",
                "supported_versions": ["2.6", "2.7", "3.3"],
            }
        )

    def test_directory_listing_in_root(self):
        expected = set(os.listdir(os.path.join(os.path.dirname(pyproject.__file__), "_skeleton")))
        expected.remove("{{name}}")
        expected.add(self.package_name)
        for x in list(expected):
            if x.endswith(".j2"):
                expected.remove(x)
                expected.add(x[:-3])
        self.assertItemsEqual(os.listdir(self.path), expected)
