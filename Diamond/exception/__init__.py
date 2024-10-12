import os
import sys

def error_message_detail(error,error_detail:sys):
    """
    Function to get the error message detail

    error: object of class Exception
    error_detail: object of class sys

    Returns:
        string: error message
    """
    _,_,exc_tb = error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )

    return error_message




class DiamondException(Exception):
    def __init__(self,error_message,error_detail:sys):
        """
        :param error_message: error message in string format
        :param error_detail: object of sys module
        """
        
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message,
            error_detail=error_detail
        )

    def __str__(self):
        
        
        """
        Return the error message of the exception instance

        Returns:
            string: error message
        """

        return self.error_message