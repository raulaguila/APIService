import uvicorn
import threading
import cx_Logging
import logging
import logging.config
import src.app

from src.log.log import logger
from uvicorn.config import LOGGING_CONFIG


class AppServer:

    def __init__(self, host: str = "127.0.0.1", port: int = 8004, reload: bool = True) -> None:

        logging.info("Is being called..")  # It's not coming in here
        self.host = host
        self.port = port
        self.reload = reload

        try:

            # %(name)s : uvicorn, uvicorn.error, ... . Not insightful at all.
            # LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
            # LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"

            # date_fmt = "%Y-%m-%d %H:%M:%S"
            # LOGGING_CONFIG["formatters"]["default"]["datefmt"] = date_fmt
            # LOGGING_CONFIG["formatters"]["access"]["datefmt"] = date_fmt
            ##

            self.config = uvicorn.Config(app=src.app.app, host=self.host, port=self.port, reload=self.reload)
            self.server = uvicorn.Server(self.config)
            self.server.install_signal_handlers = lambda: None  # Need this line, or the server wont start
            self.is_running = False

            logging.info("AppServer.server created: " + str(self.server is not None))

        except Exception as e:

            logging.error("AppServer.init error: " + e.__str__())

    def run(self):

        try:

            logging.info("Starting API...")
            self.server.run()

        except Exception as e:

            logging.error("AppServer.run error: " + e.__str__())
            self.is_running = False

    def start(self):

        try:

            self.is_running = True
            self.proc = threading.Thread(target=self.run, args=())
            self.proc.setDaemon(True)
            self.proc.start()

        except Exception as e:

            logging.error("AppServer.stop error: " + e.__str__())

    def stop(self):

        try:

            self.is_running = False
            if self.proc.is_alive():
                self.proc.join()

        except Exception as e:

            logging.error("AppServer.stop error: " + e.__str__())


class Handler:

    def __init__(self):

        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()
        self.server = AppServer()
        self.server.__init__()

    def configLog(self):

        cx_Logging.StartLogging(cx_Logging.GetLoggingFileName(), cx_Logging.INFO, prefix="%d %t %l")

        if logger().log_create_file(clear_log=True):

            cx_Logging.Info("Logging configured successfully")

        else:

            cx_Logging.Erro("Logging configured successfully")

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

            logging.error("Handler.run error: " + e.__str__())

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

            logging.error("Handler.stop error: " + e.__str__())

    # called in run
    def main(self):

        try:

            self.server.start()

        except Exception as e:

            logging.error("Handler.main error: " + e.__str__())
