from dependency_injector import containers, providers

from flask import Flask
# from flask_sqlalchemy import SessionBase
from sqlalchemy.orm.scoping import scoped_session

from .catalog.infra.repository.sql_category_repository import SqlCategoryRepository
from .catalog.infra.repository.sql_product_repository import SqlProductRepository
from .order.infra.dao.sql_order_summary_dao import SqlOrderSummaryDao
from .order.query.application.order_view_list_service import OrderViewListService

# https://github.com/ets-labs/python-dependency-injector/issues/344


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    app = providers.Dependency(instance_of=Flask)
    session = providers.Dependency(instance_of=scoped_session)
    category_repository = providers.Factory(
        SqlCategoryRepository, session=session)
    product_repository = providers.Factory(
        SqlProductRepository, session=session)
    order_summary_dao = providers.Factory(SqlOrderSummaryDao, session=session)
    order_view_list_service = providers.Factory(
        OrderViewListService, order_summary_dao=order_summary_dao)
