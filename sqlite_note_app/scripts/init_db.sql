-- scripts/init_db.sql
DROP TABLE IF EXISTS note_topic_links;
DROP TABLE IF EXISTS learning_paths;
DROP TABLE IF EXISTS notes;
-- 1) 일간 노트 테이블
CREATE TABLE IF NOT EXISTS notes (
  id             INTEGER   PRIMARY KEY AUTOINCREMENT,
  date           DATE      NOT NULL UNIQUE,
  title          TEXT,
  content        TEXT      NOT NULL,
  prev_note_id   INTEGER   REFERENCES notes(id),
  created_at     DATETIME  DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME  DEFAULT CURRENT_TIMESTAMP
);

-- 2) 학습 경로 테이블
CREATE TABLE IF NOT EXISTS learning_paths (
  id            INTEGER   PRIMARY KEY AUTOINCREMENT,
  title         TEXT      NOT NULL,
  description   TEXT,
  purpose       TEXT,
  method        TEXT,
  order_index   INTEGER   NOT NULL,
  created_at    DATETIME  DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME  DEFAULT CURRENT_TIMESTAMP
);

-- 3) 노트-토픽 연결 테이블
CREATE TABLE IF NOT EXISTS note_topic_links (
  note_id       INTEGER   NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  path_id       INTEGER   NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
  PRIMARY KEY (note_id, path_id)
);
