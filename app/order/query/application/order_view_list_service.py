from ...domain.order import Order
from ...query.dto.order_summary import OrderSummary

def get_list():
    return OrderSummary.query.first()
