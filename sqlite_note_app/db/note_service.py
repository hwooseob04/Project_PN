# db/note_service.py
from datetime import datetime
from .connection import get_connection, close_connection

def create_note(date: str, title: str, content: str, prev_note_id: int = None) -> int:
    """
    새 노트를 삽입하고, 생성된 note.id를 반환합니다.
    date: 'YYYY-MM-DD' 형식 문자열
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO notes (date, title, content, prev_note_id)
        VALUES (?, ?, ?, ?)
        """,
        (date, title, content, prev_note_id)
    )
    conn.commit()
    new_id = cur.lastrowid
    close_connection(conn)
    return new_id

def get_note_by_id(note_id: int) -> dict:
    """ID로 노트 하나를 조회해 dict로 반환합니다."""
    conn = get_connection()
    cur = conn.execute(
        "SELECT * FROM notes WHERE id = ?", (note_id,)
    )
    row = cur.fetchone()
    close_connection(conn)
    return dict(row) if row else None

def get_note_by_date(date: str) -> dict:
    """날짜로 노트 하나를 조회해 dict로 반환합니다."""
    conn = get_connection()
    cur = conn.execute(
        "SELECT * FROM notes WHERE date = ?", (date,)
    )
    row = cur.fetchone()
    close_connection(conn)
    return dict(row) if row else None

def list_notes(limit: int = 100) -> list:
    """최근 notes를 date 내림차순으로 최대 limit개 조회."""
    conn = get_connection()
    cur = conn.execute(
        "SELECT * FROM notes ORDER BY date DESC LIMIT ?", (limit,)
    )
    rows = cur.fetchall()
    close_connection(conn)
    return [dict(r) for r in rows]

def update_note(note_id: int, title: str = None, content: str = None) -> bool:
    """
    노트의 제목 또는 내용을 업데이트합니다.
    변경된 행(row)이 있으면 True, 없으면 False 반환.
    """
    conn = get_connection()
    fields = []
    params = []
    if title is not None:
        fields.append("title = ?")
        params.append(title)
    if content is not None:
        fields.append("content = ?")
        params.append(content)
    params.append(note_id)
    sql = f"UPDATE notes SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
    cur = conn.execute(sql, params)
    conn.commit()
    updated = cur.rowcount > 0
    close_connection(conn)
    return updated

def delete_note(note_id: int) -> bool:
    """
    note_id에 해당하는 노트를 삭제합니다.
    삭제된 행이 있으면 True, 없으면 False를 반환합니다.
    """
    conn = get_connection()
    cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    close_connection(conn)
    return deleted

if __name__ == "__main__":
    # 간단 테스트
    nid = create_note("2025-07-02", "테스트 노트", "내용입니다.", None)
    print("Created Note ID:", nid)
    note = get_note_by_id(nid)
    print("Fetched:", note)
    update_note(nid, content=note["content"] + "\n추가된 줄")
    print("After update:", get_note_by_id(nid))
    print("All notes:", list_notes(5))
    delete_note(nid)
    print("Deleted? Now fetch:", get_note_by_id(nid))
