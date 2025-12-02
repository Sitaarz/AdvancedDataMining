import abc

class IMovieLogger(abc.ABC):
    @abc.abstractmethod
    def log_info(self, message: str):
        pass

    @abc.abstractmethod
    def log_error(self, log_info: str):
        pass
