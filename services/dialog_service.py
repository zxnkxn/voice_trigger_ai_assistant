from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from db.models import DialogMessage

DIALOG_TTL = timedelta(minutes=10)

# Maximum number of messages to keep in conversation history
MAX_HISTORY_MESSAGES = 8


def get_dialog_history(db: Session, toy_id: str) -> list[DialogMessage]:
    last_msg = (
        db.query(DialogMessage)
        .filter(DialogMessage.toy_id == toy_id)
        .order_by(DialogMessage.created_at.desc())
        .first()
    )

    if not last_msg:
        return []

    if datetime.now(timezone.utc) - last_msg.created_at > DIALOG_TTL:
        db.query(DialogMessage).filter(DialogMessage.toy_id == toy_id).delete()
        db.commit()
        return []

    return (
        db.query(DialogMessage)
        .filter(DialogMessage.toy_id == toy_id)
        .order_by(DialogMessage.created_at)
        .all()
    )


def save_message(db: Session, toy_id: str, role: str, text: str):
    msg = DialogMessage(
        toy_id=toy_id,
        role=role,
        text=text,
    )
    db.add(msg)
    db.commit()
    print(f"Saved to DB: id={msg.id}, role={msg.role}, text={msg.text}")

    # Trim history to keep only the last MAX_HISTORY_MESSAGES messages
    messages = (
        db.query(DialogMessage)
        .filter(DialogMessage.toy_id == toy_id)
        .order_by(DialogMessage.created_at.desc())
        .all()
    )

    if len(messages) > MAX_HISTORY_MESSAGES:
        messages_to_delete = messages[MAX_HISTORY_MESSAGES:]
        for m in messages_to_delete:
            db.delete(m)
        db.commit()
