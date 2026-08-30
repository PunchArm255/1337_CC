*This project has been created as part of the 42 curriculum by mnassiri.*

# Codexion

## Description
**Codexion** is a concurrency simulation written in C using threads and mutexes. It models multiple coders sitting in a circular table competing for a limited set of shared USB dongles to compile, debug, and refactor code without burning out. The simulation enforces strict constraints, custom priority policies (FIFO and EDF), mandatory resource cooldowns, and real-time burnout monitoring without relying on global variables.

## Instructions

### Compilation
Compile the project from the root directory using the provided `Makefile`:
```bash
make
```

This generates the `codexion` binary compiled with `-Wall -Wextra -Werror -pthread`.

### Execution

Run the executable with the following mandatory parameters:

```bash
./codexion <number_of_coders> <time_to_burnout> <time_to_compile> <time_to_debug> <time_to_refactor> <number_of_compiles_required> <dongle_cooldown> <scheduler>
```

**Parameters (in order):**

1. `number_of_coders`: Number of coders and shared dongles ($\ge 1$).
2. `time_to_burnout`: Time in milliseconds before a coder burns out if not compiling.
3. `time_to_compile`: Time in milliseconds spent compiling (requires 2 dongles).
4. `time_to_debug`: Time in milliseconds spent debugging.
5. `time_to_refactor`: Time in milliseconds spent refactoring.
6. `number_of_compiles_required`: Number of compilation cycles required per coder to stop the simulation.
7. `dongle_cooldown`: Cooldown duration in milliseconds after a dongle is released.
8. `scheduler`: Arbitration policy when multiple coders compete for a dongle (`fifo` or `edf`).

**Example:**

```bash
./codexion 5 2000 200 200 200 3 100 fifo
```

## Resources

### References

* **Dining Philosophers Problem:** https://en.wikipedia.org/wiki/Dining_philosophers_problem
* **Operating Systems Concepts:** Concurrency, Mutex Locks, Condition Variables, and Deadlock (Coffman conditions).

### AI Usage

AI was used as an interactive technical reviewer and documentation assistant to:

* Validate the mathematical correctness of `usleep`, dongle-ring, and overflow prevention.
* Help check for any potential Data Races or Deadlocks.
* Assist in structuring documentation and testing edge cases.

## Blocking cases handled

* **Deadlock Prevention (Coffman’s Conditions):** To eliminate the Circular Wait condition in circular resource allocation, an asymmetric acquisition hierarchy (`dongle_reorder`) is enforced: even-indexed coders acquire Right-then-Left dongles, while odd-indexed coders acquire Left-then-Right dongles.
* **Starvation Prevention:** A deterministic 2-slot priority queue (`t_queue`) arbitrates dongle contention. Under `fifo`, requests are served in strict arrival order (`arrival_time`). Under `edf`, the coder with the earliest burnout deadline (`deadline`) is granted priority, with arrival timestamp serving as a deterministic tie-breaker.
* **Cooldown Handling:** Each dongle tracks `time_to_acquire = release_time + cooldown`. Requesting threads block using `pthread_cond_timedwait` set to the cooldown expiration timestamp, ensuring dongles remain unavailable until the cooldown elapses.
* **Precise Burnout Detection:** A dedicated monitor thread polls coder deadlines within a dynamic 5ms frame budget (`MONITOR_FRAME_BUDGET 5` with `precise_sleep`), guaranteeing that any burnout is detected and logged within $\le 10\text{ ms}$ of the deadline.
* **Log Serialization:** All terminal logging is channeled through `sim_log()` guarded by `pthread_mutex_t log_mtx`, preventing interleaved character output.

## Thread synchronization mechanisms

* **`pthread_mutex_t`:**
* `state_mtx`: Protects read/write access to the global `sim->should_stop` flag.
* `log_mtx`: Serializes `printf` execution to keep stdout atomic.
* `coder->mtx`: Protects thread-local state (`times_compiled` and `last_compile_start`) from concurrent read/write data races between worker and monitor threads.
* `dongle->acquire_mtx`: Guarantees mutual exclusion over the internal state of each dongle (`is_acquired`, `time_to_acquire`, and `queue`).


* **`pthread_cond_t` & Custom Event Implementation:**
* Each dongle encapsulates a `pthread_cond_t cond`.
* Threads block on `pthread_cond_timedwait` inside a `while (!sim_should_stop && must_wait)` predicate loop, eliminating busy-waiting and protecting against spurious wakeups.
* `release_dongle()` and `wake_all_dongles()` execute `pthread_cond_broadcast(&dongle->cond)` to wake waiting threads when resources are freed or simulation terminates.


* **Thread-Safe Communication & Race Condition Prevention:**
* Coders update `last_compile_start` at the start of compiling and increment `times_compiled` using mutex-protected setter functions.
* The monitor inspects coder states via mutex-protected getter functions, preventing data races.
* Termination is signaled by setting `should_stop = 1` under `state_mtx` and broadcasting to all condition variables via `wake_all_dongles()`, ensuring all blocked threads wake up, exit cleanly, and join at `pthread_join`.
