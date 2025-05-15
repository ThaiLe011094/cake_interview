import os
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator  # check airflow.__init__ for deprecated import  # noqa
from datetime import datetime


DAG_OWNER = {
    os.environ.get('AIRFLOW_DEFAULT_OWNER', 'Thai'):
        os.environ.get('AIRFLOW_DEFAULT_OWNER_URL', 'https://github.com/ThaiLe011094/'),
}

with DAG(
    dag_id='airflow_test_dag',
    description='A simple test DAG that echoes a string',
    schedule='1 * * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['test'],
    owner_links=DAG_OWNER,
) as dag:

    echo_task = BashOperator(
        task_id='echo_hello',
        bash_command='echo "This is a test dag!"',
    )

