import uvicorn
import threading
import cx_Logging
import logging

from src.log.log import logger
from uvicorn.config import LOGGING_CONFIG


class AppServer:

    def __init__(self, host: str = "0.0.0.0", port: int = 5050, reload: bool = False) -> None:

        self.host = host
        self.port = port
        self.reload = reload

        try:

            LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)-23s | %(levelname)-8s | %(client_addr)-45s | "%(request_line)s" %(status_code)s'

            self.config = uvicorn.Config(app="src.app:app", host=self.host, port=self.port, reload=self.reload)
            self.server = uvicorn.Server(self.config)
            self.server.install_signal_handlers = lambda: None  # Need this line, or the server wont start

            if self.server is not None:

                logging.info(f"AppServer.server created at 127.0.0.1:{self.port}")
                logging.info(f"AppServer.server documentation at 127.0.0.1:{self.port}/docs")

        except Exception as e:

            logging.error(f"AppServer.server error[{e.__traceback__.tb_lineno}]: {e.__str__()}")

    def run(self):

        try:

            logging.info("Starting API...")
            self.server.run()

        except Exception as e:

            logging.error(f"AppServer.run error[{e.__traceback__.tb_lineno}]: {e.__str__()}")

    def start(self):

        try:

            self.proc = threading.Thread(target=self.run, args=())
            self.proc.setDaemon(True)
            self.proc.start()

        except Exception as e:

            logging.error(f"AppServer.start error[{e.__traceback__.tb_lineno}]: {e.__str__()}")

    def stop(self):

        try:

            logging.info("Stopping API..")
            if self.proc.is_alive():
                self.server.shutdown()

        except Exception as e:

            logging.error(f"AppServer.stop error[{e.__traceback__.tb_lineno}]: {e.__str__()}")


class Handler:

    def __init__(self):

        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()

    def session_changed(self, sessionId, eventTypeId):

        self.server.stop()

        self.server.start()

    def configLog(self):

        cx_Logging.StartLogging(cx_Logging.GetLoggingFileName(), cx_Logging.INFO, prefix="%d %t %l")

        if logger().log_create_file(clear_log=True):

            cx_Logging.Info("Logging configured successfully")

        else:

            cx_Logging.Erro("Logging can\'t be configured successfully")

    # called when the service is starting
    def initialize(self, configFileName):

        self.configLog()

    # called after initialize
    def run(self):

        try:

            logging.info("Starting Service")
            self.main()
            self.stopRequestedEvent.wait()
            self.stopEvent.set()

        except Exception as e:

            logging.error(f"Handler.run error[{e.__traceback__.tb_lineno}]: {e.__str__()}")

    def Run(self):
        pass

    # called when the service is being stopped by the service manager GUI
    def stop(self):
        try:

            logging.info("Stopping Service")
            self.server.stop()
            self.stopRequestedEvent.set()
            self.stopEvent.wait()
            # How to stop the server???

        except Exception as e:

            logging.error(f"Handler.stop error[{e.__traceback__.tb_lineno}]: {e.__str__()}")

    # called in run
    def main(self):

        try:

            self.server = AppServer()
            self.server.start()

        except Exception as e:

            logging.error(f"Handler.main error[{e.__traceback__.tb_lineno}]: {e.__str__()}")
