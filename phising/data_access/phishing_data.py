import sys
import pandas as pd
import numpy as np
import logging
from typing import Optional
from phising.configuration.mongo_db_connection import MongoDBClient
from phising.constants import DATABASE_NAME
from phising.exception import PhishingException

class PhishingData:
    """
    This class helps to export the entire MongoDB record as a pandas DataFrame
    """

    def __init__(self):
        """
        Initialize the MongoDB client
        """


        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
            logging.info(f"connected to MongoDB database : {DATABASE_NAME}")
        except Exception as e:
            raise PhishingException(e,sys)
        # try:
        #     self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        #     logging.info(f"Connected to MongoDB database: {DATABASE_NAME}")
        # except Exception as e:
        #     logging.error(f"Failed to connect to MongoDB: {str(e)}")
        #     raise USvisaException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Export the entire MongoDB collection as a DataFrame.
        
        :param collection_name: MongoDB collection name to export
        :param database_name: Optional MongoDB database name, defaults to the main database
        :return: pd.DataFrame containing the collection's data
        """
        try:
            # Use the provided database name if specified
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.get_collection(collection_name)  # Using method to get collection

            # Fetch data from MongoDB collection
            logging.info(f"Fetching data from collection: {collection_name}")
            data = list(collection.find())

            # Check if the data is empty
            if not data:
                logging.warning(f"No data found in collection: {collection_name}")
                return pd.DataFrame()  # Return empty DataFrame if no data is found

            logging.info(f"Number of documents retrieved: {len(data)}")
            logging.info(f"Sample documents: {data[:5]}")  # Log first 5 documents for debugging

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Drop MongoDB's _id field if present
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
                logging.info("Dropped '_id' column from DataFrame")

            # Replace 'na' strings with NaN
            df.replace({"na": np.nan}, inplace=True)
            logging.info("Replaced 'na' with NaN in DataFrame")

            return df

        except Exception as e:
            logging.error(f"Error occurred while exporting collection as DataFrame: {str(e)}")
            raise PhishingException(e, sys)
