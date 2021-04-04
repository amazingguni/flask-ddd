
import abc
from typing import List
from app.order.query.dto.order_summary import OrderSummary


class OrderSummaryDao(abc.ABC):
    @abc.abstractmethod
    def select_by_orderer(self, orderer_id:int):
        raise NotImplementedError
    
    # List<OrderSummary> select(Specification<OrderSummary> spec, int firstRow, int maxResults);
    # long counts(Specification<OrderSummary> spec);