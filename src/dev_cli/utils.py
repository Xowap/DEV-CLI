from logging import DEBUG, ERROR, WARNING, getLogger

import coloredlogs


def setup_logging():
    """
    Setups the log formatting
    """

    coloredlogs.install(
        level=DEBUG, fmt="%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s"
    )

    getLogger("hpack").setLevel(ERROR)
    getLogger("asyncio").setLevel(WARNING)
    getLogger("httpx").setLevel(WARNING)
