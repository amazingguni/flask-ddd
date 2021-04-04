from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderSummary:
    order_id: int
    orderer_id: int
    orderer_username: str
    total_amounts: int
    receiver_name: str
    state: str
    order_date: datetime
    product_id: int
    product_name: str
