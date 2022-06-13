from actions_logging.logging import SQLiteLogger
from db.db_managers import SourceManager, UserManager


async def get_current_user(session, event):
    return await UserManager.get_user_by_name(session, event.from_user.full_name)


async def change_n_value(session, event, n_value):
    """
    Changes user's N value
    """
    if not n_value.isdigit():
        await event.answer('Wrong value type.')  # Do nothing if value has wrong type
        return None

    n_value = int(n_value)

    if not 1 <= n_value <= 10:
        # Do nothing if value is too high or too low
        await event.answer("N value should be 1 <= N <= 10")
        return None

    current_user = await get_current_user(session, event)
    n_value_before_changing = current_user.value_n

    await UserManager.update_user(
        session,
        user_id=current_user.id,
        value_n=n_value
    )

    await event.answer(f"N value has been changed from {n_value_before_changing} to {n_value}")
    await SQLiteLogger.log_action(
        session,
        action_type=f'change N value from {n_value_before_changing} to {n_value}',
        user_id=current_user.id
    )


async def get_source_by_name(session, source_name):
    source = await SourceManager.get_source_by_name(session, name=source_name)
    return source


async def set_user_source(event, session, source):
    """
    Sets user's preferable source to retrieve news from
    """
    current_user = await get_current_user(session, event)
    await UserManager.update_user(
        session=session,
        user_id=current_user.id,
        selected_news_source=source.id
    )
    await event.answer(f"News source has been set to {source.name}")


async def get_all_sources(session):
    sources = await SourceManager.get_all_sources(session)
    return sources


async def get_user_source(session, user):
    source = await SourceManager.get_source_by_id(session, user.selected_news_source)
    return source


async def add_new_user(session, event):
    await UserManager.create_user(
        session,
        name=event.from_user.full_name
    )
