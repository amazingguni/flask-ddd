from typing import List
from dataclasses import dataclass
from app.user.domain.user import User
from app.order.domain.shipping_info import ShippingInfo
from .order_product import OrderProduct


@dataclass
class OrderRequest:
    order_products: List[OrderProduct]
    orderer: User
    shipping_info: ShippingInfo
