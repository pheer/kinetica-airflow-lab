from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime, timedelta

###############################################
# Parameters
###############################################
spark_master = "spark://spark-master:7077"
spark_app_name = "Kinetica Ingest"
file_path = "/app/conf.yml"

###############################################
# DAG Definition
###############################################
now = datetime.now()

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
        "kinetica-ingest",
        default_args=default_args, 
        schedule_interval=timedelta(1)
    )

start = DummyOperator(task_id="start", dag=dag)

spark_job = SparkSubmitOperator(
    task_id="spark_job_id",
    application="/app/kinetica_ingest.py",
    jars="/libs/kinetica-spark-7.0.6.0-jar-with-dependencies.jar",
    name=spark_app_name,
    conn_id="spark_default",
    verbose=1,
    conf={"spark.master":spark_master},
    application_args=[file_path],
    executor_cores=4,
    dag=dag)

end = DummyOperator(task_id="end", dag=dag)

start >> spark_job >> end
