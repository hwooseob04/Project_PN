# 학습 경로 테이블을 control

from .connection import get_connection, close_connection

def create_path(title: str, description: str = None, purpose: str = None
                ,method: str = None, order_index: int = 0) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO learning_paths (title, description, purpose, method, order_index)
        VALUES (?,?,?,?,?)
""", (title, description, purpose, method, method, order_index)
)
    conn.commit()
    # 삽입된 새로운 행의 id 반환
    new_id = cur.lastrowid
    close_connection(conn)

    return new_id

def get_path_by_id(path_id: int) -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * from learning_paths WHERE id = ?", path_id)
    row = cur.fetchone()
    close_connection(conn)
    return dict(row) if row else None

def list_paths(limit: int = 100) -> list:

    return 
def update_path(path_id: int, title: str = None, description: str = None,
                purpose: str = None, method: str = None, order_index: int = None) -> bool:
    conn = get_connection()
    fields, params = [], []
    if title is not None:
        fields.append("title = ?"); params.append(title)
    # …같은 방식으로 description/purpose/method/order_index 처리…
    params.append(path_id)
    sql = f"UPDATE learning_paths SET {', '.join(fields)} WHERE id = ?"
    cur = conn.execute(sql, params)
    conn.commit()
    updated = cur.rowcount > 0
    close_connection(conn)
    return updated    
    return 

def delete_path(path_id: int) -> bool:
    conn = get_connection()
    cur = conn.execute("DELETE FROM learning_paths WHERE id = ?", (path_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    close_connection(conn)
    return deleted
