from mpi4py import MPI # pyright: ignore[reportMissingImports]
from multiprocessing import Manager, Process, Lock
import time
from master import generate_orders
from worker import process_order


try:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    using_mpi = size > 1
except:
    rank = 0
    size = 1
    using_mpi = False


if not using_mpi:
    # Fallback to multiprocessing when MPI is not available or has only 1 process
    def worker_process(order_queue, result_queue, lock, shared_results, rank):
        """Worker process that retrieves orders from queue and processes them."""
        while True:
            order = order_queue.get()
            if order is None:
                break
            
            result = process_order(order, rank)
            
            # Append to shared results with lock for synchronization
            with lock:
                shared_results.append(result)
            
            result_queue.put(result)

    if __name__ == '__main__':
        # Create shared data structures with synchronization
        manager = Manager()
        shared_results = manager.list()
        lock = Lock()
        
        order_queue = manager.Queue()
        result_queue = manager.Queue()
        
        num_workers = 3  # Number of worker processes
        
        print("MASTER STARTED")
        
        # Generate orders
        orders = generate_orders()
        
        # Start worker processes
        workers = []
        for i in range(num_workers):
            p = Process(target=worker_process, args=(order_queue, result_queue, lock, shared_results, i+1))
            p.start()
            workers.append(p)
        
        # Distribute orders
        for order in orders:
            order_queue.put(order)
        
        # Send termination signals
        for _ in range(num_workers):
            order_queue.put(None)
        
        # Collect results from individual workers
        results = []
        for _ in range(len(orders)):
            result = result_queue.get()
            results.append(result)
        
        # Wait for all workers to complete
        for p in workers:
            p.join()
        
        # Display shared results (synchronized access)
        with lock:
            print("\nFINAL RESULTS (from shared memory with Lock synchronization):")
            for r in shared_results:
                print(r)
else:
    # MPI-based implementation when multiple processes are available
    if rank == 0:
        print("MASTER STARTED (MPI Mode)")
        
        orders = generate_orders()
        worker_count = size - 1
        
        if worker_count <= 0:
            print("No workers available")
        else:
            # Distribute orders to workers
            for i, order in enumerate(orders):
                worker = (i % worker_count) + 1
                comm.send(order, dest=worker)
            
            # Send termination signals
            for i in range(1, size):
                comm.send(None, dest=i)
            
            # Collect results
            results = []
            for _ in range(len(orders)):
                result = comm.recv(source=MPI.ANY_SOURCE)
                results.append(result)
            
            print("\nFINAL RESULTS:")
            for r in results:
                print(r)
    else:
        # Worker process
        while True:
            order = comm.recv(source=0)
            if order is None:
                break
            
            result = process_order(order, rank)
            print(f"Worker {rank}: {result}")
            comm.send(result, dest=0)
