import uuid


def new_session_id(name: str) -> str:
    return f"{name}#{uuid.uuid4().hex[:8]}"
