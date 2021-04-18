
import abc


class RefundService(abc.ABC):
    @abc.abstractmethod
    def refund(self, order_id: int):
        raise NotImplementedError
