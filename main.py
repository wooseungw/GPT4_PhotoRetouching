from flask import Flask, request, render_template
from gpt4 import Gpt4
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'img_dir'  # 이미지를 저장할 위치
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']): #디렉토리 없는 경우 자동 생성
            os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 파일 열기
        with open('key.txt', 'r') as file:
            # 첫 번째 줄 읽기
            key = file.readline()
            gpt4_instance = Gpt4(key = key)
            
        image = request.files['image']  # 이미지 받기
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)  # 이미지를 저장할 경로
        image.save(filepath)  # 이미지 저장

        sentence = request.form['sentence']  # 문장 받기
        # result_image, result_sentence = gpt4_instance.parse(filepath, sentence)  # 이미지 파일 경로와 문장을 gpt4로 전달
        result_sentence = gpt4_instance.parse(filepath, sentence)  # 현재 문장만 생성하기 때문에 출력값 하나로 축소

        # return render_template('result.html', image=result_image, sentence=result_sentence)  # 결과 표시
        return render_template('result.html', sentence=result_sentence)  # 현재 문장만 생성하기 때문에 출력값 하나로 축소
    
    return render_template('index.html')  # 초기 페이지 표시

if __name__ == "__main__":
    app.run(debug=True)
