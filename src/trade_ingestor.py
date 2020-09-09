import websocket
import boto3
import json
import structlog

log = structlog.get_logger()


class TradeIngestor:
    """ Ingest trades from finnhub into Kinesis.
    Kinesis and websocket interactions confined to run to make testing easier.
    """
    def __init__(self, stream_name: str, finnhub_token: str, symbols: [str] = []):
        self.stream_name = stream_name
        self.finnhub_token = finnhub_token
        self.symbols = symbols

    def transform(self, raw_msg: str) -> []:
        """ Transform into a Kinesis stream message
        """

        rows = []
        if raw_msg is None or raw_msg == "":
            return rows

        try:
            message = json.loads(raw_msg)
            if message.get("type") == "ping":
                log.info("on_message pinged")
            elif message.get("type") == "trade":
                data = message.get('data')
                if data:
                    for row in data:
                        rows.append({
                            "Data": json.dumps(row),
                            "PartitionKey": row.get('s')
                        })
                    log.info("transformed", rows=rows)
            else:
                log.info("on_message unknown type", data=message)
        except json.JSONDecodeError:
            log.exception("Unable to json decode", raw_msg=raw_msg)

        return rows

    def get_subscriptions(self) -> []:
        return [json.dumps({"type": "subscribe", "symbol": symbol}) for symbol in self.symbols]

    def run(self):
        """ Runs process loop to receive messages from socket.
        """

        if len(self.symbols) == 0:
            log.info("No symbols to run exiting")
            return

        session = boto3.Session()
        kinesis = session.client("kinesis")

        def on_message(ws, msg):
            log.info("on_message", raw_msg=msg)
            rows = self.transform(msg)
            if len(rows) > 0:
                kinesis.put_records(StreamName=self.stream_name, Records=rows)

        def on_error(ws, error):
            log.exception("on_error", error=error)

        def on_close(ws):
            log.info("closing websocket")

        def on_open(ws):
            for sub in self.get_subscriptions():
                ws.send(sub)

        log.info("opening websocket")
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://ws.finnhub.io?token={0}".format(self.finnhub_token),
                                          on_message=on_message,
                                          on_error=on_error,
                                          on_close=on_close,
                                          on_open=on_open)
        ws.run_forever()



