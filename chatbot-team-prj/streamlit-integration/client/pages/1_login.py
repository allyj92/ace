import streamlit as st
import requests
from streamlit_cookies_manager import EncryptedCookieManager

# 쿠키 매니저 초기화
cookies = EncryptedCookieManager(
    prefix="myapp",  # 애플리케이션 고유의 쿠키 이름
    password="3511"  # 쿠키 암호화에 사용할 비밀번호
)


# 만약 쿠키를 사용할 수 없으면 경고
if not cookies.ready():
    st.stop()

# 로그인 상태 확인 및 세션 상태 초기화
if 'logged_in' not in st.session_state:
    if cookies.get('logged_in') == 'true':
        st.session_state['logged_in'] = True
        st.session_state['username'] = cookies.get('username', '')
    else:
        st.session_state['logged_in'] = False


# 홈 페이지 함수
def home_page():
    st.title("로그인")
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
    st.write(f"로그인에 성공했습니다, {st.session_state['username']}님 반갑습니다.")

    # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state['logged_in'] = False  # 로그인 상태 해제
        st.session_state['username'] = ''  # 세션 상태 초기화
        cookies['logged_in'] = 'false'  # 쿠키에서 로그인 상태 해제
        cookies.save()  # 쿠키 저장
        st.session_state['current_page'] = 'login'  # 로그인 페이지로 이동
#         st.experimental_rerun()  # 페이지 새로고침

# 로그인 페이지 함수
def login_page():
    st.title("로그인")
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

    # 로그인 입력 필드
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        # POST 요청으로 로그인 데이터 전송
        login_data = {"username": username, "password": password}
        response = requests.post("http://localhost:8080/auth/login", json=login_data)

        if response.status_code == 200:
            st.session_state['logged_in'] = True  # 로그인 상태 저장
            st.session_state['username'] = username  # 유저네임 저장
            cookies['logged_in'] = 'true'  # 쿠키에 로그인 상태 저장
            cookies['username'] = username  # 쿠키에 유저명 저장
            cookies.save()  # 쿠키 저장
            st.success("로그인 성공!")
            st.session_state['current_page'] = 'home'  # 로그인 성공 후 홈 페이지로 이동
#
        else:
            st.session_state['logged_in'] = False 
            st.error(f"로그인 실패: {response.text}")  # 서버 응답 메시지 출력

# 초기 세션 상태 설정
if 'logged_in' not in st.session_state:
    if cookies.get('logged_in') == 'true':
        st.session_state['logged_in'] = True
        st.session_state['username'] = cookies.get('username', '')
    else:
        st.session_state['logged_in'] = False

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'  # 기본 페이지는 로그인

# 페이지 라우팅
if st.session_state['current_page'] == 'home' and st.session_state['logged_in']:
    home_page()  # 로그인 상태면 홈 페이지로 이동
else:
    login_page()  # 로그인이 안 되어있으면 로그인 페이지로 이동
