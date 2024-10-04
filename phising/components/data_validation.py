import json
import sys
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from pandas import DataFrame

from phising.exception import PhishingException
from phising.logger import logging
from phising.utils.main_utils import read_yaml_file, write_yaml_file
from phising.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from phising.entity.config_entity import DataValidationConfig
from phising.constants import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            logging.info("DataValidation initialized with schema configuration.")
        except Exception as e:
            raise PhishingException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            expected_columns = len(self._schema_config["ColName"])
            status = len(dataframe.columns) == expected_columns
            logging.info(f"Number of columns validation status: {status}")
            return status
        except Exception as e:
            raise PhishingException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns.tolist()
            missing_columns = []

            # Check for all columns defined in the schema
            for column in self._schema_config["ColName"]:
                if column not in dataframe_columns:
                    missing_columns.append(column)

            if missing_columns:
                logging.warning(f"Missing columns: {missing_columns}")

            return not missing_columns
        except Exception as e:
            raise PhishingException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Data read successfully from {file_path}")
            return df
        except Exception as e:
            raise PhishingException(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            logging.info(f"{n_drifted_features}/{n_features} features drift detected.")

            return json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
        except Exception as e:
            raise PhishingException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation process.")
            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            validation_error_msg = ""
            validations = [
                (self.validate_number_of_columns(train_df), "training"),
                (self.validate_number_of_columns(test_df), "testing"),
                (self.is_column_exist(train_df), "training"),
                (self.is_column_exist(test_df), "testing")
            ]

            for status, phase in validations:
                if not status:
                    validation_error_msg += f"Columns are missing in {phase} dataframe. "

            validation_status = not validation_error_msg

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                validation_error_msg = "Drift detected" if drift_status else "Drift not detected"
            else:
                logging.error(f"Validation errors: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg.strip(),
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact created: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise PhishingException(e, sys)
