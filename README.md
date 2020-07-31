
# pyquorum

PyQuorum is a simple leader election algorithm written in Python.

## Description

The servers where PyQuorum is run will form a cluster and run a specified script in a separate thread as long as the majority of servers are online. Once quorum is lost, the script will be terminated and a new master elected.

## Election

Each server sends keep-alive messages to other servers and monitors their availability. Once the majority of servers are available (more than half) the server with the lowest ip address proposes to be the master. Each node votes whether the proposed master should be master and if consensus is achieved (a node has the majority of votes being master) the node will transition to master mode and run the specified script. If not enough votes or nodes are available the master will automatically transition to slave mode and stop the execution of the script (send a SIGTERM signal which can be handled by the script).

## Requirements

* Python >= 3.7
* 3 or more servers

**Note:** It is possible to run this with only two servers but without high-availability. Only an odd number of servers are recommended.

## Installation

```bash
python3 -m venv venv
. ./venv/bin/activate
./build.sh
```

Once built you can either use the above installation process for other nodes or deploy the application using wheel packages.

```bash
pip install -U ./dist/pyquorum-{...}.wheel
```

## Usage

The commands below assume that you have installed the package locally in your virtual environment. Otherwise the commands may vary and you need to make sure that the binary is in your environments path.

```bash
pyquorum [-h] [--version] [-b BIND] [-p PORT] [-s SCRIPT] [-v] [-vv] SERVER [SERVER ...]
```

Optional Arguments:

| Name               | Required | Default Value      | Description                                              |
|--------------------|----------|--------------------|----------------------------------------------------------|
| -h/--help          | no       |                    | Shows the manual                                         |
| --version          | no       |                    | Shows the current version of PyQuorum installed          |
| -b/--bind          | no       | Primary IP address | Bind to a specific ip.                                   |
| -p/--port          | no       | 51621              | Port that should be used for communication between nodes |
| -s/--verbose       | no       |                    | set loglevel to INFO                                     |
| -vv/--very-verbose | no       |                    | set loglevel to DEBUG                                    |

If not script is specified then this program is pretty pointless as it does nothing after master election.

After the optional arguments you need to specify *at least* one other server which should be part of the cluster. However can use as many servers as you like in the cluster.

## Example

The below commands can be executed on the respective node to form a simple three-node cluster. The master will run the script *test_runner.sh*. When quorum is lost the script will be killed and started on another node.
Node 1: ```pyquorum -b 172.16.0.1 -s ./test_runner.sh 172.16.0.2 172.16.0.3```
Node 2: ```pyquorum -b 172.16.0.2 -s ./test_runner.sh 172.16.0.1 172.16.0.3```
Node 3: ```pyquorum -b 172.16.0.3 -s ./test_runner.sh 172.16.0.1 172.16.0.2```

## Tests

Unit-Test can be run with ```python setup.py test```

## License

The project is subject to the MIT license unless otherwise noted. A copy can be found in the root directory of the project [LICENSE](LICENSE.txt).
