# db/continuity_service.py
from datetime import datetime, timedelta
from .note_service import get_note_by_date, create_note

def get_yesterday_summary(date: str, lines: int = 2) -> str:
    dt = datetime.strptime(date, "%Y-%m-%d")
    yesterday = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
    prev = get_note_by_date(yesterday)
    if not prev:
        return ""
    content_lines = prev["content"].splitlines()
    return "\n".join(content_lines[-lines:])

def create_daily_note_with_summary(date: str, title: str, content: str) -> int:
    summary = get_yesterday_summary(date)
    if summary:
        full_content = (
            f"> 어제 요약:\n"
            + "\n".join(f"> {line}" for line in summary.splitlines())
            + f"\n\n{content}"
        )
    else:
        full_content = content

    # 어제 노트 ID 찾기
    yesterday = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    prev_note = get_note_by_date(yesterday)
    prev_id = prev_note["id"] if prev_note else None

    return create_note(date=date, title=title, content=full_content, prev_note_id=prev_id)
