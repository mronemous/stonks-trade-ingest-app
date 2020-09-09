from trade_ingestor import TradeIngestor
import structlog
from decouple import config

log = structlog.get_logger()


def main():

    symbols: [str] = ["AAPL", "AMZN", "TSLA"]

    ingestor = TradeIngestor(stream_name=config("KINESIS_STREAM"),
                             finnhub_token=config("FINNHUB_TOKEN"),
                             symbols=symbols)
    ingestor.run()


if __name__ == "__main__":
    main()
