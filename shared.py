from multiprocessing import Manager
from multiprocessing import Lock


def create_shared():
    manager = Manager()
    return manager.list()
   
lock = Lock()