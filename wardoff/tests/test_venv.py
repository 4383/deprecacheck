from pathlib import Path
import unittest

from wardoff import utils
from wardoff import venv


class TestVenv(unittest.TestCase):
    def test_create(self):
        venv.create()
        self.assertTrue(venv.VENVDIR.is_dir())

    def test_pip_show(self):
        venv.create()
        info = venv.pip_show('niet')
        home_page = None
        for el in info:
            if not el.startswith("Home-page:"):
                continue
            home_page = el.replace("Home-page: ", "")
        self.assertEqual(home_page, "https://github.com/openuado/niet/")

    def test_destroy(self):
        venv.create()
        self.assertTrue(venv.VENVDIR.is_dir())
        venv.destroy()
        self.assertFalse(venv.VENVDIR.is_dir())
