import cv2
import numpy as np
#노출, 휘도,하이라이트,그림자,대비,밝기,블랙 포인트,채도,색 선명도,따듯함,색조,선명도,명료도,노이즈 감소,비네트
#밝기,대비,노이즈,색상,채도,명도,사프니스,블러
class ImageProcessor:
    def __init__(self, image_path, retouch):
        self.origin_img = cv2.imread(image_path)
        self.output_img = self.origin_img
        self.retouch = self.parse_retouch(retouch)
        

    def adjust_brightness(self, beta):
        """
        밝기를 조정합니다.
        :param beta: 밝기 조정 비율. -1~1 사이의 값을 가집니다. 양수면 밝아지고, 음수면 어두워집니다.
        """
        beta = 255 * beta
        self.output_img = cv2.convertScaleAbs(self.output_img, alpha=1, beta=beta)
        return self.output_img

    def adjust_contrast(self, alpha):
        """
        대비를 조정합니다.
        :param alpha: 대비 조정 비율. 0~2 사이의 값을 가집니다. 1보다 크면 대비가 강해지고, 1보다 작으면 대비가 약해집니다.
        """
        self.output_img = cv2.convertScaleAbs(self.output_img, alpha=alpha, beta=0)
        return self.output_img

    def reduce_noise(self, h):
        """
        노이즈를 감소시킵니다.
        :param h: 필터 강도 비율. 0~1 사이의 값을 가집니다. 값이 클수록 노이즈 감소 효과가 강해집니다. 
        """
        h = 10 * h
        hColor = h
        self.output_img = cv2.fastNlMeansDenoisingColored(self.output_img, None, h, hColor, 7, 21)
        return self.output_img

    def adjust_hue(self, h_scale):
        """
        색상(Hue) 값을 조정합니다. 색상을 바꾸는 효과가 있습니다.
        :param h_scale: H 값 조정 비율. 0~2 사이의 값을 가집니다. 값이 클수록 색조가 바뀝니다.
        """
        hsv_image = cv2.cvtColor(self.output_img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        h = np.clip(h * h_scale, 0, 180).astype(np.uint8)
        hsv_image = cv2.merge([h, s, v])
        self.output_img = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return self.output_img

    def adjust_saturation(self, s_scale):
        """
        채도(Saturation) 값을 조정합니다. 색상의 선명도를 바꾸는 효과가 있습니다.
        :param s_scale: S 값 조정 비율. 0~2 사이의 값을 가집니다. 값이 클수록 색상이 선명해집니다.
        """
        hsv_image = cv2.cvtColor(self.output_img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        s = np.clip(s * s_scale, 0, 255).astype(np.uint8)
        hsv_image = cv2.merge([h, s, v])
        self.output_img = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return self.output_img 

    def adjust_value(self, v_scale):
        """
        명도(Value) 값을 조정합니다. 이미지의 밝기를 바꾸는 효과가 있습니다.
        :param v_scale: V 값 조정 비율. 0~2 사이의 값을 가집니다. 값이 클수록 밝기가 증가합니다.
        """
        hsv_image = cv2.cvtColor(self.output_img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        v = np.clip(v * v_scale, 0, 255).astype(np.uint8)
        hsv_image = cv2.merge([h, s, v])
        self.output_img = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return self.output_img

    def sharpen(self, alpha):
        """
        이미지를 선명하게 만듭니다.
        :param alpha: 선명도 조정 비율. 0~2 사이의 값을 가집니다. 값이 클수록 선명해집니다.
        """
        blurred = cv2.GaussianBlur(self.output_img, (5,5), 0)
        self.output_img = cv2.addWeighted(self.output_img, alpha, blurred, 1-alpha, 0)
        return self.output_img

    def blur(self, beta):
        """
        이미지를 흐릿하게 만듭니다.
        :param beta: 블러 강도 비율. 0~1 사이의 값을 가집니다. 값이 클수록 블러 효과가 강해집니다.
        """
        beta = beta * 50 + 1  # 1~51 사이의 홀수
        beta = int(beta) // 2 * 2 + 1  # 홀수로 만듭니다.
        
        self.output_img = cv2.GaussianBlur(self.output_img, (beta, beta), 0)
        return self.output_img
    
    def GetOutput(self):
        return self.output_img

    #retouch 기능 실행전 전처리
    def parse_retouch(self, retouch):
        retouch_dict = {}
        retouch_items = retouch.split(",")  # 각 기능과 수치를 분리합니다.
        for item in retouch_items:
            key, value = item.split(":")  # 기능과 수치를 분리합니다.
            key = key.strip()
            value = float(value.strip())  # 수치를 실수로 변환합니다.
            retouch_dict[key] = value
        return retouch_dict

    def processing(self):
        # retouch 딕셔너리를 사용하여 이미지 처리기의 메서드를 호출합니다.
        if "밝기" in self.retouch:
            self.adjust_brightness(self.retouch["밝기"])
        if "대비" in self.retouch:
            self.adjust_contrast(self.retouch["대비"])
        if "노이즈" in self.retouch:
            self.reduce_noise(self.retouch["노이즈"])
        if "색상" in self.retouch:
            self.adjust_hue(self.retouch["색상"])
        if "채도" in self.retouch:
            self.adjust_saturation(self.retouch["채도"])
        if "명도" in self.retouch:
            self.adjust_value(self.retouch["명도"])
        if "선명도" in self.retouch:
            self.sharpen(self.retouch["선명도"])
        if "블러" in self.retouch:
            self.blur(self.retouch["블러"])

        return self.GetOutput()  # 처리된 이미지를 가져옵니다.


# retouch = "밝기: 0.1, 대비: 0.9, 노이즈: 0.2, 색상: 1.05, 채도: 1.125, 명도: 1.155, 선명도: 1.32, 블러: 0.001"

# processor  = ImageProcessor("example_img\ex1.png",retouch=retouch)
# print(processor.retouch)
# image = processor.processing()

# cv2.imshow('END', image)
# cv2.waitKey(0)

# cv2.destroyAllWindows()
