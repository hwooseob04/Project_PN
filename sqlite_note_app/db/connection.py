# python 3.6 이상에선 바로 실행 가능능
import sqlite3
from pathlib import Path

#connection.py의 차상위 = /sqlite_note_app
BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / 'project.db'


def get_connection():
    conn = sqlite3.connect(str(DB_PATH),
                           detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def close_connection(conn):
    """주어진 Connection 객체를 닫습니다."""
    if conn:
        conn.close()
        
if __name__ == '__main__':
    # 간단 테스트: 테이블 목록 출력
    conn = get_connection()
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row['name'] for row in cur.fetchall()]
    print("Connected to:", DB_PATH)
    print("Tables:", tables)
    close_connection(conn)
