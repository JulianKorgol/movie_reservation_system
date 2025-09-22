from enum import Enum


class PublicError(Enum):
    '''
    Enum for public-facing errors with HTTP status codes. Should be used in API responses if needed.
    '''
    SOMETHING_WENT_WRONG = {"html_code": 500, "message": "Something went wrong"}
    INCORRECT_REQ_DATA = {"html_code": 422, "message": "Incorrect request data"}
