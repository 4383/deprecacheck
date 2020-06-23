from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import uuid
import venv


from wardoff import utils


TMPDIR = Path(tempfile.gettempdir())
VENVDIR = TMPDIR.joinpath(utils.identifier())


def destroy():
    if VENVDIR.is_dir():
        shutil.rmtree(str(VENVDIR))


def create():
    destroy()
    venv.create(str(VENVDIR))


def pip(*cmd):
    base = [os.path.join(VENVDIR, 'bin', 'python'), '-m', 'pip']
    argv = base + list(cmd)
    return subprocess.check_output(argv).decode('utf8')


def pip_install(package):
    pip('install', package)


def pip_show(package):
    pip_install(package)
    return pip('show', package).split("\n")
