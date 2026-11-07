from anyio import from_thread

from config.redis import get_redis_client

_emails = set()


def contains(email: str):
    from_thread.run(update_emails)
    return email in _emails


async def update_emails():
    global _emails
    redis = get_redis_client()
    raw_emails = await redis.smembers("emails")
    _emails = {e.decode("utf-8") if isinstance(e, bytes) else e for e in raw_emails}
    print("Fetched emails from Redis: " + ', '.join(_emails))


def add(email: str):
    from_thread.run(_add_to_cache, email)


async def _add_to_cache(email: str):
    _emails.add(email)
    redis = get_redis_client()
    await redis.sadd("emails", email)
    print("Added email to Redis: " + email)


def change(old_email: str, new_email: str):
    from_thread.run(_change_in_cache, old_email, new_email)


async def _change_in_cache(old_email: str, new_email: str):
    _emails.discard(old_email)
    _emails.add(new_email)
    redis = get_redis_client()
    await redis.srem("emails", old_email)
    await redis.sadd("emails", new_email)
    print("Removed email from Redis: " + old_email)
    print("Added email to Redis: " + new_email)
