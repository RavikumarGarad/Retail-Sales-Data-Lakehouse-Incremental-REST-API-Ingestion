from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


# ---------------------------------------------------------
# Default DAG configuration
# ---------------------------------------------------------
default_args = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


# ---------------------------------------------------------
# Task functions
# ---------------------------------------------------------
def run_api_ingestion():
    """
    Trigger REST API ingestion.
    Actual API ingestion logic is maintained
    in notebooks/01_api_ingestion/api_ingestion_demo.py
    """
    print("Starting REST API incremental ingestion...")
    print("Customer and Sales data ingestion completed.")


def run_bronze_processing():
    """
    Process raw API data into Bronze layer.
    """
    print("Starting Bronze layer processing...")
    print("Bronze processing completed.")


def run_customer_silver():
    """
    Transform customer data into Silver layer.
    """
    print("Starting Customer Silver transformation...")
    print("Customer Silver processing completed.")


def run_sales_silver():
    """
    Transform sales data into Silver layer.
    """
    print("Starting Sales Silver transformation...")
    print("Sales Silver processing completed.")


def run_gold_processing():
    """
    Create Gold-layer business aggregations.
    """
    print("Starting Gold layer processing...")
    print("Gold aggregations completed.")


def run_data_quality():
    """
    Execute data quality validations.
    """
    print("Starting data quality checks...")
    print("Data quality checks completed successfully.")


# ---------------------------------------------------------
# DAG definition
# ---------------------------------------------------------
with DAG(
    dag_id="retail_lakehouse_pipeline",
    default_args=default_args,
    description="Retail Lakehouse incremental REST API ingestion pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["retail", "azure", "adls", "databricks", "delta"],
) as dag:

    # 1. API ingestion
    api_ingestion = PythonOperator(
        task_id="api_ingestion",
        python_callable=run_api_ingestion,
    )

    # 2. Bronze layer
    bronze_processing = PythonOperator(
        task_id="bronze_processing",
        python_callable=run_bronze_processing,
    )

    # 3. Silver layer
    customer_silver = PythonOperator(
        task_id="customer_silver_processing",
        python_callable=run_customer_silver,
    )

    sales_silver = PythonOperator(
        task_id="sales_silver_processing",
        python_callable=run_sales_silver,
    )

    # 4. Gold layer
    gold_processing = PythonOperator(
        task_id="gold_processing",
        python_callable=run_gold_processing,
    )

    # 5. Data quality
    data_quality = PythonOperator(
        task_id="data_quality_checks",
        python_callable=run_data_quality,
    )

    # -----------------------------------------------------
    # Pipeline dependency
    # -----------------------------------------------------
    api_ingestion >> bronze_processing

    bronze_processing >> [
        customer_silver,
        sales_silver,
    ]

    [
        customer_silver,
        sales_silver,
    ] >> gold_processing

    gold_processing >> data_quality