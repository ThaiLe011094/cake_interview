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


# References
 - [Configuration Reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html)
 - [Airflow Official Docker Compose](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml)

# How to run
## Setup docker if not installed yet


## Invoke some commands
Run these commands <r>without</r> the `$`, `$` means to be executed by <g>normal user</g>.
```bash
$ chmod +x init.sh
$ ./init.sh
$ sudo docker compose airflow-init  # we only need this once
$ sudo docker compose build --no-cache  # this can be run in any time, but it's better to be run after changing the requirement
$ sudo docker compose up  # this can also be run in any time
```
