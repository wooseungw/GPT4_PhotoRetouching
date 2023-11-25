from flask import Flask, request, render_template
from gpt4 import Gpt4
import os
import shutil
from edit_img import *

app = Flask(__name__)
UPLOAD_FOLDER = './img_dir'  # 이미지를 저장할 위치
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('./static', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 파일 열기
        with open('key.txt', 'r') as file:
            # 첫 번째 줄 읽기
            key = file.readline()
            gpt4_instance = Gpt4(key = key)
            
        image = request.files['image']  # 이미지 받기
        filepath = f"{app.config['UPLOAD_FOLDER']}/{image.filename}"
        image.save(filepath)  # 이미지 저장
        shutil.copy(filepath, f'./static/{image.filename}')     # 이미지를 static 폴더에 복사 -> static 폴더에 있어야 html에서 출력가능

        sentence = request.form['sentence']  # 문장 받기
        #문장 처리
        result_sentences = gpt4_instance.parse(filepath, sentence)  # 현재 문장만 생성하기 때문에 출력값 하나로 축소
        #이미지 처리
        processor  = ImageProcessor(filepath, retouch=result_sentences['retouch'])
        result_img = processor.processing()


        # 이미지 저장
        cv2.imwrite(f"./static/result.jpg", result_img)

        # 결과 표시
        return render_template('result.html', original_image=image.filename, image="result.jpg", sentence_text=result_sentences['text'], sentence_retouch=result_sentences['retouch'])

    return render_template('index.html')  # 초기 페이지 표시

if __name__ == "__main__":
    app.run(debug=True)
