from dependency_injector import containers, providers

from flask import Flask
from sqlalchemy.orm.scoping import scoped_session

from .catalog.infra.repository.sql_category_repository import SqlCategoryRepository
from .catalog.infra.repository.sql_product_repository import SqlProductRepository
from .catalog.application.product_service import ProductService
from .order.infra.dao.sql_order_summary_dao import SqlOrderSummaryDao
from .order.infra.repository.sql_order_repository import SqlOrderRepository
from .order.infra.repository.sql_order_repository import SqlOrderRepository
from .cart.infra.repository.sql_cart_repository import SqlCartRepository
from .order.query.application.order_view_list_service import OrderViewListService
from .cart.application.add_cart_service import AddCartService
from .order.application.place_order_service import PlaceOrderService
from .order.application.cancel_order_service import CancelOrderService
from .order.infra.paygate.external_refund_service import ExternalRefundService

# https://github.com/ets-labs/python-dependency-injector/issues/344


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    app = providers.Dependency(instance_of=Flask)
    session = providers.Dependency(instance_of=scoped_session)

    category_repository = providers.Factory(
        SqlCategoryRepository, session=session)
    product_repository = providers.Factory(
        SqlProductRepository, session=session)
    product_service = providers.Factory(
        ProductService, product_repository=product_repository, category_repository=category_repository)
    order_summary_dao = providers.Factory(SqlOrderSummaryDao, session=session)
    order_view_list_service = providers.Factory(
        OrderViewListService, order_summary_dao=order_summary_dao)
    order_repository = providers.Factory(
        SqlOrderRepository, session=session)
    cart_repository = providers.Factory(
        SqlCartRepository, session=session)
    add_cart_service = providers.Factory(
        AddCartService, cart_repository=cart_repository)
    place_order_service = providers.Factory(
        PlaceOrderService, cart_repository=cart_repository, order_repository=order_repository)
    refund_service = providers.Factory(ExternalRefundService)
    cancel_order_service = providers.Factory(
        CancelOrderService, order_repository=order_repository, refund_service=refund_service)
