import json
import logging


def map_log_level(levelno):
    # Map Python logging levels to browser stack executor levels
    level_map = {
        logging.DEBUG: "debug",
        logging.INFO: "info",
        logging.WARNING: "warn",
        logging.ERROR: "error",
        logging.CRITICAL: "error"
    }
    return level_map.get(levelno, "info")


class BrowserStackHandler(logging.Handler):
    def __init__(self, driver=None):
        super().__init__()
        self.driver = driver

    def set_driver(self, driver):
        self.driver = driver

    def emit(self, record):
        if self.driver is None:
            return
        level = map_log_level(record.levelno)
        executor_object = {
            'action': 'annotate',
            'arguments': {
                'data': f"{record.msg}",
                'level': f'{level}'
            }
        }
        # browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
        # self.driver.execute_script(browserstack_executor)
