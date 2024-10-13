import streamlit as st
import pandas as pd
import re
import numpy as np
import easyocr
import time
import cv2
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import os
import requests


def login_page():
    st.title("로그인")

    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        # POST 요청으로 데이터 전송
        login_data = {"username": username, "password": password}
        response = requests.post("http://localhost:8080/auth/login", json=login_data)

        if response.status_code == 200:
            st.success("로그인 성공!")
        else:
            st.error("로그인 실패. 아이디와 비밀번호를 확인하세요.")




# 환경 설정
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
torch.set_num_threads(1)

# EasyOCR Reader 생성
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 엑셀 파일에서 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        # 엑셀 파일에서 데이터 로드
        df = pd.read_excel('./codeData.xlsx')  # 엑셀 파일 이름을 'codeData.xlsx'로 가정
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

# 유사도를 계산하는 함수 (V, A 기반으로 유사 제품 찾기)
def calculate_similarity(target_value, all_products, column):
    all_products = all_products.dropna(subset=[column])  # 유사도 계산을 위해 null 값 제거
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
    tfidf_matrix = vectorizer.fit_transform(all_products[column].astype(str))  # 대상 컬럼 벡터화
    target_vector = vectorizer.transform([str(target_value)])
    similarity = cosine_similarity(target_vector, tfidf_matrix)  # 코사인 유사도 계산
    all_products['similarity'] = similarity[0]
    similar_products = all_products.sort_values(by='similarity', ascending=False).head(5)
    return similar_products

# 이미지 확대 및 샤프닝 후 OCR 적용 함수
def preprocess_and_extract_text(image):
    image = np.array(image)
    scale_percent = 200  # 이미지 크기 200%로 확대
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    # 이미지 확대
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    # 샤프닝 커널 적용
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened_image = cv2.filter2D(resized_image, -1, kernel)

    # OCR 적용
    ocr_result = reader.readtext(sharpened_image, detail=0)
    extracted_text = " ".join(ocr_result)

    return extracted_text

# 정격출력 DC 정보를 추출하는 함수
def extract_dc_output(text):
    dc_output_match = re.search(r'DC\s?(\d{1,3}(\.\d+)?)[Vv]?\s?(\d{1,3}(\.\d+)?)[Aa]?', text)
    if dc_output_match:
        v_value = dc_output_match.group(1)
        a_value = dc_output_match.group(3)
        return v_value, a_value
    return None, None

# 인증번호를 추출하는 함수
def extract_cert_num(text):
    cert_nums = re.findall(r'\b[A-Z]{2}\d{5}-\d{5}\b', text)
    return cert_nums

# 제품 찜하기 기능
def add_to_wishlist(product_name):
    if product_name not in st.session_state['wishlist']:
        st.session_state['wishlist'].append(product_name)
        st.success(f"{product_name}을(를) 찜 목록에 추가했습니다!")
    else:
        st.warning(f"{product_name}은(는) 이미 찜 목록에 있습니다.")

# 링크 클릭 카운트 기능
def count_click(product_name):
    if product_name not in st.session_state['click_counts']:
        st.session_state['click_counts'][product_name] = 0
    st.session_state['click_counts'][product_name] += 1
    st.write(f"clicked : {st.session_state['click_counts'][product_name]}")





