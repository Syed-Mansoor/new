import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from pathlib import Path
from Diamond.logger import logging
from Diamond.exception import DiamondException
import sys
import os

class DataIngestionConfig:
    def __init__(self):
        # Create artifact directories without timestamp
        self.artifacts_dir = os.path.join('artifacts', 'data_ingestion')
        
        # Define paths using the consistent directory
        self.raw_data_path: str = os.path.join(self.artifacts_dir, 'feature_store', 'raw.csv')
        self.train_data_path: str = os.path.join(self.artifacts_dir, 'ingested', 'train.csv')
        self.test_data_path: str = os.path.join(self.artifacts_dir, 'ingested', 'test.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Data ingestion process has started')
        try:
            # Step 1: Read the raw data
            logging.info('Attempting to read raw data from gemstone.csv...')
            data = pd.read_csv(Path(os.path.join('notebook/data', 'gemstone.csv')))
            logging.info(f"Successfully read raw data with {data.shape[0]} rows and {data.shape[1]} columns")

            # Step 2: Create directories for feature store and ingested if they don't exist
            logging.info('Checking if directories for feature store and ingested data exist...')
            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            logging.info(f'Directories created successfully: {self.ingestion_config.artifacts_dir}')
            
            # Step 3: Save raw data to the feature store
            logging.info(f'Saving raw data to {self.ingestion_config.raw_data_path}...')
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Raw data saved successfully to the feature store")

            # Step 4: Split the data into train and test sets
            logging.info("Splitting the data into train and test sets with a 75%/25% ratio...")
            train_data, test_data = train_test_split(data, test_size=0.25, random_state=42)
            logging.info(f"Train set: {train_data.shape[0]} rows, Test set: {test_data.shape[0]} rows")
            
            # Step 5: Save train and test data
            logging.info(f'Saving train data to {self.ingestion_config.train_data_path}...')
            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            logging.info(f"Train data saved successfully at {self.ingestion_config.train_data_path}")

            logging.info(f'Saving test data to {self.ingestion_config.test_data_path}...')
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info(f"Test data saved successfully at {self.ingestion_config.test_data_path}")

            logging.info('Data ingestion process completed successfully')
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error(f"Exception occurred during data ingestion: {str(e)}")
            raise DiamondException(e, sys)
