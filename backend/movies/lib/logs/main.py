import logging


class AppLogger:
  def __init__(self) -> None:
    self.__logger = logging.getLogger('app')
    self.__logger.setLevel(logging.ERROR)

    # Create a file handler
    file_handler = logging.FileHandler('app.log')

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    self.__logger.addHandler(file_handler)

  def error(self, message: str) -> None:
    self.__logger.error(message)


app_logger = AppLogger()
