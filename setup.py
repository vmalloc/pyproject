from distutils.core import setup

from pyproject import __version__ as VERSION

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
      version=VERSION,
      packages=["pyproject"],
      scripts=['scripts/start_python_project'],
      )
