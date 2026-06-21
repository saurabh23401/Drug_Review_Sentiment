from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from airflow.datasets import Dataset
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from main import run_processing

drug_review_dataset = Dataset("data\raw\drugLibTest_raw.tsv")

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=10),
    "depends_on_past": False,
}

with DAG(
    dag_id="drug_reviews_dag",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="0 * * * *",   # Hourly. Use "0 0 * * *" for daily.
    catchup=False,
    sla_miss_callback=None,           # Add SLA callback if needed
    description="ETL pipeline for drug review sentiment with NER and dashboard update"
) as dag:

    start_task = DummyOperator(task_id="start_task")
    
    process_task = PythonOperator(
        task_id="processing_dag",
        python_callable=run_processing
    )

    dag_end  = DummyOperator(task_id="Dag_end")

    start_task >> process_task >> dag_end

    # clean_and_preprocess = PythonOperator(
    #     task_id="clean_and_preprocess",
    #     python_callable=preprocess_main,
    #     sla=timedelta(hours=1)
    # )

    # run_ner_normalize_drug_names = PythonOperator(
    #     task_id="run_ner_normalize_drug_names",
    #     python_callable=ner_normalize_main,
    #     sla=timedelta(hours=1)
    # )

    # vectorize_features = PythonOperator(
    #     task_id="vectorize_features",
    #     python_callable=vectorize_main,
    #     sla=timedelta(hours=1)
    # )

    # train_or_update_model = PythonOperator(
    #     task_id="train_or_update_model",
    #     python_callable=train_model_main,
    #     trigger_rule="all_done",            # Customize as needed (manual/weekly triggers can be handled via DAG parameters or branch)
    #     schedule_interval="0 0 * * 0",      # Schedule weekly with cron if separated
    #     sla=timedelta(hours=3)
    # )

    # batch_infer_new_reviews = PythonOperator(
    #     task_id="batch_infer_new_reviews",
    #     python_callable=batch_infer_main,
    #     sla=timedelta(hours=1)
    # )

    # update_dashboard_data = PythonOperator(
    #     task_id="update_dashboard_data",
    #     python_callable=update_dashboard_main,
    #     sla=timedelta(hours=1)
    # )

    # Task dependencies
    # start >> clean_and_preprocess
    # clean_and_preprocess >> run_ner_normalize_drug_names
    # run_ner_normalize_drug_names >> vectorize_features
    # vectorize_features >> [train_or_update_model, batch_infer_new_reviews]
    # batch_infer_new_reviews >> update_dashboard_data
    # update_dashboard_data >> end
    # train_or_update_model >> end   # This finishes the path for the model retrain

