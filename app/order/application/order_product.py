from dataclasses import dataclass


@dataclass
class OrderProduct:
    product_id: int
    quantity: int
