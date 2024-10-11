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

# EasyOCR Reader 생성
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 엑셀 파일 로드 함수
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

# 유사도를 계산하는 함수
def calculate_similarity(target_value, all_products, column):
    all_products = all_products.dropna(subset=[column])
    vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
    tfidf_matrix = vectorizer.fit_transform(all_products[column].astype(str))
    target_vector = vectorizer.transform([str(target_value)])
    similarity = cosine_similarity(target_vector, tfidf_matrix)
    all_products['similarity'] = similarity[0]
    similar_products = all_products.sort_values(by='similarity', ascending=False).head(5)
    return similar_products

# 이미지 확대 및 샤프닝 후 OCR 적용 함수
def preprocess_and_extract_text(image):
    image = np.array(image)
    scale_percent = 200  # 이미지 크기를 200%로 확대
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
    # 'DC' 키워드를 포함한 라인을 찾은 후, 그 뒤에 오는 V/A 정보를 추출
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

# 앱 제목
st.title('OCR 기반 인증번호 및 V/A 유사 제품 검색')

# 세션 상태 초기화
if 'cert_num_confirmed' not in st.session_state:
    st.session_state.cert_num_confirmed = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 파일 경로 설정 및 데이터 로드
file_path = './codeData.xlsx'
df = load_data(file_path)

# 이미지 파일 업로더
if df is not None:
    uploaded_file = st.file_uploader("**🤖 챗봇:** **제품 라벨 이미지를 업로드하세요**", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

if st.session_state.uploaded_file:
    st.write("**🤖 챗봇:** 인식 중입니다, 잠시만 기다려주세요...")  # 인식 중임을 알리는 메시지
    with st.spinner("이미지 인식 중입니다. 잠시만 기다려주세요..."):
        image = Image.open(st.session_state.uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)

        # 전처리 후 EasyOCR로 텍스트 추출
        extracted_text = preprocess_and_extract_text(image)
        cert_nums = extract_cert_num(extracted_text)
        v_value, a_value = extract_dc_output(extracted_text)

        # 추출된 정보들 출력
        print(f"인증번호: {cert_nums[0] if cert_nums else '추출되지 않음'}")
        print(f"정격 출력(V): {v_value}V" if v_value else "추출되지 않음")
        print(f"정격 출력(A): {a_value}A" if a_value else "추출되지 않음")

    # 인증번호가 없을 경우 V/A 검색
    if not cert_nums:
        st.write("**🤖 챗봇:** 인증번호로 제품을 찾기 어렵습니다. V/A 값을 기반으로 검색을 진행합니다...")
        time.sleep(3)

        if v_value and a_value:
            with st.spinner("V/A 검색 중입니다. 잠시만 기다려주세요..."):
                time.sleep(3)
            similar_products = calculate_similarity(f"{v_value}V {a_value}A", df, 'V')
            if not similar_products.empty:
                st.write(f"정격 출력 {v_value}V {a_value}A에 대한 유사 제품 검색 결과:")
                for _, row in similar_products.iterrows():
                    product_name = row['제품명']
                    product_url = row.get('URL', 'URL 없음')
                    product_image = row.get('Image', None)
                    st.markdown(f"<h3 style='text-align: center;'>{product_name}</h3>", unsafe_allow_html=True)
                    if product_image:
                        st.image(product_image, caption=product_name)
                    if product_url != 'URL 없음':
                        st.markdown(f"[제품 페이지]({product_url})", unsafe_allow_html=True)
                    else:
                        st.write(f"{product_name}에 대한 URL이 없습니다.")
                    st.markdown("---")  # 구분선 추가
            else:
                st.write("해당 전류와 전압으로 유사 제품을 찾을 수 없습니다.")
        else:
            st.write("V 또는 A 값이 추출되지 않았습니다. 입력을 해주세요.")
            v_value = st.text_input("정격 출력(V)을 입력하세요.")
            a_value = st.text_input("정격 출력(A)를 입력하세요.")
            if v_value and a_value:
                with st.spinner("검색 중입니다. 잠시만 기다려주세요..."):
                    time.sleep(3)
                similar_products = calculate_similarity(f"{v_value}V {a_value}A", df, 'V')
                if not similar_products.empty:
                    st.write(f"정격 출력 {v_value}V {a_value}A에 대한 유사 제품 검색 결과:")
                    for _, row in similar_products.iterrows():
                        product_name = row['제품명']
                        product_url = row.get('URL', 'URL 없음')
                        product_image = row.get('Image', None)
                        st.markdown(f"<h3 style='text-align: center;'>{product_name}</h3>", unsafe_allow_html=True)
                        if product_image:
                            st.image(product_image, caption=product_name)
                        if product_url != 'URL 없음':
                            st.markdown(f"""
    <div style='text-align: center;'>
        <a href='{product_url}' target='_blank' style='font-size:24px;'>제품 페이지</a>
    </div>
    """, unsafe_allow_html=True)
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
                if product_image:
                    st.image(product_image, caption=product_name)
                if product_url != 'URL 없음':
                    st.markdown(f"[제품 페이지]({product_url})", unsafe_allow_html=True)
                else:
                    st.write(f"{product_name}에 대한 URL이 없습니다.")
                st.markdown("---")  # 구분선 추가
        else:
            st.write(f"해당 인증번호로 유사 제품을 찾을 수 없습니다. V/A로 다시 검색합니다.")
            time.sleep(3)
            if v_value and a_value:
                with st.spinner("V/A로 검색 중입니다..."):
                    time.sleep(3)
                similar_products = calculate_similarity(f"{v_value}V {a_value}A", df, 'V')
                if not similar_products.empty:
                    for _, row in similar_products.iterrows():
                        product_name = row['제품명']
                        product_url = row.get('URL', 'URL 없음')
                        product_image = row.get('Image', None)
                        st.markdown(f"<h3 style='text-align: center;'>{product_name}</h3>", unsafe_allow_html=True)
                        if product_image:
                            st.image(product_image, caption=product_name)
                        if product_url != 'URL 없음':
                            st.markdown(f"[제품 페이지]({product_url})", unsafe_allow_html=True)
                        else:
                            st.write(f"{product_name}에 대한 URL이 없습니다.")
                        st.markdown("---")  # 구분선 추가
                else:
                    st.write("해당 전류와 전압으로 유사 제품을 찾을 수 없습니다.")

    # 처음으로 버튼 추가
    if st.session_state.cert_num_confirmed:
        if st.button("처음으로"):
            st.session_state.cert_num_confirmed = False
            st.session_state.uploaded_file = None
            st.session_state.chat_history = []  # 초기화 후 처음으로 돌아가기
            st.write("초기 상태로 돌아갑니다. 페이지를 새로고침하세요.")

else:
    st.warning("데이터를 불러오지 못했습니다.")

