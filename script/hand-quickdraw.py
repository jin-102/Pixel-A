import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras import layers
from keras.models import load_model
import cv2


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.image = QImage(QSize(400, 400), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 20
        self.brush_color = Qt.black
        self.last_point = QPoint()
        self.loaded_model = None
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('File')

        load_model_action = QAction('Load model', self)
        load_model_action.setShortcut('Ctrl+L')
        load_model_action.triggered.connect(self.load_model)
  
        clear_action = QAction('Clear', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)

        filemenu.addAction(load_model_action)
        #filemenu.addAction(save_action)
        filemenu.addAction(clear_action)

        self.statusbar = self.statusBar()

        self.setWindowTitle('QuickDraw 인식입니다')
        self.setGeometry(300, 300, 400, 400)
        self.statusbar.showMessage('File 버튼을 눌러 모델을 Load해주세요')
        self.show()

    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = e.pos()

    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:

            self.drawing = False
            
            arr = np.empty([0,28*28])
            arr_test = np.empty([0,28,28])
            self.image.save('temp_img_save.png','PNG',-1)

            loaded_test_img = cv2.imread('temp_img_save.png',cv2.IMREAD_GRAYSCALE)
            ret, loaded_test_img = cv2.threshold(loaded_test_img, 250, 255, cv2.THRESH_BINARY_INV)
            height, width = loaded_test_img.shape[:2]     # 읽어들이 이미지의 사이즈 확인
            if (width*height) != 784:     #만일 사이즈가 28 * 28 이 아니라면
                loaded_test_img = cv2.resize(loaded_test_img, dsize=(28, 28), interpolation = cv2.INTER_AREA)
            loaded_test_img = loaded_test_img.reshape(1,784)    # array reshape
            arr = np.concatenate((arr, loaded_test_img), axis=0)

            loaded_test_img = None

            arr = 255 - np.reshape(arr,(1, 28,28))
            arr_test = arr[0:1,:]
            arr_test = arr_test.reshape(1,28,28,1).astype('float32')
            arr_test /= 255.0

            if self.loaded_model:
                pred = np.argmax(self.loaded_model.predict(arr_test),axis=1)
                class_names = ['cloud', 'sun', 'pants', 'umbrella', 'table', 'ladder', 'eyeglasses', 'clock', 'scissors', 'cup','apple','pizza','eye','frog','flower','hand','foot','donut','elephant','bicycle','candle','chair','face','fish','tree']  #원하는 클래스 정의
                
                pred_class = class_names[pred[0]]
                
                self.statusbar.showMessage('이 그림은 ' + pred_class + '입니다.')

    def load_model(self):
        from keras.models import load_model
        fname, _ = QFileDialog.getOpenFileName(self, 'Load Model', '')
        #fname = 'quickdrawmodel.h5'

        if fname:
            self.loaded_model = tf.keras.models.load_model(fname)
            self.statusbar.showMessage('Model loaded.')

    def clear(self):
        self.image.fill(Qt.white)
        self.update()
        self.statusbar.clearMessage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
