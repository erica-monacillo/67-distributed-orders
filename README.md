# cs323-distributed-orders
## GROUP 67

## MONACILLO
## SUELO
## ARRIBA
## PANA

# MPI & Multiprocessing Reflection

## 1. How did you distribute orders among worker processes?

The master process (rank 0) distributes orders using MPI by sending each order to worker processes in a round-robin manner. This ensures that all workers receive tasks evenly and efficiently.

---

## 2. What happens if there are more orders than workers?

If there are more orders than workers, some workers will receive multiple orders. The master continues assigning tasks until all orders are distributed, so workers process tasks one by one.

---

## 3. How did processing delays affect the order completion?

Processing delays (using `time.sleep()`) caused tasks to finish at different times. Even if orders were sent in sequence, the output showed that some workers finished earlier than others, demonstrating real-world asynchronous behavior.

---

## 4. How did you implement shared memory, and where was it initialized?

We used `Manager().list()` from the multiprocessing module to create a shared list. It was initialized in the main program so all processes could store and access completed orders.

---

## 5. What issues occurred when multiple workers wrote to shared memory simultaneously?

Without synchronization, multiple workers could write at the same time, which may cause inconsistent or incomplete data. This can lead to missing or corrupted outputs.

---

## 6. How did you ensure consistent results when using multiple processes?

We used a `Lock()` to control access to the shared memory. By allowing only one worker to write at a time, we ensured that the final output is complete and consistent (walay gubot sa data).


