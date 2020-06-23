import os


def identifier():
    return "wardoff-{pid}".format(pid=os.getpid())


def package_sources(package_info):
    pass
