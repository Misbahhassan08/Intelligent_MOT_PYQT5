import sys
import cv2
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from onescreen import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.stream_thread = Stream_thread()
        self.browse_button.clicked.connect(self.browse)
        self.pause_button.clicked.connect(self.stream_thread.video_and_camera_Stop)
        self.play_button.clicked.connect(self.stream_select)
        self.close_button.clicked.connect(self.close)
        self.main_select = False
        pass   # end of MainWindow
        
    def browse(self):
        self.filename, _ = QFileDialog.getOpenFileName(self, "select mp4 file") 
        self.stream_thread.filename = self.filename
        self.stream_thread.select = True
        self.main_select = True
        pass    # end of browse button

    def stream_select(self):
        select_screens = self.comboBox.currentText()
        if select_screens == "You want to play video":
           if self.main_select:
              self.stream_thread.video_Start()
              self.stream_thread.change_pixmap.connect(self.screen_1.setPixmap)
              self.label.setText("Status : You are playing video")
           elif self.main_select == False:
                self.label.setText("Status : Please select video before play   !!!!!!!!!!!!!!")
        elif select_screens == "You want to play camera":
             self.stream_thread.camera_Start()
             self.stream_thread.change_pixmap.connect(self.screen_1.setPixmap)
             self.label.setText("Status : You are playing camera")
        self.stream_thread.start()


class Stream_thread(QtCore.QThread):
    change_pixmap = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.video_active = None
        self.camera_active = None
        self.frame_counter = 0
        self.thread_is_active = True 
        self.filename = None
        self.select = False
        pass   # end of Stream_thread  __init__ constructer
    def run(self):  
        cap2 = cv2.VideoCapture(0)    
        while self.thread_is_active:
              if self.select:
                 cap1 = cv2.VideoCapture(self.filename)
                 self.select = False
              if self.video_active:
                 self.frame_counter += 1
                 ret, frame = cap1.read()
                 if self.frame_counter == cap1.get(cv2.CAP_PROP_FRAME_COUNT):
                    self.frame_counter = 0 #Or whatever as long as it is the same as next line
                    cap1.set(cv2.CAP_PROP_POS_FRAMES, 0)
                 if ret:
                    width = 1800
                    height = 950
                    dsize = (width, height)
                    output = cv2.resize(frame, dsize, interpolation = cv2.INTER_AREA)
                    image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                    flipped_image = cv2.flip(image, 1)
                    qt_image = QtGui.QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0], QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(qt_image)
                    self.change_pixmap.emit(pixmap)
              elif self.camera_active:
                   ret, frame = cap2.read()              
                   if ret:
                      width = 1800
                      height = 950
                      dsize = (width, height)
                      output = cv2.resize(frame, dsize, interpolation = cv2.INTER_AREA)
                      image = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                      flipped_image = cv2.flip(image, 1)
                      qt_image = QtGui.QImage(flipped_image.data, flipped_image.shape[1], flipped_image.shape[0], QtGui.QImage.Format_RGB888)
                      pixmap = QtGui.QPixmap.fromImage(qt_image)
                      self.change_pixmap.emit(pixmap)
    def stop(self):
        self.thread_is_active = False
        self.quit()
        # end of stop function
    def video_Start(self):
        self.video_active = True
        self.camera_active = False
        pass    # end of video_Start
    def camera_Start(self):
        self.camera_active = True
        self.video_active = False
        pass    # end of camera_Start
    def video_and_camera_Stop(self):
        self.camera_active = False
        self.video_active = False
        pass    # end of video_and_camera_Stop
         
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = MainWindow()
    controller.showFullScreen()
    sys.exit(app.exec_())
    pass  # end of main()
if __name__ == "__main__":
    import sys
    main()
    pass   # end of if __name__