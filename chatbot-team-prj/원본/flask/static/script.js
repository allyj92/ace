document.getElementById('search-form').addEventListener('submit', function (e) {
    e.preventDefault();  // 폼의 기본 제출 동작을 막음

    let certNum = document.getElementById('cert_num').value;
    let modelName = document.getElementById('model_name').value;

    let formData = new FormData();
    formData.append('cert_num', certNum);
    formData.append('model_name', modelName);

    fetch('/search', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            let resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '';  // 기존 결과 초기화

            if (Array.isArray(data)) {
                data.forEach(item => {
                    let resultItem = `
                    <p><strong>인증번호:</strong> ${item.인증번호}</p>
                    <p><strong>제품명:</strong> ${item.제품명}</p>
                    <p><strong>모델명:</strong> ${item.모델명}</p>
                    <p><strong>제조사:</strong> ${item.제조사}</p>
                    <p><strong>제조국:</strong> ${item.제조국}</p>
                `;
                    // 비고 항목이 있을 때만 추가
                    if (item.비고 && item.비고 !== 'NaN') {
                        resultItem += `<p><strong>비고:</strong> ${item.비고}</p>`;
                    }
                    resultItem += `<hr>`;
                    resultDiv.innerHTML += resultItem;
                });
            } else {
                resultDiv.innerHTML = `<p>${data}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
