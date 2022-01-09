import logging
import src.app as Application

from src.log.log import logger

if __name__ == "__main__":

    if logger(cwd=True).log_create_file(clear_log=True):

        logging.info("Starting test...")
        Application.run()

    else:

        logging.error("Error to start test...")
