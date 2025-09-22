from enum import Enum


class APPError(Enum):
    '''
    Enum for internal application errors.
    '''
    SOMETHING_WENT_WRONG = {"message": "Something went wrong"}
