import sys, os

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()

    file_name= exc_tb.tb_frame.f_code.co_filename
    
    error_message="Error occured python script name [{0}] line number [{1}] error message"

class SensorException(Exception):
    def __init__(self,error_message,error_details:sys):
        
