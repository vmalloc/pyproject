# -*- mode: python -*-
from __future__ import print_function
import time
import os
import posix
from platform import python_version
from optparse import OptionParser
from . import SETUP_FILE_TEMPLATE
from . import DOCTEST_TEST_FILE_TEMPLATE
from .licenses import LICENSES

parser = OptionParser("%prog [options...] directory")
parser.add_option("-d", "--defaults", action="store_true", dest="defaults", default=False)
parser.add_option("-n", "--namespace", action="store_true", default=False, dest="create_namespace_packages")

def create_directory(options, directory, params):
    _try_makedirs(directory)
    projname_parts = params['projname'].split(".")
    _create_main_structure(options, directory, projname_parts)
    for subdir in ['scripts', 'tests']:
        _try_makedirs(os.path.join(directory, subdir))
    with open(os.path.join(directory, "README.rst"), 'wb') as readme_file:
        pass
    render_setup_file(directory, params)
    render_license_file(directory, params)
    render_tox_file(directory, params)
    create_tests_directory(directory, params)

def _create_main_structure(options, directory, parts):
    for index, part in enumerate(parts):
        directory = os.path.join(directory, part)
        _try_makedirs(directory)
        with open(os.path.join(directory, "__init__.py"), "wb") as init_file:
            if index == len(parts) - 1:
                print('from .__version__ import __version__', file=init_file)
            elif options.create_namespace_packages:
                print("__import__('pkg_resources').declare_namespace(__name__)", file=init_file)

    with open(os.path.join(directory, '__version__.py'), 'wb') as version_file:
        print('__version__ = "0.0.1"', file=version_file)

def render_setup_file(directory, params):
    with open(os.path.join(directory, 'setup.py'), 'wb') as outfile:
        outfile.write(SETUP_FILE_TEMPLATE.render(params))

def render_tox_file(directory, params):
    with open(os.path.join(directory, 'tox.ini'), 'wb') as outfile:
        outfile.write(
"""[tox]
envlist = py26,py27,py32

[testenv]
deps=nose
commands=nosetests -w {toxinidir}/tests
changedir = {envdir}

[testenv:py26]
deps=unittest2
     nose
""")

def create_tests_directory(directory, params):
    tests_dir = os.path.join(directory, "tests")
    _try_makedirs(tests_dir)
    with open(os.path.join(tests_dir, 'test__readme_doctest.py'), 'wb') as test_file:
        test_file.write(DOCTEST_TEST_FILE_TEMPLATE.render(params))


def _try_makedirs(path):
    if os.path.isdir(path):
        return
    if os.path.exists(path):
        raise OSError("%s already exists, but not a directory" % path)
    os.makedirs(path)

def get_dest_directory(options, args):
    return args[0]

def get_params(options, directory):
    returned = {}
    for param, display, default in [
        ('projname', 'Project Name', os.path.basename(directory)),
        ('description', 'Description', ''),
        ('author', 'Author', posix.getlogin()),
        ('author_email', 'Email', ''),
        ('pyversion', 'Python Version', '.'.join(python_version().split('.')[:2])),
        ('license', 'License ({})'.format('/'.join(LICENSES)), 'proprietary')
        ]:
        if options.defaults:
            value = default
        else:
            value = raw_input("%s (default: %s): " % (display, default)).strip()
            if not value:
                value = default
        returned[param] = value
    projname_parts = returned["projname_parts"] = returned["projname"].split(".")
    ns_packages = returned["ns_packages"] = []
    if options.create_namespace_packages:
        for part in projname_parts[:-1]:
            if ns_packages:
                part = "{0}.{1}".format(ns_packages[-1], part)
            ns_packages.append(part)
    returned['license'] = license = LICENSES[returned['license']]
    returned['license_name'] = license['name']
    returned['year'] = time.localtime().tm_year
    return returned

def render_license_file(directory, params):
    with open(os.path.join(directory, "LICENSE"), "wb") as license_file:
        license_file.write(params['license']['template'].render(params))

def main_entry_point():
    options, args = parser.parse_args()
    directory = get_dest_directory(options, args)
    params = get_params(options, directory)
    create_directory(options, directory, params)
