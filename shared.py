from multiprocessing import Manager, Lock


def create_shared():
    """Create a shared list for storing order results."""
    manager = Manager()
    return manager.list()


def get_lock():
    """Create a lock for synchronizing access to shared data."""
    return Lock()