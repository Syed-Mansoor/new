import os
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
from Diamond.utils import load_object
from Diamond.exception import DiamondException
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelEvaluation:
    def __init__(self):
        pass
    
    def eval_metrics(self, actual, predicted):
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mae = mean_absolute_error(actual, predicted)
        r2 = r2_score(actual, predicted)
        return rmse, mae, r2
    
    def initiate_model_evaluation(self, train_array, test_array):
        try:
            # Log the shapes of train and test arrays
            logging.info("Train array shape: %s", train_array.shape)
            logging.info("Test array shape: %s", test_array.shape)

            X_test, y_test = test_array[:, :-1], test_array[:, -1]
            model_path = os.path.join("artifacts", "model_trainer", "model.pkl")
            model = load_object(file_path=model_path)
            logging.info("Model has been loaded successfully from %s.", model_path)

            # Log model parameters if available
            if hasattr(model, 'get_params'):
                params = model.get_params()
                logging.info("Model parameters: %s", params)
            
            # Check if there's an active MLflow run and end it
            active_run = mlflow.active_run()
            if active_run is not None:
                logging.warning("Ending active run with ID: %s", active_run.info.run_id)
                mlflow.end_run()
            
            # Start a new MLflow run
            with mlflow.start_run():
                prediction = model.predict(X_test)

                # Log predictions and their shape
                logging.info("Predictions made for test data. Shape of predictions: %s", prediction.shape)
                logging.info("Predictions: %s", prediction[:10])  # Log the first 10 predictions

                rmse, mae, r2 = self.eval_metrics(y_test, prediction)
                logging.info("Computed metrics: RMSE: %f, MAE: %f, R^2: %f", rmse, mae, r2)

                mlflow.log_metric('rmse', rmse)
                mlflow.log_metric('r2', r2)
                mlflow.log_param('mae', mae)

                tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme
                if tracking_url_type_store != 'file':
                    mlflow.sklearn.log_model(model, 'model', registered_model_name='Diamond')
                else:
                    mlflow.sklearn.log_model(model, 'model')
                logging.info("Model and metrics logged successfully.")

        except Exception as e:
            logging.error("Error occurred during model evaluation: %s", str(e))
            raise DiamondException(e, sys)
