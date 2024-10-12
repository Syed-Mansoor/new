import os
import sys
from Diamond.exception import DiamondException
from Diamond.logger import logging
from dataclasses import dataclass
from Diamond.utils import save_object,evaluate_model
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
from sklearn.tree import DecisionTreeRegressor
from catboost import CatBoostRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor 
from xgboost import XGBRegressor


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model_trainer','model.pkl')
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self,train_array, test_array):
        try:
            logging.info('Split training and test input data')
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                'LinearRegression':LinearRegression(),
                'Lasso':Lasso(),
                'Ridge':Ridge(),
                'Elasticnet':ElasticNet(),
                'DecisionTree':DecisionTreeRegressor(),
                'RandomForest':RandomForestRegressor(),
                'AdaBoost':AdaBoostRegressor(),
                'GradientBoosting':GradientBoostingRegressor(),
                'XGBoost':XGBRegressor(),
                'CatBoost':CatBoostRegressor(verbose=False),
                'KNeighbors':KNeighborsRegressor()
            }
            model_report = evaluate_model(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)
            ## To get best model score from each model
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            logging.info(f'Best model found, Model Name: {best_model_name}, R2 Score: {best_model_score}')
            logging.info(f'Checking if {os.path.exists(self.model_trainer_config.trained_model_file_path)}')
            if not os.path.exists(self.model_trainer_config.trained_model_file_path):
                logging.info(f'{self.model_trainer_config.trained_model_file_path} created')
                save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model)
            else:
                logging.info(f'{self.model_trainer_config.trained_model_file_path} is already present')

        except Exception as e:
            logging.info('Exception occured during model training')
            raise DiamondException(e,sys)