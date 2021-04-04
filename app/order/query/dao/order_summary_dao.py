import abc


class OrderSummaryDao(abc.ABC):
    @abc.abstractmethod
    def select_by_orderer(self, orderer_id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def counts(self, filters: dict):
        raise NotImplementedError

    @abc.abstractmethod
    def select(self, filters: dict, offset: int, limit: int):
        raise NotImplementedError
