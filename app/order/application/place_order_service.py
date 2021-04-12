from .order_request import OrderRequest


class PlaceOrderService:
    def __init__(self, product_repository, order_repository):
        self.product_repository = producdt_repository
        self.order_repository = order_repository

    def place_order(self, order_request: OrderRequest):

        order_lines = []
        for op in order_request.order_products:
            product = self.product_repository.find_by_id(op.product_id)
            order_lines.add(OrderLine(product=product, quantity=op.quantity))

        order = Order(
            orderer=order_request.orderer,
            order_lines=order_lines,
            shipping_info=order_request.shipping_info,
            OrderState.PAYMENT_WAITING)

        self.order_repository.save(order)
        return order
