from trade_ingestor import TradeIngestor


def get_trade_ingestor() -> TradeIngestor:
    return TradeIngestor(stream_name="",
                     finnhub_token="",
                     symbols=["AAPL", "AMZN", "TSLA"])

def test_transform_ping():
    ingestor = get_trade_ingestor()
    assert ingestor.transform('{"type":"ping"}') == []

def test_transform_one_trade():
    ingestor = get_trade_ingestor()
    assert ingestor.transform('{"data":[{"p":354.9084,"s":"TSLA","t":1599676370725,"v":100}],"type":"trade"}') == [
        {"Data": '{"p": 354.9084, "s": "TSLA", "t": 1599676370725, "v": 100}', "PartitionKey": "TSLA"}
    ]

def test_transform_trade_multiple():
    ingestor = get_trade_ingestor()
    assert ingestor.transform('{"data":[{"p":354.9084,"s":"TSLA","t":1599676370725,"v":100}, {"p":354.8084,"s":"TSLA","t":1599676370725,"v":10}],"type":"trade"}') == [
        {"Data": '{"p": 354.9084, "s": "TSLA", "t": 1599676370725, "v": 100}', "PartitionKey": "TSLA"},
        {"Data": '{"p": 354.8084, "s": "TSLA", "t": 1599676370725, "v": 10}', "PartitionKey": "TSLA"}
    ]

def test_transform_trade_no_data():
    ingestor = get_trade_ingestor()
    assert ingestor.transform(
        '{"data":[],"type":"trade"}') == []

def test_transform_unknown():
    ingestor = get_trade_ingestor()
    assert ingestor.transform(
        '{"data":[],"type":"unknown_action"}') == []

def test_transform_no_type():
    ingestor = get_trade_ingestor()
    assert ingestor.transform('{}') == []

def test_transform_blank_message():
    ingestor = get_trade_ingestor()
    assert ingestor.transform('') == []

def test_transform_no_message():
    ingestor = get_trade_ingestor()
    assert ingestor.transform(None) == []

def test_transform_bad_json():
    ingestor = get_trade_ingestor()
    assert ingestor.transform('{') == []

def test_get_subscriptions_no_symbols():
    ingestor = get_trade_ingestor()
    ingestor.symbols = []
    assert ingestor.get_subscriptions() == []