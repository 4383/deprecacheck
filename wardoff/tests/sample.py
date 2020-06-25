import requests
import abc
from foo import bar


def baz():
    print("baz")


def raiseValueError():
    print("raise")
    raise ValueError("boom")


def fiz():
    print("fiz")
    print("fiz")
    print("fiz")
    print("fiz")
    raise DeprecationWarning()


def foz():
    raise DeprecationWarning("foz is deprecated please stop to use it")
    print("foz")


def fuzz():
    raise DeprecationWarning(
        "foz is deprecated please stop to use it"
        "blablabla"
        "blablafuzz"
    )
    print("foz")


class Bar:
    def run(self):
        print("run")

    def bar(self):
        print("bar")
        raise DeprecationWarning("boom")


class Foo:
    pass
