import sys
from networksecurity.logging_utils import logger

class Custom_Exception(Exception):
    def __init__(self, err_message, err_details: sys):
        self.err_message = err_message
        _, _, exc_tb = err_details.exc_info()
        
        self.err_line = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f'Error in {self.file_name}\nLine Number: {self.err_line}\nDetails: {self.err_message}'
