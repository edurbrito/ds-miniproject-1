# ds-miniproject-1

-------------------

### Instructions (Tested in Linux)

Ensure you have Python installed.

Then, run the following command:

```
run.sh <N>
            N   number of processes (N > 0)
```

It will automatically create a virtual environment (`env` folder), if it does not exist, and install the requirements.
Finally it will start the algorithm by creating the N processes.

### Notes

Each node is a process running independently. And each process has a main thread which is bound to a socket attached to an RPC service. This service will listen to RPC connections and spawn new threads to answer them (ThreadedServer). There is also a Worker thread, running in parallel, that is responsible for executing the algorithm state machine.

Each process is listening on a port in the range [18812, 18812 + N]. Check `src/__env__.py` for the default configuration values.

### Deliverables

###### src folder

Contains all the source code, classes and configuration variables needed to run the program. The `__main__.py` file is the entrypoint for the program, which then just needs to be called with `python ./src N`.

###### docs folder

Contains the specification PDF, and the video of a running example - this video was recorded with other values for the timeouts ([10,20] for `time-p` and [10,15] for `time-cs`), in order to better visualize the algorithm under 1 minute.

###### bonus folder

Contains a demonstration video and a docker-compose file with all the configuration needed to spawn 3 replicas of the Apache Zookeeper image which are connected to each other and will perform a leader election to choose the leader amongst them.

To run the file:
1. Go to the `bonus` folder: `cd bonus`
2. Run the docker-compose file: `docker-compose up`

Each replica has two ports published: One for communication between the replicas, another for hosting a web interface to get information of the cluster.

The environment variables used are the replica ID and the list of connected replicas.

To test the cluster running, one can query some information like:

* Who is the leader:

```sh
curl http://localhost:9666/commands/leader
```

* What is the last snapshot:

```sh
curl http://localhost:9665/commands/last_snapshot
```

* The last voting view:

```sh
curl http://localhost:9667/commands/voting_view
```

* Monitoring the cluster:

```sh
curl http://localhost:9666/commands/monitor
```

* Get the environment information:

```sh
curl http://localhost:9667/commands/environment
```

* List of all the commands:

```sh
curl http://localhost:9667/commands
```

References:
* [Docker Hub Zookeeper official image](https://hub.docker.com/_/zookeeper)
* [Setting up an Apache Zookeeper cluster in Docker](https://farid-baharuddin.medium.com/setting-up-an-apache-zookeeper-cluster-in-docker-8960d5c23f5c)

### Group

* Eduardo Ribas Brito
* Elizaveta Nikolaeva