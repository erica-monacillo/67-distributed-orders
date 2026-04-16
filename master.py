
def generate_orders():
    return [
        {"id": 1, "item": "Burger"},
        {"id": 2, "item": "Fries"},
        {"id": 3, "item": "Pizza"},
        {"id": 4, "item": "Milk Tea"},
        {"id": 5, "item": "Coffee"}
    ]


def distribute_orders(comm, size):
    orders = generate_orders()


    worker_count = size - 1


    if worker_count <= 0:
        print("No workers available")
        return


    for i, order in enumerate(orders):
        worker = (i % worker_count) + 1
        comm.send(order, dest=worker)


    for i in range(1, size):
        comm.send(None, dest=i)