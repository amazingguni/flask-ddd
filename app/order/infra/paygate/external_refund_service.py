from app.order.domain.refund_service import RefundService


class ExternalRefundService(RefundService):
    def refund(self, order_id: int):
        print(f'Order id "{order_id}" is refund')
