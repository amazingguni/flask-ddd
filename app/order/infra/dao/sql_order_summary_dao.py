from app.order.query.dao.order_summary_dao import OrderSummaryDao
from app.order.domain.order import Order
from app.catalog.domain.product import Product


class SqlOrderSummaryDao(OrderSummaryDao):
    def __init__(self, session):
        self.session = session
        
    def select_by_orderer(self, orderer_id):
        query = self.session.query(Order.id)
        # print(query.all())
        return 

        '''
        @Immutable
        @Subselect("select o.order_number as number, " +
        "o.version, " +
        "o.orderer_id, " +
        "o.orderer_name, " +
        "o.total_amounts, " +
        "o.receiver_name, " +
        "o.state, " +
        "o.order_date, " +
        "p.product_id, " +
        "p.name as product_name " +
        "from purchase_order o inner join order_line ol " +
        "    on o.order_number = ol.order_number " +
        "    cross join product p " +
        "where " +
        "ol.line_idx = 0 " +
        "and ol.product_id = p.product_id"
        '''
        '''
         TypedQuery<OrderSummary> query = em.createQuery("select os from OrderSummary " +
                "os where os.ordererId = :ordererId " +
                "order by os.orderDate desc", OrderSummary.class);
        query.setParameter("ordererId", ordererId);'''