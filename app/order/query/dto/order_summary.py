from dataclasses import dataclass

@dataclass
class OrderSummary:
    order_id: int
    orderer_id: int
    orderer_name:str
    total_amounts:int
    receiver_name:str
    state:str
    order_date:str
    product_id:int
    product_name:str
