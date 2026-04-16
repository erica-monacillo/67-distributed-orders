from multiprocessing import Process, Queue
from master import generate_orders
from worker import process_order


def worker_process(order_queue, result_queue, rank):
    while True:
        order = order_queue.get()
        if order is None:
            break
        result = process_order(order, rank)
        result_queue.put(result)

if __name__ == '__main__':
    order_queue = Queue()
    result_queue = Queue()

    num_workers = 2  # Number of worker processes

    workers = []
    for i in range(num_workers):
        p = Process(target=worker_process, args=(order_queue, result_queue, i+1))
        p.start()
        workers.append(p)

    print("MASTER STARTED")

    orders = generate_orders()
    for order in orders:
        order_queue.put(order)

    for _ in range(num_workers):
        order_queue.put(None)

    results = []
    for _ in range(5):
        result = result_queue.get()
        results.append(result)


    print("\nFINAL RESULTS:")
    for r in results:
        print(r)


    for p in workers:
        p.join()
