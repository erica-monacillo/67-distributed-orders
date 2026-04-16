import time


def process_order(order, rank):
    print(f"Worker {rank} processing {order}")
    time.sleep(2)
    return f"Order {order['id']} done by Worker {rank}"
