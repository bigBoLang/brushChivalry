import cv2
from paddleocr import PaddleOCR

def recognize_text(image_path):
    # 初始化 PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # 使用中文模型
    # 读取图像
    image = cv2.imread(image_path)

    # 进行文字识别
    results = ocr.ocr(image_path, cls=True)

    # 提取识别到的文本
    extracted_texts = []
    for line in results:
        for word_info in line:
            text = word_info[1][0]  # 提取文本
            extracted_texts.append(text)

    return extracted_texts

def main():
    image_path = 'capture.png'  # 替换为您的图像路径
    texts = recognize_text(image_path)

    # 打印识别到的文本
    print("识别到的文本:")
    for text in texts:
        print(text)

if __name__ == "__main__":
    main()