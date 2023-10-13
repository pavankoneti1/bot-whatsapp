from rest_framework.exceptions import APIException
from rest_framework import status

class BaseApiException(APIException):
    '''
    API for the Exception of base Exception
    '''
    status_code = status.HTTP_400_BAD_REQUEST
    err_message = 'Exception occured'
    err_title = 'Exception occured'
    err_dev_message = err_message

    def construct_details(self):
        self.default_detail = {
            'err_message' : self.err_message,
            'err_title' : self.err_title,
            'err_dev_message' : self.err_dev_message,
        }

    def __init__(self, *args, **kwargs):
        self.construct_details()
        super().__init__(*args, **kwargs)


class InvalidMobileNumberException(BaseApiException):
    err_message = 'Mobile number is Invalid'
    err_title = 'Invalid mobile number'

class InvalidOtpException(BaseApiException):
    err_message = 'OTP is Invalid or expired'
    err_title = 'Invalid OTP'