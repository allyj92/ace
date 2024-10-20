import streamlit as st
import requests

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

# 마이페이지 UI
st.title("마이페이지")
st.header("나의 정보 수정")

with st.form(key='update_info_form'):
    if st.session_state['logged_in']:
        # 서버에서 사용자 정보를 가져옴
        response = requests.get(f"{API_BASE_URL}/user/{st.session_state['username']}")
        if response.status_code == 200:
            user_data = response.json()
            st.session_state['username'] = user_data['username']
            st.session_state['email'] = user_data['email']
            st.session_state['phoneNumber'] = user_data['phone_number']
        new_email = st.text_input("이메일", value=st.session_state.get('email', ''))
        new_phone_number = st.text_input("전화번호", value=st.session_state.get('phoneNumber', ''))
    else:
        new_email = st.text_input("이메일", value='')
        new_phone_number = st.text_input("전화번호", value='')

    if st.form_submit_button("정보 수정"):
        st.write(f'{new_email}, {new_phone_number}')
        if st.session_state['logged_in']:
            url = f"{API_BASE_URL}/user/{st.session_state['username']}/update"
            data = {"email": new_email, "phoneNumber": new_phone_number}  # 필드명을 서버에 맞춤

            # 서버로 PUT 요청을 전송
            response = requests.put(url, json=data)

            # 서버 응답이 성공적이면 세션 상태를 업데이트
            if response and response.status_code == 200:
                st.session_state['email'] = new_email
                st.session_state['phoneNumber'] = new_phone_number  # 세션에서 phoneNumber로 수정

                # 디버깅용 세션 상태 출력
                st.write("세션 상태 디버깅 (업데이트 후):", st.session_state)
                st.success("정보가 성공적으로 수정되었습니다!")
            else:
                st.error(f"정보 수정에 실패했습니다. 상태 코드: {response.status_code}, 응답 내용: {response.text}")
                st.write("세션 상태 디버깅 (수정 실패):", st.session_state)
        else:
            st.error("로그인이 필요합니다.")

# 로그인 페이지 UI
st.title("로그인")
if not st.session_state['logged_in']:
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        login_data = {"username": username, "password": password}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)

        if response.status_code == 200:
            st.success("로그인 성공!")
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            # 로그인 후 사용자 정보를 다시 가져옴
            response = requests.get(f"{API_BASE_URL}/user/{st.session_state['username']}")
            if response.status_code == 200:
                user_data = response.json()
                st.session_state['email'] = user_data['email']
                st.session_state['phoneNumber'] = user_data['phone_number']
        else:
            st.error("로그인 실패: 아이디 또는 비밀번호를 확인하세요.")