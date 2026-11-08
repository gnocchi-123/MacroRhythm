"""Verify the installed package, rather than importing from an ad hoc source path."""

from importlib.metadata import version

import macrorhythm


def test_installed_package_version():
    assert version("macrorhythm") == macrorhythm.__version__ == "0.1.0"
