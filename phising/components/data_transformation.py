from phising.constants import TARGET_COLUMN, SCHEMA_FILE_PATH
from phising.entity.config_entity import DataTransformationConfig
from phising.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from phising.exception import PhishingException
from phising.logger import logging
from phising.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, remove_unwanted_spaces
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import RandomOverSampler


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise PhishingException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise PhishingException(e, sys)

    def get_data_transformer_object(self) -> SimpleImputer:
        logging.info("Entered get_data_transformer_object method of DataTransformation class")
        try:
            # Use the correct attribute for the validated data path
            dataframe = DataTransformation.read_data(
                file_path=self.data_ingestion_artifact.trained_file_path  # Change this if needed
            )
            dataframe = remove_unwanted_spaces(dataframe)
            dataframe.replace('?', np.NaN, inplace=True)

            return SimpleImputer(strategy='most_frequent')
        except Exception as e:
            raise PhishingException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object")

                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]

                input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
                target_feature_test_df = test_df[TARGET_COLUMN]

                logging.info("Got train and test features")

                # Prepare data for oversampling
                X = train_df.drop(columns=TARGET_COLUMN)
                y = np.where(train_df[TARGET_COLUMN] == -1, 0, 1)

                sampler = RandomOverSampler()
                x_sampled, y_sampled = sampler.fit_resample(X, y)

                X_train, X_test, y_train, y_test = train_test_split(x_sampled, y_sampled, test_size=0.2)

                x_train_scaled = preprocessor.fit_transform(X_train)
                x_test_scaled = preprocessor.transform(X_test)

                # Saving processed data
                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=x_train_scaled)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=x_test_scaled)

                logging.info("Saved the preprocessor and transformed data")

                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                )
                logging.info("Exited initiate_data_transformation method of DataTransformation class")
                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise PhishingException(e, sys) from e
