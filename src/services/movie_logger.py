import logging
import threading
from typing import Optional

from src.interfaces.i_movie_logger import IMovieLogger


class MovieLogger(IMovieLogger):
    def __init__(self, log_file='movies.log', flush_interval: float = 1.0):

        self.logger = logging.getLogger('MovieIDLogger')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        self.file_handler = file_handler
        self.flush_interval = flush_interval
        self._flush_timer: Optional[threading.Timer] = None
        self._lock = threading.Lock()

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self._start_periodic_flush()

    def _flush_all_handlers(self):
        with self._lock:
            for handler in self.logger.handlers:
                if hasattr(handler, 'flush'):
                    handler.flush()

    def _periodic_flush(self):
        self._flush_all_handlers()
        self._flush_timer = threading.Timer(self.flush_interval, self._periodic_flush)
        self._flush_timer.daemon = True
        self._flush_timer.start()

    def _start_periodic_flush(self):
        self._flush_timer = threading.Timer(self.flush_interval, self._periodic_flush)
        self._flush_timer.daemon = True
        self._flush_timer.start()

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)
