import logging

from django.conf import settings

try:
    import tweepy
except Exception:  # pragma: no cover - optional dependency at runtime
    tweepy = None

logger = logging.getLogger(__name__)


def _is_enabled() -> bool:
    return bool(getattr(settings, 'X_TWEETS_ENABLED', False))


def _has_credentials() -> bool:
    required = (
        getattr(settings, 'X_API_KEY', ''),
        getattr(settings, 'X_API_SECRET', ''),
        getattr(settings, 'X_ACCESS_TOKEN', ''),
        getattr(settings, 'X_ACCESS_TOKEN_SECRET', ''),
    )
    return all(required)


def _truncate(text: str, max_len: int = 280) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + '…'


def _client():
    if tweepy is None:
        raise RuntimeError('tweepy is not installed')
    return tweepy.Client(
        consumer_key=settings.X_API_KEY,
        consumer_secret=settings.X_API_SECRET,
        access_token=settings.X_ACCESS_TOKEN,
        access_token_secret=settings.X_ACCESS_TOKEN_SECRET,
    )


def send_tweet(text: str) -> None:
    if not _is_enabled():
        logger.info('X tweet skipped: X_TWEETS_ENABLED is false')
        return
    if not _has_credentials():
        logger.warning('X tweet skipped: missing credentials')
        return
    try:
        client = _client()
        client.create_tweet(text=_truncate(text))
    except Exception as exc:  # pragma: no cover
        logger.exception('X tweet failed: %s', exc)


def tweet_new_store(store) -> None:
    description = (store.store_description or '').strip()
    message = f"New store: {store.store_name}"
    if description:
        message = f"{message} — {description}"
    send_tweet(message)


def tweet_new_product(product) -> None:
    store_name = getattr(product.store, 'store_name', 'Store')
    description = (product.description or '').strip()
    message = f"New product at {store_name}: {product.name}"
    if description:
        message = f"{message} — {description}"
    send_tweet(message)
