
import contextvars

_current_user_id: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "current_user_id",
    default=None,
)


def set_current_actor(user_id: str) -> contextvars.Token:
    return _current_user_id.set(user_id)


def reset_current_actor(token: contextvars.Token) -> None:
    _current_user_id.reset(token)


def get_current_actor() -> str:
    user_id = _current_user_id.get()
    if user_id is None:
        return "system"
    return str(user_id)
