import json

from db import actions


async def get_current_user(session, event):
    user_actions = actions.UserAction(session)
    return await user_actions.get_user_by_name(event.from_user.full_name)


async def change_n_value(session, event, n_value):
    """
    Changes user's N value
    """
    user_actions = actions.UserAction(session)
    if not n_value.isdigit():
        await event.answer('Wrong value type.')  # Do nothing if value has wrong type
        return None

    n_value = int(n_value)

    if not 1 <= n_value <= 10:
        await event.answer("N value should be 1 <= N <= 10")  # Do nothing if value is too high or too low
        return None

    current_user = await get_current_user(session, event)
    n_value_before_changing = current_user.value_n

    await user_actions.update_user(
        user_id=current_user.id,
        value_n=n_value
    )

    await event.answer(f"N value has been changed from {n_value_before_changing} to {n_value}")


def get_decoded_json(json_body) -> dict:
    """
    Decodes json to python dictionary
    """
    decoder = json.decoder.JSONDecoder()
    decoded_json = decoder.decode(json_body)
    return decoded_json


def dict_to_string(entry_dict) -> str:
    result = '\n\n'.join(f'{key}:\n{entry_dict[key]}' for key in entry_dict)
    return result
