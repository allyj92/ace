from flask import Flask, request, jsonify, render_template
import pandas as pd

# Flask 앱 초기화
app = Flask(__name__)

# 엑셀 파일 로드 (파일 경로 업데이트 필요)
file_path = 'merged_unique_model_names - 추가.xlsx'  # 파일 경로를 알맞게 수정
df = pd.read_excel(file_path)

# 제품 검색 함수: 인증번호 또는 모델명으로 검색할 수 있습니다.
def search_product(cert_num=None, model_name=None):
    if cert_num:
        # 인증번호로 검색
        result = df[df['인증번호'] == cert_num]
    elif model_name:
        # 모델명으로 검색
        result = df[df['모델명'] == model_name]
    else:
        return "인증번호 또는 모델명을 입력해주세요."

    # 결과가 존재할 경우 해당 제품 정보 반환
    if not result.empty:
        return result[['인증번호', '제품명', '모델명', '제조사', '제조국','비고']].to_dict(orient='records')
    else:
        return "해당 정보로 제품을 찾을 수 없습니다."

# 기본 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# 제품 검색 요청 처리
@app.route('/search', methods=['POST'])
def search():
    cert_num = request.form.get('cert_num')
    model_name = request.form.get('model_name')

    # 제품 검색 결과 반환
    result = search_product(cert_num=cert_num, model_name=model_name)
    return jsonify(result)

# Flask 앱 실행
if __name__ == '__main__':
    app.run(debug=True)
