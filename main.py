from flask import Flask, request, render_template
import gpt4

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['image']  # 이미지 받기
        sentence = request.form['sentence']  # 문장 받기
        result_image, result_sentence = gpt4.parse(image, sentence)  # pgt4를 사용해서 이미지와 문장 처리
        return render_template('result.html', image=result_image, sentence=result_sentence)  # 결과 표시
    return render_template('index.html')  # 초기 페이지 표시

if __name__ == "__main__":
    app.run(debug=True)
