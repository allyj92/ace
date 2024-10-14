import streamlit as st
import requests

# 서버 URL 설정 (REST API 서버 주소 설정)
API_BASE_URL = "http://localhost:8080"

# 세션 상태 초기화
if 'wishlist' not in st.session_state:
    st.session_state['wishlist'] = []  # 찜한 상품 목록을 서버에서 가져옴
if 'username' not in st.session_state:
    st.session_state['username'] = ''  # 사용자명 초기화
if 'email' not in st.session_state:
    st.session_state['email'] = ''  # 이메일 초기화
if 'phone_number' not in st.session_state:
    st.session_state['phone_number'] = '0'  # 전화번호 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # 로그인 상태 초기화

# 서버에서 사용자 정보와 찜한 상품 목록을 가져오는 함수
def load_user_data():
    response = requests.get(f"{API_BASE_URL}/user/{st.session_state['username']}")
    if response.status_code == 200:
        user_data = response.json()  # 서버로부터 사용자 정보 JSON 형태로 가져옴
        st.session_state['username'] = user_data['username']  # 사용자명 설정
        st.session_state['email'] = user_data['email']  # 이메일 설정
        st.session_state['phone_number'] = user_data['phone_number']  # 전화번호 설정
        st.session_state['wishlist'] = user_data['wishlist']  # 찜한 상품 목록 설정
    else:
        st.error("사용자 정보를 불러오는 데 실패했습니다.")  # API 호출 실패 시 에러 메시지

# 사용자 정보를 서버에 업데이트하는 함수
def update_user_info(email, phone_number):
    payload = {
        "username": st.session_state['username'],  # 로그인된 사용자명 사용
        "email": email,
        "phone_number": phone_number
    }
    response = requests.put(f"{API_BASE_URL}/user/update", json=payload)
    return response.status_code == 200  # 업데이트 성공 여부 반환

# 찜한 상품 목록을 모두 삭제하는 함수
def delete_all_wishlist():
    response = requests.delete(f"{API_BASE_URL}/user/{st.session_state['username']}/wishlist")
    return response.status_code == 200  # 삭제 성공 여부 반환

# 마이페이지 UI
def mypage():
    st.title("마이페이지")  # 페이지 제목 설정

    # 사용자 정보 수정 섹션
    st.header("나의 정보 수정")
    with st.form(key='update_info'):
        new_email = st.text_input("이메일", value=st.session_state['email'])
        new_phone_number = st.text_input("전화번호", value=st.session_state['phone_number'])




        if st.form_submit_button("정보 수정"):
            if update_user_info(new_email, new_phone_number):
                st.session_state['email'] = new_email
                st.session_state['phone_number'] = new_phone_number
                st.success("정보가 성공적으로 수정되었습니다!")  # 성공 메시지 표시
            else:
                st.error("정보 수정에 실패했습니다.")  # 실패 메시지 표시

    # 찜한 상품 목록 섹션
    st.header("찜한 상품 목록")
    if st.session_state['wishlist']:
        for product in st.session_state['wishlist']:
            st.write(f"- {product}")
    else:
        st.write("찜한 상품이 없습니다.")  # 찜한 상품이 없을 때 메시지 표시

    # 찜한 상품 모두 삭제 버튼
    if st.button("찜한 상품 모두 삭제"):
        if delete_all_wishlist():
            st.session_state['wishlist'].clear()  # 찜한 상품 목록 초기화
            st.success("찜한 상품이 모두 삭제되었습니다.")  # 성공 메시지
        else:
            st.error("찜한 상품 삭제에 실패했습니다.")  # 실패 메시지

    # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state.clear()  # 세션 상태 초기화
        st.session_state['logged_in'] = False  # 로그인 상태 해제
        st.experimental_rerun()  # 페이지 새로고침으로 로그아웃 처리

# 로그인 페이지 UI
def login_page():
    st.title("로그인")  # 로그인 페이지 제목 설정

    if not st.session_state['logged_in']:
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        if st.button("로그인"):
            login_data = {"username": username, "password": password}
            response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)

            if response.status_code == 200:
                st.success("로그인 성공!")  # 로그인 성공 메시지
                st.session_state['logged_in'] = True  # 로그인 상태 True
                st.session_state['username'] = username  # 로그인된 사용자명 저장
                load_user_data()  # 로그인 후 사용자 정보 불러오기
                st.experimental_rerun()  # 페이지 새로고침으로 로그인 상태 반영
            else:
                st.error("로그인 실패: 아이디 또는 비밀번호를 확인하세요.")  # 실패 시 에러 메시지
    else:
        mypage()  # 로그인 상태라면 마이페이지로 이동

# 페이지 실행
if st.session_state['logged_in']:
    mypage()  # 로그인 상태면 마이페이지 실행
else:
    login_page()  # 로그인되지 않은 상태면 로그인 페이지 실행
