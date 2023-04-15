
import matplotlib.pyplot as plt
from datetime import datetime
import cv2
from mtcnn import MTCNN

start = datetime.now()

# Load ảnh
img = cv2.imread("Test.jpg")
# Khởi tạo bộ nhận diện MTCNN
detector = MTCNN()
# Phát hiện khuôn mặt trong ảnh
faces = detector.detect_faces(img)
# Vẽ bounding box xung quanh các khuôn mặt được phát hiện
for face in faces:
    x, y, width, height = face['box']
    cv2.rectangle(img, (x, y), (x+width, y+height), (0, 255, 0), 2)

# Hiển thị ảnh với các khuôn mặt được phát hiện
end = datetime.now()
print (end-start)

plt.imshow(img,cmap='gray')
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()



