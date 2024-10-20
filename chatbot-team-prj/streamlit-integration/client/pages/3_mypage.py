import streamlit as st
import requests

# 서버 URL 설정 (REST API 서버 주소 설정)
API_BASE_URL = "http://localhost:8080"

# # 세션 상태 초기화
if 'wishlist' not in st.session_state:
    st.session_state['wishlist'] = []  # 찜한 상품 목록을 서버에서 가져옴

# 세션 상태 초기화 (이미 값이 있는지 확인 후 초기화)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False  # 로그인 상태 초기화

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
    url = f"http://localhost:8080/user/{username}/wishlist"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            st.session_state['wishlist'] = response.json()
        else:
            st.error(f"찜 리스트를 불러오는 데 실패했습니다: {response.text}")
    except Exception as e:
        st.error(f"불러오는 중 오류가 발생했습니다: {e}")

# 서버에서 사용자 정보와 찜한 상품 목록을 가져오는 함수
def load_user_data():
    response = requests.get(f"{API_BASE_URL}/user/{st.session_state['username']}")
    if response.status_code == 200:
        user_data = response.json()
        st.session_state['username'] = user_data['username']
        st.session_state['email'] = user_data['email']
        st.session_state['phone_number'] = user_data['phone_number']
        if 'wishlist' in user_data:
            st.session_state['wishlist'] = user_data['wishlist']
        else:
            load_wishlist_from_server(st.session_state['username'])
    else:
        st.error("사용자 정보를 불러오는 데 실패했습니다.")

# 찜한 상품 목록 표시 섹션
def display_wishlist():
    st.header("찜한 상품 목록")

    # 세션에서 wishlist가 있는지 확인
    if st.session_state['wishlist']:
        # wishlist 안에 있는 각각의 상품을 가져와 출력
        for product in st.session_state['wishlist']:
            product_name = product.get('name', '이름 없음')
            product_image = product.get('image', None)
            product_url = product.get('url', 'URL 없음')

            st.write(f"**상품명:** {product_name}")

            if product_image:
                st.image(product_image, caption=product_name)

            if product_url:
                st.markdown(
                    f"""
                    <div style='display: flex; justify-content: center;'>
                        <a href="{product_url}" target="_blank" style="text-decoration: none; background-color: #ebebeb; color: gray; padding: 10px 20px; border-radius: 5px; text-align: center;'>
                            상품 페이지로 이동하기
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")  # 구분선
    else:
        st.write("찜한 상품이 없습니다.")

    # 세션 상태의 wishlist를 별도로 표시 (디버깅용)
    st.subheader("세션에 저장된 찜한 상품 목록")
    for item in st.session_state['wishlist']:
        st.write(f"상품명: {item.get('name', '이름 없음')}, URL: {item.get('url', 'URL 없음')}")

display_wishlist()
# 마이페이지 UI
def mypage():

    st.title("마이페이지")

    st.header("나의 정보 수정")
    with st.form(key='update_info_form'):
        if st.session_state['logged_in']:
            load_user_data()
            new_email = st.text_input("이메일", value=st.session_state.get('email', ''))
            new_phone_number = st.text_input("전화번호", value=st.session_state.get('phone_number', ''))
        else:
            new_email = st.text_input("이메일", value='')
            new_phone_number = st.text_input("전화번호", value='')

        if st.form_submit_button("정보 수정"):
            if st.session_state['logged_in']:
                response = update_user_info(new_email, new_phone_number)
                if response.status_code == 200:
                    st.session_state['email'] = new_email
                    st.session_state['phone_number'] = new_phone_number
                    st.success("정보가 성공적으로 수정되었습니다!")

                else:
                    st.error(f"정보 수정에 실패했습니다. 상태 코드: {response.status_code}, 응답 내용: {response.text}")
            else:
                st.error("로그인이 필요합니다.")

    # 찜한 상품 목록 표시
    display_wishlist()


    if st.button("찜한 상품 모두 삭제"):
        if delete_all_wishlist():
            st.session_state['wishlist'].clear()
            st.success("찜한 상품이 모두 삭제되었습니다.")
        else:
            st.error("찜한 상품 삭제에 실패했습니다.")

    if st.button("로그아웃"):
        st.session_state.clear()
        st.session_state['logged_in'] = False


# 로그인 페이지 UI
def login_page():
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
                load_user_data()
            else:
                st.error("로그인 실패: 아이디 또는 비밀번호를 확인하세요.")
    else:
        mypage()

# 페이지 실행 로직
if st.session_state['logged_in']:
    mypage()
else:
    login_page()


