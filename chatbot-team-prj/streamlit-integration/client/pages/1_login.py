import streamlit as st
import requests

def login_page():
    st.title("로그인")



    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        # POST 요청으로 로그인 데이터 전송
        login_data = {"username": username, "password": password}
        response = requests.post("http://localhost:8080/auth/login", json=login_data)

        if response.status_code == 200:
            st.success("로그인 성공!")
            st.experimental_rerun()  # 페이지 새로고침으로 로그인 상태 반영
        else:
            st.error(f"로그인 실패: {response.text}")  # 서버 응답 메시지 출력

# 로그인 페이지 실행
login_page()
