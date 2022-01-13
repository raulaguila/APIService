import os
import sys
import configparser
import logging
import logging.config
import cx_Logging

# Check versions
import uvicorn
import fastapi

folder_log = "logs"
folder_cfg = "configs"


class logger():
    def __init__(self, cwd: bool = False) -> None:

        try:

            if cwd:

                self.log_cfg_file = os.path.join(os.path.join(os.getcwd(), folder_cfg), "logging.conf")
                self.log_out_file = os.path.join(os.path.join(os.getcwd(), folder_log), "stdout.log")
                self.std_err_file = os.path.join(os.path.join(os.getcwd(), folder_log), "stderr.log")
                self.std_out_file = os.path.join(os.path.join(os.getcwd(), folder_log), "console.log")

            else:

                self.log_cfg_file = os.path.join(os.path.join(os.path.dirname(sys.executable), folder_cfg), "logging.conf")
                self.log_out_file = os.path.join(os.path.join(os.path.dirname(sys.executable), folder_log), "stdout.log")
                self.std_err_file = os.path.join(os.path.join(os.path.dirname(sys.executable), folder_log), "stderr.log")
                self.std_out_file = os.path.join(os.path.join(os.path.dirname(sys.executable), folder_log), "console.log")

        except Exception as e:

            cx_Logging.Error("logger.init, error: " + e.__str__())

    def log_create_file(self, clear_log: bool = True) -> bool:

        try:

            os.makedirs(os.path.dirname(self.log_out_file), 0o666, True)
            os.makedirs(os.path.dirname(self.std_out_file), 0o666, True)
            os.makedirs(os.path.dirname(self.std_err_file), 0o666, True)

            if clear_log:

                with open(self.log_out_file, 'w'):
                    pass

                with open(self.std_out_file, 'w'):
                    pass

                with open(self.std_err_file, 'w'):
                    pass

            sys.stdout = open(self.std_out_file, 'w')
            sys.stderr = open(self.std_err_file, 'w')

            aux = self.log_out_file.replace('\\', '\\\\') if sys.platform == "win32" else self.log_out_file
            config = configparser.ConfigParser()
            config.read_file(open(self.log_cfg_file))
            config.set("handler_fileHandler", "args", f'("{aux}", "a")')

            with open(self.log_cfg_file, 'w') as f:
                config.write(f)

            return self._start_logger()

        except Exception as ex:

            print("Exception:", ex.__str__())
            return False

    def _start_logger(self) -> bool:

        logging.config.fileConfig(self.log_cfg_file)
        logging.info("Starting system..")
        logging.info(' _________________________________________')
        logging.info(f'| {"package" : <18} | {"version" : >18} |')
        logging.info(f"| {'uvicorn': <18} | {uvicorn.__version__ : >18} |")
        logging.info(f"| {'fastapi': <18} | {fastapi.__version__ : >18} |")
        logging.info('|____________________|____________________|')

        return True
