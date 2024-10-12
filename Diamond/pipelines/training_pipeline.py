from Diamond.components.data_ingestion import DataIngestion
from Diamond.components.data_transformation import DataTransformation
from Diamond.logger import logging
from Diamond.exception import DiamondException
import os
import sys
import pandas as pd

class TrainingPipeline:
    def __init__(self):
        try:
            self.data_ingestion = DataIngestion()
            self.data_transformation = DataTransformation()

        except Exception as e:
            raise DiamondException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            train_data_path,test_data_path = self.data_ingestion.initiate_data_ingestion()
            return train_data_path,test_data_path
        except Exception as e:
            raise DiamondException(e,sys)
        
    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:
            return self.data_transformation.initialize_data_transformation(train_path=train_data_path,test_path=test_data_path) 
        except Exception as e:
            raise DiamondException(e,sys)
        
    def run_pipeline(self):
        try:
        # Step 1: Data Ingestion
            logging.info('Pipeline has been started')
            logging.info('Data Ingestion Initiated')
            train_data_path, test_data_path = self.initiate_data_ingestion()  # Correct unpacking
            logging.info('Data Ingestion Completed')
            
            logging.info('Data Transformation Initiated')
            # Step 2: Data Transformation
            train_arr, test_arr= self.initiate_data_transformation(train_data_path=train_data_path, test_data_path=test_data_path)
            logging.info('Data Transformation Completed')
            
            # Step 3: Model Training
    
            
            logging.info('Data transformation completed')
        except Exception as e:
            raise DiamondException(e, sys)
