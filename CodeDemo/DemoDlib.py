
from datetime import datetime
from PIL import Image,ImageDraw

img_file1 = 'HIT.jpg'
img_file2 = 'IT_Fest.jpg'
img_file3 = 'Test.jpg'

start = datetime.now()

def face_reco(img_file):
    import face_recognition
    img = Image.open(img_file)
    draw= ImageDraw.Draw(img)
    # Tải file ảnh và chuyển đổi nó thành mảng NumPy
    image = face_recognition.load_image_file(img_file)
    # Tìm vị trí khuôn mặt trong 1 bức ảnh
    image_locations= face_recognition.face_locations(image)
    # Mã hóa các khuôn mặt được tìm thấy trong ảnh thành các vector đặc trưng
    image_encoding= face_recognition.face_encodings(image, image_locations)
    # Vòng lặp dử dụng để duyệt qua danh sách các vị trí khuôn mặt và vector đặc trưng tương ứng trong ảnh
    c = 0
    for (top, right, bottom, left), face_encoding in zip(image_locations, image_encoding):
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        c+=1

    img.show()
    print ('counted ',c,' faces')

face_reco(img_file3)

end = datetime.now()
print (end-start)

