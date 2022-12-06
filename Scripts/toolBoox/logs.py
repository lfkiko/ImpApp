import inspect
from logging import info


def startLog(name=None):
    if name is None:
        name = inspect.getmodule(inspect.stack()[1][0]).__name__.split('.')[-1]
    info("START: " + name + " start running")


def endLog(err: bool = True, name=None):
    if name is None:
        name = inspect.getmodule(inspect.stack()[1][0]).__name__.split('.')[-1]
    if err:
        info("Done: " + name + " running is over")
    else:
        info("Done: " + name + " running is over with errors")


def fileStatus(filePath: str, staus):
    fileName = filePath.split('\\')[-1]
    if staus == 'update':
        info("Upadted: " + fileName + " was updated")
