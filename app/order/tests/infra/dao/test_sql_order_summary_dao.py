

def test_select_by_orderer(sql_order_summary_dao):
    order_summaries = sql_order_summary_dao.select_by_orderer(1)
    assert len(order_summaries) == 2
    summary = order_summaries[0]

    assert summary.order_id == 1
    assert summary.orderer_id == 1
    assert summary.orderer_username == '사용자1'
    assert summary.product_id == 1
    assert summary.product_name == '라즈베리파이3 모델B'
    assert summary.total_amounts == 4000

def test_count_by_filter(sql_order_summary_dao):
    assert sql_order_summary_dao.counts(None) == 3
    assert sql_order_summary_dao.counts({'orderer_id': 1}) ==  2
    assert sql_order_summary_dao.counts({'orderer_id': 2}) ==  1