from datetime import datetime
from PIL import Image,ImageDraw
from retinaface import RetinaFace

img_file1 = 'HIT.jpg'
img_file2 = 'IT_Fest.jpg'
img_file3 = 'Test.jpg'

start = datetime.now()

def retina(img_file):
    
    img = Image.open(img_file)
    draw= ImageDraw.Draw(img) 
    resp = RetinaFace.detect_faces(img_file)
    
    c=0
    for item in resp.items():
        top = item[1]['facial_area'][1]
        right = item[1]['facial_area'][2]
        bottom = item[1]['facial_area'][3]
        left = item[1]['facial_area'][0]
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        c+=1
    img.show()
    print ('counted ',c,' faces')

retina(img_file3)
#retina(img_file2)

end = datetime.now()
print (end-start)


