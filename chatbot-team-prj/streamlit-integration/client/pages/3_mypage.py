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

# 세션 상태 디버깅 출력
st.write("세션 상태 디버깅:", st.session_state)

# 서버 URL 설정 (REST API 서버 주소 설정)
API_BASE_URL = "http://localhost:8080"

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # 로그인 상태 초기화

if 'username' not in st.session_state:
    st.session_state['username'] = ''  # 사용자명 초기화
if 'email' not in st.session_state:
    st.session_state['email'] = ''  # 이메일 초기화
if 'phoneNumber' not in st.session_state:
    st.session_state['phoneNumber'] = ''  # 기본값을 빈 문자열로 설정 (user_data 없이)

# 로그인되지 않았으면 로그인 페이지로 이동
if not st.session_state['logged_in']:
    st.title("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        login_data = {"username": username, "password": password}

        # 서버로 로그인 요청
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)

        if response.status_code == 200:
            st.success("로그인 성공!")
            st.session_state['logged_in'] = True
            cookies['logged_in'] = 'true'
            st.session_state['username'] = username
            cookies.save()  # 쿠키 저장
            st.success("로그인 성공!")
            st.session_state['current_page'] = 'home'

            # 로그인 성공 후 사용자 정보를 다시 가져옴
            response = requests.get(f"{API_BASE_URL}/user/{username}")
            if response.status_code == 200:
                user_data = response.json()
                st.session_state['email'] = user_data.get('email', '')
                st.session_state['phoneNumber'] = user_data.get('phone_number', '')
            else:
                st.error(f"사용자 정보를 가져오는 데 실패했습니다: {response.status_code}")
        else:
            st.error("로그인 실패: 아이디 또는 비밀번호를 확인하세요.")
else:
    # 로그인된 경우 마이페이지 UI 표시
    st.title("마이페이지")
    st.markdown(
            """
            <style>
            .underline {
                border-bottom: 2px solid #e3e3e3;  /* 밑줄 스타일 */
                padding-bottom: 10px;
                margin-bottom: 20px;
            }
            </style>
            <div class="underline"> </div>
            """,
            unsafe_allow_html=True
        )
    st.header("나의 정보 수정")

    # 서버에서 사용자 정보를 가져옴 (로그인한 경우)
    response = requests.get(f"{API_BASE_URL}/user/{st.session_state['username']}")
    if response.status_code == 200:
        user_data = response.json()
        st.session_state['email'] = user_data.get('email', '')
        st.session_state['phoneNumber'] = user_data.get('phone_number', '')
    else:
        st.error(f"사용자 정보를 가져오는 데 실패했습니다: {response.status_code}")

    with st.form(key='update_info_form'):
        new_email = st.text_input("이메일", value=st.session_state['email'])
        new_phone_number = st.text_input("전화번호", value=st.session_state['phoneNumber'])

        if st.form_submit_button("정보 수정"):
            url = f"{API_BASE_URL}/user/{st.session_state['username']}/update"
            data = {"email": new_email, "phoneNumber": new_phone_number}

            # 서버로 PUT 요청을 전송
            response = requests.put(url, json=data)

            if response.status_code == 200:
                st.session_state['email'] = new_email
                st.session_state['phoneNumber'] = new_phone_number
                st.success("정보가 성공적으로 수정되었습니다!")
            else:
                st.error(f"정보 수정에 실패했습니다: {response.status_code} - {response.text}")
