"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['program.py']
DATA_FILES = ['mpb_logo.png','block.py']
PKGS = ['python_hosts','elevate']
OPTIONS = {
	'packages' : PKGS
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)