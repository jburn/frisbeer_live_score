import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(message)s"
        ),
        handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log"),
        ],
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)