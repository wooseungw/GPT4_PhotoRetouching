# from IPython.display import display, Image, Audio

# import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
# import time
from openai import OpenAI
# import os
# import requests


class Gpt4:
  def __init__(self, key) -> None:
    self.key = key
    self.client = OpenAI(api_key = key)

  def parse(self, filepath, sentence):
    base64_img = self._img_to_base64(filepath) # 저장된 이미지 파일을 불러와서 base64형식으로 변환

    response = self.client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
      {
        "role": "system",
        "content": [
          {"type": "text", "text": "역활 놀이를 하자 나는 요청자고 너는 Setimental한 Photo Retouching으로 상을 받은 사진가야. \
            나는 내가 원하는 색감이나 감성을 이미지와 함께 입력할꺼야.\
            너는 그 이미지의 어떤 오브젝트가 있는지와 광량, 추정된 위치 등을 바탕으로, 피사체를 강조하는게 좋을지 아니면 전체적인 분위기를 보여주는게 좋을지 말해주고,그런데 [text]로 시작해서[/text]로 끝내줘.\
            내가 보내준 사진에 어울리는 사진보정방법을 알려줘야해.\
            사진 보정법을 알려줄땐 [retorch]로시작해서 [/retorch]로 끝내야해 그리고 안에 사진 보정 속성 (채도,하이라이트,등 속성) 중 바꿔야 할 부분을 수치화 해서 알려줘.\
              예시로 [retorch]\n 채도 '10' , 하이라이트 '-20',... [/retorch]\
            다 알려주면 대화 종료야"},
        ],
      },
      {
        "role": "user",
        "content": [
          {"type": "text", "text": f"{sentence}"},
          {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}", "detail":"low"}},  # detail 필요시 high로 변경 가능
          ],
        }
      ],
      max_tokens=500,
    )
    return response.choices[0].message.content

  def _img_to_base64(self, filepath) -> str:
    '''
    이미지 파일을 filepath에서 불러와서 base64(string) 형식으로 변경
    '''
    with open(filepath, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')