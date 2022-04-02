# ds-miniproject-1

-------------------

### Instructions (Tested in Linux)

Ensure you have Python installed.

Then, run the following command:

```
run.sh <N>
            N   number of processes (N > 0)
```

It will automatically create a virtual environment, if it does not exist, and install the requirements.
Finally it will start the algorithm by creating the N processes.

### Notes

Each node is a process running independently. And each process has a main thread which is bound to a socket attached to an RPC service. This service will listen to RPC connections and spawn new threads to answer them (ThreadedServer). There is also a Worker thread, running in parallel, that is responsible for executing the algorithm state machine.

Each process is listening on a port in the range [18812, 18812 + N]. Check `src/__env__.py` for the default configuration values.

### Group

* Eduardo Ribas Brito
* Elizaveta Nikolaeva