import db.actions
from db.config import async_session
from utils import get_current_user


async def log_action(action_type: str, user_id: int = None, event=None, used_news_source: int = None):
    async with async_session() as session:

        if not user_id and not event:
            raise UserWarning

        logging_actions = db.actions.ActionDoings(session)

        if event:
            user = await get_current_user(session, event)
            user_id = user.id

        await logging_actions.create_action(
            action_type=action_type,
            user_id=user_id,
            used_news_source=used_news_source
        )
