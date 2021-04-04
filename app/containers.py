from dependency_injector import containers, providers

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .order.infra.dao.sql_order_summary_dao import SqlOrderSummaryDao
from .order.query.application.order_view_list_service import OrderViewListService

# https://github.com/ets-labs/python-dependency-injector/issues/344


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    app = providers.Dependency(instance_of=Flask)
    db = providers.Dependency(instance_of=SQLAlchemy)
    order_summary_dao = providers.Factory(SqlOrderSummaryDao, db=db)
    order_view_list_service = providers.Factory(
        OrderViewListService, order_summary_dao=order_summary_dao)
