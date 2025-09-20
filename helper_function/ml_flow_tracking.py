
import mlflow
import mlflow.pyfunc
from mlflow.data import from_pandas
from pathlib import Path
from main import os, app_logger, pd
from helper_function.pre_process import generate_text_transformation, pipeline
from mlflow import MlflowClient


class SentimentPipelineWrapper(mlflow.pyfunc.PythonModel):
    def __init__(self, mdl_name="distilbert-base-uncased-finetuned-sst-2-english"):
        self.mdl_name = mdl_name

    def load_context(self, context):
        self.sentiment_classifier = pipeline("sentiment-analysis", model=self.mdl_name)

    def predict(self, context, model_input):
        # Accepts a DataFrame with a column 'text'
        texts = model_input["text"].tolist()
        predictions = self.sentiment_classifier(texts)
        return [pred["label"] for pred in predictions]

def run_mlflow_tracking(
    df: pd.DataFrame,
    cols_to_concat: list,
    polarities_limit: list = [8, 3],
    sys_col_rating_nm: str = "rating",
    mdl_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
): 
     
    try:
        project_root = Path(__file__).resolve().parent.parent
    except NameError:
        project_root = Path(os.getcwd()).parent.parent
    except Exception as e:
        app_logger.error("unable to get project root path")
        raise(e)
    app_logger.info(f"Setting project root folder ro {project_root} ")
    mlflow.set_active_model(name=mdl_name)

    with mlflow.start_run(run_name="DrugReviewSentiment"):
        # Log parameters
        mlflow.log_param("cols_to_concat", cols_to_concat)
        mlflow.log_param("polarities_limit", polarities_limit)
        mlflow.log_param("sys_col_rating_nm", sys_col_rating_nm)
        mlflow.log_param("mdl_name", mdl_name)
        dataset = from_pandas(df, name="drug_LibTrain_raw.tsv")
        mlflow.log_input(dataset, context="training")


        # Run your transformation pipeline
        transformed_df = generate_text_transformation(
            df, cols_to_concat, polarities_limit, sys_col_rating_nm, mdl_name
        )

        # Calculate and log metrics (example: sentiment distribution)
        sentiment_counts = transformed_df['mdl_sentiment_lbl'].value_counts().to_dict()
        for sentiment, count in sentiment_counts.items():
            mlflow.log_metric(f"sentiment_{sentiment.lower()}_count", count)

        # Log processed data as artifact
        try:    
            processed_path = os.path.join(project_root,"data/processed/drug_transformed.csv")
            mlflow.log_artifact(processed_path)
        except FileNotFoundError:
            app_logger.error("File not Found: Unable to load Artifact from file ")
        except Exception as e:
            app_logger.error("Unable to load project Artifact...system failed")
            raise(e)

        # Log the custom sentiment pipeline model
        sentiment_model = SentimentPipelineWrapper(mdl_name=mdl_name)
        mlflow.pyfunc.log_model(
            "sentiment_pipeline",
            python_model=sentiment_model,
            registered_model_name="SentimentPipelineModel" 
        )
        app_logger.info("Custom sentiment pipeline model logged to MLflow.")
        
        mlflow.end_run(status="FINISHED")

    model_id = mlflow.get_active_model_id()
    app_logger.info(f"Active Ml model id was running >> {model_id}")

    app_logger.info("MLflow run completed and logged.")

    return "Completed"

def kill_ml_run(run_id:str):
    client = MlflowClient()

    # Set the run to 'KILLED' status
    client.set_terminated(
        run_id=run_id, 
        status="KILLED"
    )
    app_logger.warning(f"{run_id} terminated")
    return None
