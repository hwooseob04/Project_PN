from .connection import get_connection, close_connection

def link_note_topic(note_id: int, path_id: int) -> None:
    """
    note_id와 path_id를 연결 테이블에 삽입합니다.
    이미 연결되어 있으면 아무 동작도 하지 않습니다.
    """
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO note_topic_links (note_id, path_id) VALUES (?, ?)",
        (note_id, path_id)
    )
    conn.commit()
    close_connection(conn)

def unlink_note_topic(note_id: int, path_id: int) -> bool:
    """
    연결을 제거합니다. 성공 시 True, 없으면 False를 반환합니다.
    """
    conn = get_connection()
    cur = conn.execute(
        "DELETE FROM note_topic_links WHERE note_id = ? AND path_id = ?",
        (note_id, path_id)
    )
    conn.commit()
    deleted = cur.rowcount > 0
    close_connection(conn)
    return deleted

def list_topics_for_note(note_id: int) -> list[dict]:
    """
    특정 노트에 연결된 토픽들을 order_index 순으로 반환합니다.
    """
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT p.* 
          FROM learning_paths p
          JOIN note_topic_links l ON p.id = l.path_id
         WHERE l.note_id = ?
         ORDER BY p.order_index
        """,
        (note_id,)
    )
    rows = cur.fetchall()
    close_connection(conn)
    return [dict(r) for r in rows]

def list_notes_for_topic(path_id: int) -> list[dict]:
    """
    특정 토픽에 연결된 노트들을 날짜 순으로 반환합니다.
    """
    conn = get_connection()
    cur = conn.execute(
        """
        SELECT n.* 
          FROM notes n
          JOIN note_topic_links l ON n.id = l.note_id
         WHERE l.path_id = ?
         ORDER BY n.date
        """,
        (path_id,)
    )
    rows = cur.fetchall()
    close_connection(conn)
    return [dict(r) for r in rows]

"""
간단한 link_service test
"""
if __name__ == '__main__':
    print(list_topics_for_note)
