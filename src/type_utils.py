from datetime import datetime
from constants import ISO_DATE_FORMAT


def convert_to_iso8601(epoch_ms: int):
    if not epoch_ms:
        return None
    dt = datetime.fromtimestamp(epoch_ms / 1000.0)

    return datetime.strftime(dt, ISO_DATE_FORMAT)
