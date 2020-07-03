import os
import shutil
import subprocess
import tempfile
import venv as virtualenv
from pathlib import Path

from wardoff import utils

TMPDIR = Path(tempfile.gettempdir())
VENVDIR = TMPDIR.joinpath(utils.identifier())


class VenvException(Exception):
    pass


def site_packages():
    python_version = [el for el in VENVDIR.rglob("lib/python*")][0]
    site_packages_path = VENVDIR.joinpath(
        "lib", python_version, "site-packages"
    )
    return site_packages_path


def is_installed(package):
    return site_packages().joinpath(package).is_dir()


def destroy():
    if VENVDIR.is_dir():
        shutil.rmtree(str(VENVDIR))


def create():
    destroy()
    # Normally we don't need to do this as create accept a path
    # but on travis created virtualenv is weird so we prefer to
    # create the path manually on then move in to create the venv.
    cwd = os.getcwd()
    os.mkdir(str(VENVDIR))
    os.chdir(str(VENVDIR))
    virtualenv.create(
        ".",
        clear=False,
        symlinks=True,
        system_site_packages=False,
        prompt=None,
        with_pip=True,
    )
    os.chdir(cwd)


def pip(cmd_params):
    if not isinstance(cmd_params, list):
        raise ValueError("list is excepted")
    binary = VENVDIR.joinpath("bin", "python")
    base = [str(binary), "-m", "pip"]
    argv = base + cmd_params
    print(" ".join(argv))
    return subprocess.check_output(argv).decode("utf8")


def pip_install(*package):
    cmd_params = list(package)
    cmd_params.insert(0, "install")
    cmd_params.insert(1, "-I")
    return pip(cmd_params)


def pip_show(package):
    return pip(["show", package]).split("\n")
