#!/bin/bash

mkdir -p ./dags ./logs ./plugins ./config ./logs
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=$(id -u)\nAIRFLOW__CORE__LOAD_EXAMPLES=False" >>.env
