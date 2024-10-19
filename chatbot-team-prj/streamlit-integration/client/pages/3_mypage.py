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
    st.session_state['phone_number'] = ''  # 전화번호 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # 로그인 상태 초기화

 # 서버에서 유저의 찜 리스트를 불러오는 함수 (정의된 위치 확인)
def load_wishlist_from_server(username):
        url = f"http://localhost:8080/user/{username}/wishlist"  # 유저의 찜 리스트를 불러오는 API 엔드포인트
        try:
            response = requests.get(url)
            if response.status_code == 200:
                st.session_state['wishlist'] = response.json()  # 서버에서 받은 찜 리스트를 세션에 저장
            else:
                st.error(f"찜 리스트를 불러오는 데 실패했습니다: {response.text}")
        except Exception as e:
            st.error(f"불러오는 중 오류가 발생했습니다: {e}")


# 서버에서 사용자 정보와 찜한 상품 목록을 가져오는 함수
def load_user_data():
    response = requests.get(f"{API_BASE_URL}/user/{st.session_state['username']}")
    if response.status_code == 200:
        user_data = response.json()  # 서버로부터 사용자 정보 JSON 형태로 가져옴
        st.session_state['username'] = user_data['username']  # 사용자명 설정
        st.session_state['email'] = user_data['email']  # 이메일 설정
        st.session_state['phone_number'] = user_data['phone_number']  # 전화번호 설정
        if 'wishlist' in user_data:
            st.session_state['wishlist'] = user_data['wishlist']  # 찜한 상품 목록 설정
        else:
            load_wishlist_from_server(st.session_state['username'])  # 별도의 wishlist API 호출
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
    return response #response 객체를 반환

# 찜한 상품 목록을 모두 삭제하는 함수
def delete_all_wishlist():
    response = requests.delete(f"{API_BASE_URL}/user/{st.session_state['username']}/wishlist")
    return response.status_code == 200  # 삭제 성공 여부 반환

# 찜한 상품 목록 표시 섹션
def display_wishlist():
    st.header("찜한 상품 목록")

    # 찜 리스트를 세션에서 가져오기 전에 서버에서 찜 리스트를 불러옴
    if 'username' in st.session_state and st.session_state['username']:
       load_wishlist_from_server(st.session_state['username'])  # 서버에서 찜 리스트를 불러오기

    # wishlist가 있는지 확인
    if st.session_state['wishlist']:

        # wishlist의 각 상품을 순회하며 처리
        for product in st.session_state['wishlist']:
            if isinstance(product, dict):
                product_name = product.get('name', '이름 없음')
                product_image = product.get('image', None)
                product_url = product.get('url', 'URL 없음')

                # 제품명 출력
                st.write(f"**상품명:** {product_name}")

                # 이미지 출력
                if product_image:
                    st.image(product_image, caption=product_name)

                # URL 링크 출력
                if product_url:
                    st.markdown(
                        f"""
                        <div style='display: flex; justify-content: center;'>
                            <a href="{product_url}" target="_blank" style="text-decoration: none; background-color: #ebebeb; color: gray; padding: 10px 20px; border-radius: 5px; text-align: center;">
                                상품 페이지로 이동하기
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("---")  # 구분선
            else:
                st.error("상품 데이터가 올바르지 않습니다.")  # 잘못된 형식의 데이터 처리
    else:
        st.write("찜한 상품이 없습니다.")  # 찜한 상품이 없을 때 메시지 표시

# 마이페이지 UI
def mypage():
    st.title("마이페이지")  # 페이지 제목 설정

    # 사용자 정보 수정 섹션
    st.header("나의 정보 수정")
    with st.form(key='update_info'):
        # 로그인된 경우 세션에서 이메일과 전화번호를 불러오고, 로그아웃 상태일 경우 빈 값을 사용
        if st.session_state['logged_in']:
            load_user_data()
            new_email = st.text_input("이메일", value=st.session_state.get('email', ''))
            new_phone_number = st.text_input("전화번호", value=st.session_state.get('phone_number', ''))
        else:
            new_email = st.text_input("이메일", value='')
            new_phone_number = st.text_input("전화번호", value='')

        if st.form_submit_button("정보 수정"):
            if st.session_state['logged_in']:  # 로그인된 상태에서만 정보 수정 가능
                response = update_user_info(new_email, new_phone_number)
                if response.status_code==200:
                    st.session_state['email'] = new_email
                    st.session_state['phone_number'] = new_phone_number
                    st.success("정보가 성공적으로 수정되었습니다!")  # 성공 메시지 표시
                else:
                    st.error(f"정보 수정에 실패했습니다. 상태 코드: {response.status_code}, 응답 내용: {response.text}")  # 실패 메시지 표시 및 디버깅 정보 출력  # 실패 메시지 표시
            else:
                st.error("로그인이 필요합니다.")  # 로그인되지 않은 상태에서는 수정 불가

    # 찜한 상품 목록 표시
    display_wishlist()

    # 찜한 상품 모두 삭제 버튼
    if st.button("찜한 상품 모두 삭제"):
        if delete_all_wishlist():
            st.session_state['wishlist'].clear()  # 찜한 상품 목록 초기화
            st.success("찜한 상품이 모두 삭제되었습니다.")  # 성공 메시지
        else:
            st.error("찜한 상품 삭제에 실패했습니다.")  # 실패 메시지

    # 서버에서 유저의 찜 리스트를 불러오는 함수
    # 로그인 후 유저의 찜 리스트 불러오기
    def load_wishlist_after_login(username):
        load_user_data()  # 사용자 정보 로드
        load_wishlist_from_server(username)  # 찜한 상품 리스트 로드



    # 로그인 후 유저의 찜 리스트 불러오기
    if 'logged_in' in st.session_state and st.session_state['logged_in']:
        load_wishlist_from_server(st.session_state['username'])

    # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state.clear()  # 세션 상태 초기화
        st.session_state['logged_in'] = False  # 로그인 상태 해제
#         st.experimental_rerun()  # 페이지 새로고침으로 로그아웃 처리

# 로그인 페이지 UI
def login_page():
    st.title("로그인")  # 로그인 페이지 제목 설정

    if not st.session_state['logged_in']:
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        st.write(f"**아이디:** {st.session_state['username']}")
        st.write(f"**이메일:** {st.session_state['email']}")
        st.write(f"**전화번호:** {st.session_state['phone_number']}")

        if st.button("로그인"):
            login_data = {"username": username, "password": password}
            response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)

            if response.status_code == 200:
                st.success("로그인 성공!")  # 로그인 성공 메시지
                st.session_state['logged_in'] = True  # 로그인 상태 True
                st.session_state['username'] = username  # 로그인된 사용자명 저장
                load_user_data()  # 로그인 후 사용자 정보 불러오기
#                 st.experimental_rerun()  # 페이지 새로고침으로 로그인 상태 반영
            else:
                st.error("로그인 실패: 아이디 또는 비밀번호를 확인하세요.")  # 실패 시 에러 메시지
    else:
        mypage()  # 로그인 상태라면 마이페이지로 이동

# 페이지 실행
if st.session_state['logged_in']:
    mypage()  # 로그인 상태면 마이페이지 실행
else:
    login_page()  # 로그인되지 않은 상태면 로그인 페이지 실행
