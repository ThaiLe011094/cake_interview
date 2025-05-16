def sync_sftp_dag_config(dag, **kwargs):
    """
    Sync files from source SFTP to target SFTP.
    """  # noqa
    from airflow.providers.standard.operators.python import PythonOperator
    from operators.sync_sftp_operator import (
        sync_sftp_files,
    )

    sync_sftp_operator = PythonOperator(
        task_id='sync_sftp_files_operator',
        op_kwargs=kwargs,
        dag=dag,
        python_callable=sync_sftp_files,
    )

    return sync_sftp_operator
