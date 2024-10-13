import streamlit as st

def login_page():
    st.title("로그인")

    # 아이디와 비밀번호 입력받는 필드
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    # 로그인 버튼
    if st.button("로그인"):
        # 여기에 로그인 인증 로직을 추가하면 됩니다.
        if username == "admin" and password == "password":  # 예시로 간단한 조건
            st.success("로그인 성공!")
        else:
            st.error("아이디나 비밀번호가 올바르지 않습니다.")

# 로그인 페이지 호출
login_page()