# 앱 제목
st.markdown("""
    <h1 style='text-align: center; margin: 50px 0;'>
        챗봇 제품검색 서비스
    </h1>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'cert_num_confirmed' not in st.session_state:
    st.session_state.cert_num_confirmed = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'wishlist' not in st.session_state:
    st.session_state.wishlist = []
if 'click_counts' not in st.session_state:
    st.session_state.click_counts = {}

# 데이터 로드
df = load_data()

# 엑셀 데이터를 성공적으로 불러왔는지 확인 후 출력
if df is not None:
    st.markdown("""
        <p style='text-align: center; font-size: 18px;margin-bottom:30px'>
            고성능의 OCR 인공지능 챗봇이 빠르게 스캔하여 정확한 제품을 추천드립니다.
        </p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <p style='text-align: center; font-size: 18px;'>
            데이터를 불러올 수 없습니다.
        </p>
    """, unsafe_allow_html=True)

# 이미지 파일 업로더
if df is not None:
    uploaded_file = st.file_uploader("**🤖 챗봇:** **제품 라벨 이미지를 업로드하세요**", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file:
    st.write("**🤖 챗봇:** 인식 중입니다, 잠시만 기다려주세요...")
    with st.spinner("이미지 인식 중입니다. 잠시만 기다려주세요..."):
        image = Image.open(st.session_state.uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)

        # EasyOCR로 텍스트 추출
        extracted_text = preprocess_and_extract_text(image)
        cert_nums = extract_cert_num(extracted_text)
        v_value, a_value = extract_dc_output(extracted_text)

        # 추출된 정보 출력
        st.write(f"인증번호: {cert_nums[0] if cert_nums else '추출되지 않음'}")
        st.write(f"정격 출력(V): {v_value}V" if v_value else "추출되지 않음")
        st.write(f"정격 출력(A): {a_value}A" if a_value else "추출되지 않음")

    # 인증번호가 없을 경우 V/A 검색
    if not cert_nums:
        st.write("**🤖 챗봇:** 인증번호로 제품을 찾기 어렵습니다. 정격출력 V/A 값을 기반으로 검색을 진행합니다...")
        time.sleep(3)
        similar_products = None  # Initialize to None
        if v_value and a_value:
            with st.spinner("정격출력 V/A 검색 중입니다. 잠시만 기다려주세요..."):
                time.sleep(3)
            similar_products = calculate_similarity(f"{v_value}V {a_value}A", df, 'V')
            if not similar_products.empty:
                st.write(f"정격 출력 {v_value}V {a_value}A에 대한 유사 제품 검색 결과:")
                for _, row in similar_products.iterrows():
                    product_name = row['제품명']
                    product_url = row.get('URL', 'URL 없음')
                    product_image = row.get('Image', None)
                    st.markdown(f"<h3 style='text-align: center;'>{product_name}</h3>", unsafe_allow_html=True)

                    # 제품 이미지 표시
                    if product_image:
                        st.image(product_image, caption=product_name)

                    # 제품 링크 및 찜하기 기능
                    if product_url != 'URL 없음':
                        # Add CSS to style both the 링크 이동 and 찜하기 buttons
                        button_style = """
                        <style>
                            .button-container {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                gap: 15px;  /* Space between the buttons */
                            }
                            .custom-button {
                                display: inline-block;
                                padding: 10px 20px;
                                margin: 40px 0;
                                background-color: #fff;
                                border: 1px solid #ccc;
                                border-radius: 5px;
                                font-size: 16px;
                                text-align: center;
                                text-decoration: none;
                                color: #000;
                                transition: background-color 0.3s;
                            }
                            .custom-button:hover {
                                background-color: #f7f7f7;
                            }
                        </style>
                        """

                        # Apply the button style using markdown
                        st.markdown(button_style, unsafe_allow_html=True)

                        # Create a container for both buttons using HTML
                        st.markdown(
                            f"""
                            <div class="button-container">
                                <a href="{product_url}" target="_blank" rel="noopener noreferrer" class="custom-button">📎 링크 이동</a>
                                <a href="#" class="custom-button" onclick="alert('찜하기 버튼 클릭됨!')">❤️ 찜하기</a>
                            </div>
                            """, unsafe_allow_html=True
                        )
                    else:
                        st.write(f"{product_name}에 대한 URL이 없습니다.")

                    st.markdown("---")  # 구분선 추가



            else:
                st.write("해당 전류와 전압으로 유사 제품을 찾을 수 없습니다.")

    # 인증번호가 추출된 경우 자동 검색
    if cert_nums:
        cert_num = cert_nums[0]
        st.session_state.cert_num_confirmed = True

        with st.spinner("인증번호로 제품 검색 중입니다..."):
            time.sleep(3)
            similar_products = calculate_similarity(cert_num, df, '인증번호')

        if not similar_products.empty:
            st.write(f"인증번호 {cert_num}에 대한 유사 제품 검색 결과:")
            for _, row in similar_products.iterrows():
                product_name = row['제품명']
                product_url = row.get('URL', 'URL 없음')
                product_image = row.get('Image', None)
                st.markdown(f"<h3 style='text-align: center;'>{product_name}</h3>", unsafe_allow_html=True)

                # 제품 이미지 표시
                if product_image:
                    st.image(product_image, caption=product_name)

                # 제품 링크 및 찜하기 기능
                # Loop through similar products and display them
                if not similar_products.empty:
                    st.write(f"인증번호 {cert_num}에 대한 유사 제품 검색 결과:")

                    for i, row in similar_products.iterrows():
                        product_name = row['제품명']
                        product_url = row.get('URL', 'URL 없음')
                        product_image = row.get('Image', None)

                        # Add "선택" text before each product name
                        st.markdown(f"""
                            <h2 style='text-align: center; font-size: 24px;'>
                                선택 {i + 1}
                            </h2>
                        """, unsafe_allow_html=True)

                        # Display product name in the center with larger font
                        st.markdown(f"""
                            <h3 style='text-align: center; font-size: 22px;'>
                                {product_name}
                            </h3>
                        """, unsafe_allow_html=True)

                        # Display product image
                        if product_image:
                            st.image(product_image, caption=product_name, use_column_width=True)

                        # Product link and 찜하기 button
                        if product_url != 'URL 없음':
                            button_style = """
                            <style>
                                .button-container {
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    gap: 15px;  /* Space between the buttons */
                                }
                                .custom-button {
                                    display: inline-block;
                                    padding: 10px 20px;
                                    margin: 40px 0;
                                    background-color: #fff;
                                    border: 1px solid #ccc;
                                    border-radius: 5px;
                                    font-size: 16px;
                                    text-align: center;
                                    text-decoration: none;
                                    color: #000;
                                    transition: background-color 0.3s;
                                }
                                .custom-button:hover {
                                    background-color: #f7f7f7;
                                }
                            </style>
                            """

                            # Apply the button style using markdown
                            st.markdown(button_style, unsafe_allow_html=True)

                            # Create a container for both buttons using HTML
                            st.markdown(f"""
                                <div class="button-container">
                                    <a href="{product_url}" target="_blank" rel="noopener noreferrer" class="custom-button">📎 링크 이동</a>
                                    <a href="#" class="custom-button" onclick="alert('찜하기 버튼 클릭됨!')">❤️ 찜하기</a>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.write(f"{product_name}에 대한 URL이 없습니다.")

                        st.markdown("---")  # 구분선 추가


                # 찜한 제품 목록 표시
                if st.session_state.wishlist:
                    st.write("**찜한 제품 목록**")
                    for item in st.session_state.wishlist:
                        st.write(f"- {item}")

                # 처음으로 버튼 추가
                if st.session_state.cert_num_confirmed:
                    if st.button("처음으로"):
                        st.session_state.cert_num_confirmed = False
                        st.session_state.uploaded_file = None
                        st.session_state.wishlist = []
                        st.write("초기 상태로 돌아갑니다. 페이지를 새로고침하세요.")
