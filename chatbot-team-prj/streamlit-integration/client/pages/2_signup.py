import streamlit as st
import requests

def signup_page():
    st.title("회원가입")
    st.markdown(
            """
            <style>
            .underline {
                border-bottom: 2px solid #e3e3e3;  /* 밑줄 스타일 (검정색, 두께 2px) */
                padding-bottom: 10px;  /* 제목과 밑줄 사이 간격 */
                margin-bottom: 20px;  /* 밑줄과 콘텐츠 사이 간격 */
            }
            </style>
            <div class="underline"> </div>
            """,
            unsafe_allow_html=True
        )

    st.write("회원가입을 하시면 맞춤형 제품 추천을 더 빠르게 받을 수 있어요!")

    # 회원가입 폼 UI
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    confirm_password = st.text_input("비밀번호 확인", type="password")
    name = st.text_input("이름")  # 이름 필드 추가
    email = st.text_input("이메일")
    address = st.text_input("주소")  # 주소 필드 추가
    phone_number = st.text_input("전화번호")

    # 회원가입 버튼
    if st.button("회원가입"):
        if password == confirm_password:
            # API로 보낼 데이터
            signup_data = {
                "username": username,
                "password": password,
                "name": name,  # 이름 필드 추가
                "email": email,
                "address": address,  # 주소 필드 추가
                "phoneNumber": phone_number
            }

            # POST 요청 보내기
            response = requests.post("http://localhost:8080/auth/signup", json=signup_data)

            # 응답 처리
            if response.status_code == 200:
                st.success(f"회원가입 성공! 환영합니다, {username}님!")
            else:
                st.error(f"회원가입 실패: {response.text}")
        else:
            st.error("비밀번호가 일치하지 않습니다.")

# 회원가입 페이지 호출
signup_page()
