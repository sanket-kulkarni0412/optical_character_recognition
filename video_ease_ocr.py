from PIL import Image
import cv2
import pytesseract
import os
import easyocr
import imageio
import numpy as np
import datetime

def get_text(video_path,inst):
    #os.makedirs('text.csv',exist_ok=True)
    os.makedirs('output_images',exist_ok=True)
    image_frames= 'image_frames'
    try:
        os.remove(image_frames)
    except OSError:
        pass

    if not os.path.exists(image_frames):
        os.makedirs(image_frames)
        

    index=0
    inst=float(inst)
    src_vid= cv2.VideoCapture(video_path)
    fps=src_vid.get(cv2.CAP_PROP_FPS)
    tfr=src_vid.get(cv2.CAP_PROP_FRAME_COUNT)
    fr=round(inst*fps)
    sec=int(round(tfr/fps))
    while True:
        ret, frame = src_vid.read()
        if ret==False:
            break
        name='image_frames/frame'+str(index)+'.jpg'

        if index % fr==0:
            print('Extracting frame',name)
            image=cv2.imwrite(name, frame)
        index=index+1
        if cv2.waitKey(10) and 0xFF == ord('q'):
            break
    src_vid.release()
    cv2.destroyAllWindows()

    reader= easyocr.Reader(['en'],gpu=True)
    j=inst
    while j<=sec:
        for file in os.listdir(image_frames):
            dtsring=datetime.timedelta(seconds=j)
            img=Image.open('image_frames'+'/'+file)
            imgarray=np.array(img)
            img3=cv2.medianBlur(imgarray,1)
            result= reader.readtext(img3)
            text_list=[]
            for i in range (0,len(result)):
                top_left= result[i][0][0]
                bottom_right= result[i][0][2]
                text=result[i][1]
                img=cv2.rectangle(imgarray,top_left,bottom_right,(155,155,0),2)
                img=cv2.putText(imgarray, text,top_left,cv2.FONT_HERSHEY_COMPLEX,0.5,(155,155,0),1,cv2.LINE_AA)

                text_list.append(text)

            with open('text.csv','r+') as ft:
                mydatalist=ft.readlines()
                textlist=[]
                for line in mydatalist:
                    entry=line.split(',')  
                    textlist.append(entry[1].replace('\n',''))
            if text not in textlist:
                with open('text.csv','a+') as ft:
                    ft.writelines(f'\n{dtsring},{" ".join(text_list)}')
            j=j+inst    
        image=cv2.imwrite('output_images/'+file, img)

    img_array = []
    for i in os.listdir('output_images'):
        img=Image.open('output_images'+'/'+i)
        img=np.array(img)
        img=cv2.resize(img,(224,224))
        img=cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)


    out = cv2.VideoWriter('project2.avi',cv2.VideoWriter_fourcc(*'DIVX'),1, size)
    
    for i in range(0,len(img_array)):
        out.write(img_array[i])
    out.release()
get_text('project.mp4',1)