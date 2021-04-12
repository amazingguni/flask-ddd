from typing import List
from dataclasses import dataclass
from app.user.domain.user import User
from .order_product import OrderProduct
from ..domain.shipping_info import ShippingInfo


@dataclass
class OrderRequest:
    order_products: List[OrderProduct]
    orderer: User
    shipping_info: ShippingInfo
