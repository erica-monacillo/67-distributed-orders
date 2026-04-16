
def generate_orders():
    return [
        {"id": 1, "item": "Burger"},
        {"id": 2, "item": "Fries"},
        {"id": 3, "item": "Pizza"},
        {"id": 4, "item": "Milk Tea"},
        {"id": 5, "item": "Coffee"},
        {"id": 6, "item": "Pasta"},
        {"id": 7, "item": "Salad"},
        {"id": 8, "item": "Dessert"}
    ]


def distribute_orders(comm, size, orders):
    """Distribute orders to worker processes using MPI."""
    worker_count = size - 1

    if worker_count <= 0:
        print("No workers available")
        return

    # Distribute orders to workers
    for i, order in enumerate(orders):
        worker = (i % worker_count) + 1
        comm.send(order, dest=worker)

    # Send termination signal (None) to all workers
    for i in range(1, size):
        comm.send(None, dest=i)