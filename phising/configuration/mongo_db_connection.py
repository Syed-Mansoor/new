import sys
import os
import pymongo
import certifi
from phising.exception import PhishingException
from phising.logger import logging
from phising.constants import DATABASE_NAME, MONGODB_URL_KEY

# Use certifi to get the CA certificates for TLS connections
ca = certifi.where()

class MongoDBClient:
    """
    Class Name : MongoDBClient
    Description : This class manages the MongoDB client connection and database access.
    """
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        """
        Initializes the MongoDB client and connects to the specified database.
        
        :param database_name: Name of the MongoDB database to connect to.
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                
                # Create a MongoDB client instance
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                logging.info("MongoDB client initialized successfully.")
                
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"Connected to MongoDB database: {self.database_name}")
        
        except pymongo.errors.ConnectionError as ce:
            logging.error(f"Connection error: {str(ce)}")
            raise PhishingException(ce, sys)
        except Exception as e:
            logging.error(f"An error occurred while connecting to MongoDB: {str(e)}")
            raise PhishingException(e, sys)

    def get_collection(self, collection_name: str):
        """
        Retrieves a specific collection from the MongoDB database.

        :param collection_name: Name of the collection to retrieve.
        :return: Collection object.
        """
        try:
            collection = self.database[collection_name]
            logging.info(f"Retrieved collection: {collection_name} from database: {self.database_name}")
            return collection
        except Exception as e:
            logging.error(f"Failed to get collection: {collection_name}. Error: {str(e)}")
            raise PhishingException(e, sys)
