import inspect
from logging import info


def startLog():
    name = inspect.getmodule(inspect.stack()[1][0]).__name__.split('.')[-1]
    print(name)
    info("START: " + name + " start running")


def endLog(err=True):
    name = inspect.getmodule(inspect.stack()[1][0]).__name__.split('.')[-1]
    print(name)
    if err:
        info("Done: " + name + " running is over")
    else:
        info("Done: " + name + " running is over with errors")
