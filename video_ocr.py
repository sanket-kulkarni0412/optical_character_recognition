import cv2
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
cap=cv2.VideoCapture()
while True:
    image=cap.read()
    frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img2=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    img3=cv2.medianBlur(img2,1)
    img4=cv2.threshold(img3,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    result=pytesseract.image_to_string(img4)
    print(result)

    

