import json
import logging
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for field in ("method", "path", "status_code", "user_id, field_count, error_count, doc_id, payload_keys"):
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def configure_logging():
    root_logger = logging.getLogger()

    if root_logger.handlers:
        root_logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)