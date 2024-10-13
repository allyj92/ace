import streamlit as st

# 초기화
if 'wishlist' not in st.session_state:
    st.session_state['wishlist'] = ['상품1', '상품2', '상품3']  # 찜한 상품 예시
if 'username' not in st.session_state:
    st.session_state['username'] = 'test_user'  # 초기 사용자명
if 'email' not in st.session_state:
    st.session_state['email'] = 'test_user@example.com'  # 초기 이메일
if 'phone_number' not in st.session_state:
    st.session_state['phone_number'] = '010-1234-5678'  # 초기 전화번호

# 마이페이지 UI
def mypage():
    st.title("마이페이지")

    # 사용자 정보 수정 섹션
    st.header("나의 정보 수정")
    with st.form(key='update_info'):
        new_username = st.text_input("아이디", value=st.session_state['username'])
        new_email = st.text_input("이메일", value=st.session_state['email'])
        new_phone_number = st.text_input("전화번호", value=st.session_state['phone_number'])

        if st.form_submit_button("정보 수정"):
            st.session_state['username'] = new_username
            st.session_state['email'] = new_email
            st.session_state['phone_number'] = new_phone_number
            st.success("정보가 성공적으로 수정되었습니다!")

    # 찜한 상품 섹션
    st.header("찜한 상품 목록")
    if st.session_state['wishlist']:
        for product in st.session_state['wishlist']:
            st.write(f"- {product}")
    else:
        st.write("찜한 상품이 없습니다.")

    # 찜한 상품 삭제 기능
    if st.button("찜한 상품 모두 삭제"):
        st.session_state['wishlist'].clear()
        st.success("찜한 상품이 모두 삭제되었습니다.")

    # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state.clear()
        st.write("로그아웃 되었습니다. 다시 로그인 해주세요.")

# 마이페이지 실행
mypage()