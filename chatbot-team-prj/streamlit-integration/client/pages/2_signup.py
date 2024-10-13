import streamlit as st

def signup_page():
    st.title("회원가입")

    st.write("회원가입을 하시면 맞춤형 제품 추천을 더 빠르게 받을 수 있어요!")

    # 회원가입 폼 UI
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    confirm_password = st.text_input("비밀번호 확인", type="password")
    email = st.text_input("이메일")
    phone_number = st.text_input("전화번호")


    # 회원가입 버튼
    if st.button("회원가입"):
        if password == confirm_password:
            st.success(f"회원가입 성공! 환영합니다, {username}님!")
        else:
            st.error("비밀번호가 일치하지 않습니다.")

# 회원가입 페이지를 호출
signup_page()
