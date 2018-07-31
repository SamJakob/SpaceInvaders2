import abc

class MovementControls(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError("This controller method could not be initialized.")

    @abc.abstractmethod
    def moveLeft(self):
        raise NotImplementedError("Move Left feature is not implemented. You cannot use this controller method.")

    @abc.abstractmethod
    def moveRight(self):
        raise NotImplementedError("Move Right feature is not implemented. You cannot use this controller method.")

    @abc.abstractmethod
    def shoot(self):
        raise NotImplementedError("Shoot feature is not implemented. You cannot use this controller method.")

    @abc.abstractmethod
    def feedback(self):
        raise NotImplementedError("Feedback feature is not implemented. You cannot use this controller method.")
