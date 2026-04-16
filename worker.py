import time
from multiprocessing import Manager, Lock

def process_order(order, rank):
    """Process a single order with a delay."""
    print(f"Worker {rank} processing {order}")
    time.sleep(2)
    return f"Order {order['id']} done by Worker {rank}"


def process_order_with_sync(order, rank, comm):
    """Process order and return result through MPI."""
    print(f"Worker {rank} processing {order}")
    time.sleep(2)
    result = f"Order {order['id']} done by Worker {rank}"
    # Send result back to master
    comm.send(result, dest=0)
    return result
