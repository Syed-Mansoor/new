import os
import sys

import numpy as np
import pandas as pd
from phising.entity.config_entity import USvisaPredictorConfig
from phising.entity.s3_estimator import USvisaEstimator
from phising.exception import PhishingException
from phising.logger import logging
from phising.utils.main_utils import read_yaml_file
from pandas import DataFrame



class PhishingData:
    def __init__(self,
    	having_IP_Address,
        URL_Length,
        Shortining_Service,
        having_At_Symbol,
        double_slash_redirect,
        Prefix_Suffix,
        having_Sub_Domain,
        SSLfinal_State,
        Domain_registeration_length,
        Favicon,
        port,
        HTTPS_token,
        Request_URL,
        URL_of_Anchor,
        Links_in_tags,
        SFH,
        Submitting_to_email,
        Abnormal_URL,
        Redirect,
        on_mouseover,
        RightClick,
        popUpWidnow,
        Iframe,
        age_of_domain,
        DNSRecord,
        web_traffic,
        Page_Rank,
        Google_Index,
        Links_pointing_to_page,
        Statistical_report
        ):
        """
        Phishing Data constructor
        Input:all features of the trained model for prediction
        """
        try:
            self.having_IP_Address = having_IP_Address
            self.URL_Length = URL_Length
            self.Shortining_Service = Shortining_Service
            self.having_At_Symbol = having_At_Symbol
            self.double_slash_redirect = double_slash_redirect
            self.Prefix_Suffix = Prefix_Suffix
            self.having_Sub_Domain = having_Sub_Domain
            self.SSLfinal_State = SSLfinal_State
            self.Domain_registeration_length = Domain_registeration_length
            self.Favicon = Favicon
            self.port= port
            self.HTTPS_token= HTTPS_token
            self.Request_URL = Request_URL
            self.URL_of_Anchor = URL_of_Anchor
            self.Links_in_tags = Links_in_tags
            self.SFH = SFH
            self.Submitting_to_email = Submitting_to_email
            self.Abnormal_URL = Abnormal_URL
            self.Redirect = Redirect
            self.on_mouseover = on_mouseover
            self.RightClick=RightClick
            self.popUpWidnow= popUpWidnow
            self.Iframe = Iframe
            self.age_of_domain = age_of_domain
            self.DNSRecord = DNSRecord
            self.web_traffic =  web_traffic
            self.Page_Rank =    Page_Rank
            self.Google_Index = Google_Index
            self.Links_pointing_to_page = Links_pointing_to_page
            self.Statistical_report = Statistical_report
        except Exception as e:
            raise PhishingException(e,sys)

    def get_usvisa_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            
            phishing_input_dict = self.get_phishing_data_as_dict()
            return DataFrame(phishing_input_dict)
        
        except Exception as e:
            raise PhishingException(e, sys) from e


    def get_usvisa_data_as_dict(self):
        """
        This function returns a dictionary from USvisaData class input 
        """
        logging.info("Entered get_usvisa_data_as_dict method as USvisaData class")

        try:
            input_data = {
                "having_IP_Address": [self.having_IP_Address],
                "URL_Length": [self.URL_Length],
                "Shortining_Service": [self.Shortining_Service],
                "having_At_Symbol": [self.having_At_Symbol],
                "double_slash_redirect": [self.double_slash_redirect],
                "Prefix_Suffix": [self.Prefix_Suffix],
                "having_Sub_Domain": [self.having_Sub_Domain],
                "SSLfinal_State": [self.SSLfinal_State],
                "Domain_registeration_length": [self.Domain_registeration_length],
                "Favicon": [self.Favicon],
                "port": [self.port],
                "HTTPS_token": [self.HTTPS_token],
                "Request_URL": [self.Request_URL],
                "URL_of_Anchor": [self.URL_of_Anchor],
                "Links_in_tags": [self.Links_in_tags],
                "SFH": [self.SFH],
                "Submitting_to_email": [self.Submitting_to_email],
                "Abnormal_URL": [self.Abnormal_URL],
                "Redirect": [self.Redirect],
                "on_mouseover": [self.on_mouseover],
                "RightClick": [self.RightClick],
                "popUpWidnow": [self.popUpWidnow],
                "Iframe": [self.Iframe],
                "age_of_domain": [self.age_of_domain],
                "DNSRecord": [self.DNSRecord],
                "web_traffic": [self.web_traffic],
                "Page_Rank": [self.Page_Rank],
                "Google_Index": [self.Google_Index],
                "Links_pointing_to_page": [self.Links_pointing_to_page],
                "Statistical_report": [self.Statistical_report],

            }
            logging.info('Created phishing data')
            logging.info("Exited get_phishing_data_as_dict method as PhishingData class")
            return input_data

        except Exception as e:
            raise PhishingException(e, sys) from e


class PhishingClassifier:

    def __init__(self, prediction_pipeline_config: USvisaPredictorConfig = USvisaPredictorConfig(),) -> None:   
        """
#         :param prediction_pipeline_config: Configuration for prediction the value
#         """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise PhishingException(e, sys)


    def predict(self, dataframe) -> str:
        """
        This is the method of USvisaClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of USvisaClassifier class")
            model = USvisaEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise PhishingException(e, sys)
  