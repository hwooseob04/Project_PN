import streamlit as st
from datetime import datetime

from sqlite_note_app.db import note_service, connection
import sqlite3

from pathlib import Path



# app.py 위치(Path) → 상위 폴더(Path)
base_dir = Path(__file__).parent

# scripts/init_db.sql 경로(Path)
sql_file = base_dir / 'sqlite_note_app' / 'scripts' / 'init_db.sql'

def init_db():
    """데이터베이스를 초기화합니다."""
    try:
        conn = connection.get_connection()
        cursor = conn.cursor()
        
        # init_db.sql 파일 읽기
        with sql_file.open('r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()
        st.success("데이터베이스가 성공적으로 초기화되었습니다!")
        
    except sqlite3.Error as e:
        st.error(f"데이터베이스 초기화 중 오류 발생: {e}")
    finally:
        if conn:
            connection.close_connection(conn)


if not (Path(__file__).parent / 'project.db').exists():
    init_db()
    
def main():
    """Streamlit 애플리케이션의 메인 함수"""
    st.set_page_config(page_title="My Note App", layout="wide")
    st.title("📝 나의 노트 앱 (MVP)")

    # --- 사이드바 ---
    st.sidebar.title("메뉴")
    
    if st.sidebar.button("데이터베이스 초기화"):
        st.write("DB 초기화 스크립트 경로:", sql_file)
        init_db()
        st.rerun()

    menu = st.sidebar.radio(
        "작업을 선택하세요",
        ("노트 목록 보기", "새 노트 작성", "노트 검색 및 수정/삭제")
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("이 앱은 SQLite 데이터베이스를 사용하는 간단한 노트 관리 시스템입니다.")

    # --- 메인 화면 ---
    if menu == "노트 목록 보기":
        st.subheader("📓 전체 노트 목록")
        try:
            notes = note_service.list_notes(limit=1000)
            if notes:
                # Pandas를 사용하지 않고 노트 목록 표시
                for note in notes:
                    with st.expander(f"{note['date']} - {note['title']} (ID: {note['id']})"):
                        st.markdown(f"**ID:** {note['id']}")
                        st.markdown(f"**날짜:** {note['date']}")
                        st.markdown(f"**제목:** {note['title']}")
                        st.markdown(f"**생성일:** {note['created_at']}")
                        st.markdown(f"**수정일:** {note['updated_at']}")
                        st.markdown("---")
                        st.markdown(note['content'])
            else:
                st.info("작성된 노트가 없습니다. '새 노트 작성' 메뉴에서 노트를 추가해보세요.")
        except Exception as e:
            st.error(f"노트를 불러오는 중 오류가 발생했습니다: {e}")

    elif menu == "새 노트 작성":
        st.subheader("✍️ 새 노트 작성")
        with st.form("new_note_form"):
            date = st.date_input("날짜", datetime.now())
            title = st.text_input("제목")
            content = st.text_area("내용", height=300)
            
            submitted = st.form_submit_button("저장")
            
            if submitted:
                if not title:
                    st.warning("제목을 입력해주세요.")
                else:
                    try:
                        note_service.create_note(date.strftime('%Y-%m-%d'), title, content)
                        st.success("새 노트가 성공적으로 저장되었습니다!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"노트 저장 중 오류 발생: {e}")

    elif menu == "노트 검색 및 수정/삭제":
        st.subheader("🔍 노트 검색 및 관리")
        try:
            all_notes = note_service.list_notes(limit=1000)
            if not all_notes:
                st.warning("관리할 노트가 없습니다.")
                return

            # 사용자가 노트를 쉽게 찾을 수 있도록 제목으로 검색 기능 제공
            note_titles = {f"{note['id']}: {note['title']} ({note['date']})": note['id'] for note in all_notes}
            selected_key = st.selectbox("관리할 노트를 선택하세요", note_titles.keys())

            if selected_key:
                note_id = note_titles[selected_key]
                note = note_service.get_note_by_id(note_id)

                if note:
                    st.markdown("---")
                    st.markdown(f"### '{note['title']}' 노트 수정")

                    with st.form("edit_note_form"):
                        new_title = st.text_input("제목", value=note['title'])
                        new_content = st.text_area("내용", value=note['content'], height=300)
                        
                        # 수정과 삭제 버튼을 나란히 배치
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            update_button = st.form_submit_button("수정하기")
                        with col2:
                            delete_button = st.form_submit_button("삭제하기")

                        if update_button:
                            note_service.update_note(note_id, title=new_title, content=new_content)
                            st.success(f"노트(ID: {note_id})가 성공적으로 수정되었습니다.")
                            st.rerun()

                        if delete_button:
                            # 삭제 확인 절차 추가
                            st.session_state.delete_confirm = True
                            st.session_state.note_to_delete = note_id
                
                # 삭제 확인 메시지 표시
                if 'delete_confirm' in st.session_state and st.session_state.delete_confirm:
                    note_id_to_delete = st.session_state.note_to_delete
                    st.warning(f"정말로 노트(ID: {note_id_to_delete})를 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.")
                    
                    col1, col2 = st.columns(2)
                    if col1.button("예, 삭제합니다."):
                        note_service.delete_note(note_id_to_delete)
                        st.success(f"노트(ID: {note_id_to_delete})가 삭제되었습니다.")
                        del st.session_state.delete_confirm
                        del st.session_state.note_to_delete
                        st.rerun()
                    if col2.button("아니요"):
                        del st.session_state.delete_confirm
                        del st.session_state.note_to_delete
                        st.rerun()

        except Exception as e:
            st.error(f"노트 관리 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
