import uvicorn
import threading
import cx_Logging
import logging
import logging.config
import src.app

from src.log.log import logger


class AppServer:

    def __init__(self, host: str = "127.0.0.1", port: int = 8004, reload: bool = False) -> None:

        logging.info("Is being called..")
        self.host = host
        self.port = port
        self.reload = reload

        try:

            self.config = uvicorn.Config(app=src.app.app, host=self.host, port=self.port, reload=self.reload)
            self.server = uvicorn.Server(self.config)
            self.server.install_signal_handlers = lambda: None  # Need this line, or the server wont start

            logging.info("AppServer.server created: " + str(self.server is not None))

        except Exception as e:

            logging.error("AppServer.init error: " + e.__str__())

    def run(self):

        try:

            logging.info("Starting API...")
            self.server.run()

        except Exception as e:

            logging.error("AppServer.run error: " + e.__str__())

    def start(self):

        try:

            self.proc = threading.Thread(target=self.run, args=())
            self.proc.setDaemon(True)
            self.proc.start()

        except Exception as e:

            logging.error("AppServer.stop error: " + e.__str__())

    def stop(self):

        try:

            logging.info("Stopping API..")
            if self.proc.is_alive():
                self.server.shutdown()

        except Exception as e:

            logging.error("AppServer.stop error: " + e.__str__())


class Handler:

    def __init__(self):

        self.stopEvent = threading.Event()
        self.stopRequestedEvent = threading.Event()

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

            self.server = AppServer()
            self.server.start()

        except Exception as e:

            logging.error("Handler.main error: " + e.__str__())
