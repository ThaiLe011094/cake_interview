from airflow.models.dag import DAG
from datetime import datetime, timedelta
from dag_configs.sync_sftp_dag_config import sync_sftp_dag_config
from utils.logger import init_logger


dag_infos = [
    {
        'dag_id': 'sftp_sync',
        'description': 'Sync files from source SFTP to target SFTP',
        'schedule': '@daily',
        'start_date': datetime(2025, 5, 17, 0, 0, 0),  # Reminder: The dag should start in 2025-05-18  # noqa
        'catchup': False,
        'tags': ['sftp'],
    },
]


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

for dag_info in dag_infos:
    dag_id = dag_info['dag_id']
    logger = init_logger(dag_id)

    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        description=dag_info['description'],
        schedule=dag_info['schedule'],
        start_date=dag_info['start_date'],
        catchup=dag_info['catchup'],
        tags=dag_info['tags'],
        max_active_runs=dag_info.get('max_active_runs', 1),
    )
    with dag:
        sync_sftp_dag_config(
            dag=dag,
            logger=logger,
        )
    globals()[dag_id] = dag
