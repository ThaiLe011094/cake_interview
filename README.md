<style>
r { color: Crimson }
b { color: RoyalBlue }
g { color: Lime }
</style>
  
# Requirement
## Problem Statement
 - The task involves two SFTP destinations, referred to as \<<b>source</b>> and \<<b>target</b>>.
 - Your objective is to develop an Apache Airflow DAG that facilitates the transfer of files from the SFTP server at \<<b>source</b>> to the SFTP server at \<<b>target</b>> and ensures the preservation of the original directory structure.
 - The synchronization process should be unidirectional; hence, any modification made on \<<b>target</b>> must not impact the \<<b>source</b>>.
 - Deleted files on SFTP server at \<<b>source</b>> must remain intact on \<<b>target</b>> server.

## Examples:
 - On March 1st, 2024, when a file named `sftp://<source>/a/b/c/file_1.txt` is detected on the source server, it should be replicated to `sftp://<target>/a/b/c/file_1.txt` on the destination server.
 - On March 2nd, 2024, a file named `sftp://<source>/a/b/c/file_2.txt` appears on the source server and subsequently should be transferred to `sftp://<target>/a/b/c/file_2.txt` on the destination server.
 - On March 3rd, 2024, a file named `sftp://<source>/a/b/c/file_3.txt` appears on the source server and should then be transferred to `sftp://<target>/a/b/c/file_3.txt` on the destination server.

## Expected Outcome
 - Candidates are expected to provide a GitHub public repository as following:
 - Use separated commits that reflect your incremental development and refactoring. Pure atomic commits are not expected, and don’t squash them.
 - A docker-compose.yml file for deploying latest Airflow version, with each service (Scheduler, Worker, Web Server) running in a separate container. Utilizing SQLite as the backend is permissible. The use of Celery executor is advised.
 - A README.md file that includes:
 - Detailed instructions for setting up and running the project.
 - Any additional initial setup requirements.
 - An explanation of assumptions made, decisions taken, and any trade-offs considered.
 - One or more DAG file(s).
 - Any additional plugins required for the project.

## What We <r>Don’t</r> Expect
 - A comprehensive, production-ready ETL/ELT solution that is agnostic to data sources and destinations

## What We Assess
 - The functionality of a runnable Airflow DAG that accurately achieves the specified result.
 - The candidate‘s adherence to a consistent and clean coding style.
 - The level of abstraction in your API(s). Given that business requirements are subject to change, evaluate how adaptable your solution is if the data source transitions from SFTP to Object Storage.
 - The extensibility of your API(s). Assess whether it is feasible to incorporate additional transformations before loading files into the target system without significant effort.
 - Your strategy for handling anomalies. For instance, if file sizes increase dramatically from kilobytes to gigabytes, how does your solution accommodate this change in scale?


# How to run
## Setup docker if not installed yet
Follow this [official document](https://docs.docker.com/engine/install/) for installing Docker Engine and its dependencies, plugins.  
<r>**Note:**</r> Consider adjusting resource when using docker. Please follow this [document](https://docs.docker.com/engine/containers/resource_constraints/).  
<g>**Example:**</g> [How to Limit Docker Memory and CPU Usage](https://phoenixnap.com/kb/docker-memory-and-cpu-limit).

## Invoke some commands
Run these commands <r>**without**</r> the `$`, `$` means to be executed by <g>**normal user**</g>.
```bash
$ chmod +x init.sh
$ ./init.sh
$ sudo docker compose airflow-init  # we only need this once
$ sudo docker compose build --no-cache  # this can be run in any time, but it's better to be run after changing the requirement
$ sudo docker compose up  # this can also be run in any time
```
Since this repo is for completing the the interview task, so below are some commands to populate the files
```bash
# Let's assume that we're in the code directory
$ mkdir -p ./tests/source_data/a/b/c
# Since we already mounted the volume from the sftp folder to folder in tests directory
# All things changed in the tests directory will be reflected on the sftp folder
# Let's make some text files and a bin file in the sfpt_source directory only
$ echo "Test content 1" > tests/source_data/a/b/c/file_1.txt
$ echo "Test content 2" > tests/source_data/a/b/c/file_2.txt
$ head -c 10M /dev/zero > tests/source_data/a/b/c/large_file_10M.bin

```

## Add connection to Airflow
Although we can add connection to Airflow UI Connection via command line, writing data into Airflow Admin UI is more recommended.  
Get into `http://localhost:8080/connections` or `http://<airflow-hosted-address>/connections`.  
The connection info is:
Source SFTP:
```json
{
    "conn_id": "source_sftp_conn",
    "conn_type": "sftp",
    "host": "source-sftp",
    "username": "testuser",
    "password": "testpass",
    "port": 22
}
```
Target SFTP:
```json
{
    "conn_id": "target_sftp_conn",
    "conn_type": "sftp",
    "host": "target-sftp",
    "username": "testuser",
    "password": "testpass",
    "port": 22
}
```
## Run Airflow DAG
Get into `http://localhost:8080/dags/sftp_sync/` or `http://<airflow-hosted-address>/dags/sftp_sync/` then click on Triger to run the DAG.

## Check for the files on the sftp server
As in the configuration in docker-compose.yaml, we configured the sftp-source with port 2222, and sftp-source with port 2223.  
To check files in them, we can follow this command line:  
```bash
# Sample: sftp -P <port> <username>@<host>
# To test files' existence in target-sftp, we run this
$ sftp -P 2223 testuser@localhost
# To list files/folders
$ ls -la
# Then we can cd in to the directory like in the bash shell
$ cd upload
```


# Limitation
Since this code is for serving some local quick and low-size files, there will be some limitation, but first we can see something like this:
 - This code will work only on local or self-hosted platform, not yet runable on Cloud Storage.
 - The files are relative small and not too much, the code was only written to handle this case. Also not using streaming as always is for trading off the easy debug.


# Further Improvement
Although there are limitations, at least listed in the previous section, we can also improve it in later time:
 - Add feature for streaming big files. We might need to raise a flag to know if it's a big file to use the streaming.
 - Change writing locally to io.BytesIO() to write into buffer instead.
 - We can use chunked streaming with buffer to control memory usage, transfer speed, and error handling.
 - Add feature to interact with Cloud Storage, as in the code, we need to fix a bit to seperate the task for downloading and uploading. Then transfering to Cloud Storage will be implemented in ease.
 - Add precommit for checking lint, etc.


# References
 - [Configuration Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
 - [Airflow Official Docker Compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml)
 - [Docker Installation](https://docs.docker.com/engine/install/)
 - [Docker Resource Constraints](https://docs.docker.com/engine/containers/resource_constraints/)
 - [How to Limit Docker Memory and CPU Usage](https://phoenixnap.com/kb/docker-memory-and-cpu-limit)
 - [Sftp Container](https://hub.docker.com/r/atmoz/sftp)
 - [Python Stat Module](https://docs.python.org/3/library/stat.html)
 - [How to Works Python Stat Module](https://stackoverflow.com/questions/56098463/how-works-pythons-stat-module)
