from argparse import ArgumentParser, Namespace
from logging import getLogger
from os import getenv
from typing import Optional, Sequence, Text

from dotenv import find_dotenv, load_dotenv

from .api import DevApi
from .errors import DevCliError
from .parser import DevParser
from .utils import setup_logging

ALLOWED_KEYS = {"cover_image", "canonical_url", "title"}
API_KEY_ENV = "DEV_API_KEY"


logger = getLogger("dev-cli")


def parse_args(
    argv: Optional[Sequence[Text]] = None, print_help: bool = False
) -> Namespace:
    """
    Parses CLI arguments
    """

    def validate_key(key):
        if key not in ALLOWED_KEYS:
            raise ValueError(
                f'"{key}" is not a valid key. The API key is expected to '
                f"come from an environment variable, see -h output."
            )

        return key

    parser = ArgumentParser(
        description=(
            "A CLI interface to the dev.to API. The API key is expected to "
            f"be found in the {API_KEY_ENV} environment variable."
        )
    )

    sp = parser.add_subparsers(help="What action do you want to do?", dest="action")

    publish_parser = sp.add_parser("publish")
    publish_parser.add_argument("file", help="Markdown file that is the article")
    publish_parser.add_argument(
        "-k",
        "--key",
        help=(
            "Field to use as key. Choices: `cover_image`, `canonical_url` "
            "or `title`. Defaults to `canonical_url`."
        ),
        default="canonical_url",
        type=validate_key,
    )

    if print_help:
        parser.print_help()
        exit(1)

    return parser.parse_args(argv)


def publish(args: Namespace) -> None:
    """
    Executes the "publish" action, which detects if an article already exists
    or if it should be updated.
    """

    logger.info("Hello! ✨ Let's take care of that article!")

    parser = DevParser(args.file)
    key = parser.get_key(args.key)

    api_key = getenv(API_KEY_ENV)

    if not api_key:
        raise DevCliError(
            f"Could not find any API key in {API_KEY_ENV} environment "
            f"variable, is it set?"
        )

    api = DevApi(api_key)
    article = api.find_article(key)

    if article:
        logger.info("Found the article, updating")
        api.update_article(parser, article["id"])
    else:
        logger.info("Article not found, creating a new article")
        api.create_article(parser)

    logger.info("Done! 🥂")


def main(argv: Optional[Sequence[Text]] = None) -> None:
    """
    Parses the arguments and executes the action accordingly
    """

    args = parse_args(argv)

    if args.action == "publish":
        return publish(args)
    else:
        parse_args(argv, print_help=True)


if __name__ == "__main__":
    # noinspection PyBroadException
    try:
        setup_logging()
        load_dotenv(find_dotenv(usecwd=True))
        main()
    except DevCliError as e:
        logger.error(f"Error: {e}")
    except KeyboardInterrupt:
        logger.info("Quitting due to user signal")
    except SystemExit:
        pass
    except BaseException:
        logger.exception("Unknown error")
