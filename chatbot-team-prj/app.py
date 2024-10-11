import streamlit as st
import pandas as pd
import re
import numpy as np
import easyocr
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from PIL import Image

# EasyOCR Reader 생성
reader = easyocr.Reader(['en', 'ko'])  # 한국어와 영어 지원

# 엑셀 파일 로드 함수
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

# 제품 간 유사도를 계산하는 함수 (모델명, 인증번호를 기반으로)
def calculate_similarity(target_text, all_products):
    text_features = ['제품명', '모델명', '인증번호']  # 사용할 텍스트 특성

    # NaN 처리 및 텍스트 특성 결합
    all_products = all_products.dropna(subset=text_features)
    all_products['combined_text'] = all_products['제품명'].astype(str) + ' ' + all_products['모델명'].astype(str) + ' ' + all_products['인증번호'].astype(str)
    
    # TF-IDF를 사용한 벡터화
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_products['combined_text'])

    # 대상 텍스트 벡터화
    target_tfidf_vector = vectorizer.transform([target_text])

    # 텍스트 유사도 계산
    text_similarity = cosine_similarity(target_tfidf_vector, tfidf_matrix)

    # 유사도 순으로 정렬 (상위 5개만 반환)
    all_products['similarity'] = text_similarity[0]
    similar_products = all_products.sort_values(by='similarity', ascending=False).head(5)

    return similar_products

# OCR로 텍스트 추출
def extract_text_from_image(image):
    ocr_result = reader.readtext(np.array(image), detail=0)  # OCR 결과에서 텍스트만 반환
    extracted_text = " ".join(ocr_result)  # 추출된 텍스트를 하나의 문자열로 결합
    return extracted_text

# 제품 인증번호와 모델명을 추출하는 함수
def extract_cert_and_model(text):
    cert_num = re.search(r'\b[A-Z]{2}\d{5}-\d{5}\b', text)  # 인증번호 패턴: XX00000-00000
    model_name = re.search(r'[A-Za-z0-9\-]+', text)  # 모델명 추출 (단순한 문자, 숫자 및 대시)
    
    return cert_num.group(0) if cert_num else None, model_name.group(0) if model_name else None

# 앱 제목
st.title('OCR 기반 제품 검색')

# 파일 경로 설정 및 데이터 로드
file_path = './codeData.xlsx'
df = load_data(file_path)

# 데이터가 로드된 경우만 처리
if df is not None:
    # 이미지 파일 업로드
    uploaded_file = st.file_uploader("제품 라벨 이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # 이미지 로드 및 PIL로 변환
        image = Image.open(uploaded_file)

        # 원본 이미지 표시
        st.image(image, caption="업로드된 원본 이미지", use_column_width=True)

        # EasyOCR로 텍스트 추출
        extracted_text = extract_text_from_image(image)
        st.write(f"추출된 텍스트: {extracted_text}")

        # 모델명과 인증번호 추출
        cert_num, model_name = extract_cert_and_model(extracted_text)
        
        if cert_num or model_name:
            st.write(f"추출된 인증번호: {cert_num if cert_num else '인증번호 없음'}")
            st.write(f"추출된 모델명: {model_name if model_name else '모델명 없음'}")

            # 인증번호 또는 모델명으로 유사 제품 검색
            search_text = f"{model_name if model_name else ''} {cert_num if cert_num else ''}".strip()
            if search_text:
                similar_products = calculate_similarity(search_text, df)
                st.write(f"유사한 제품 (상위 5개):")
                st.dataframe(similar_products[['제품명', '모델명', '인증번호', 'similarity']])
        else:
            st.write("모델명이나 인증번호를 추출할 수 없습니다.")
    else:
        st.write("제품 이미지를 업로드하세요.")
else:
    st.warning("데이터를 불러오지 못했습니다. 파일 경로를 확인하세요.")
