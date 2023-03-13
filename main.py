import os
from PyQt5.QtCore import QUrl, QObject, pyqtSlot, QVariant
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)

        # Set the geometry of the window to fill the entire screen
        self.showFullScreen()

        # Load the HTML file
        filepath = os.path.abspath('index.html')
        url = QUrl.fromLocalFile(filepath)
        self.webview.load(url)
        # Create the QWebChannel and expose the Python object to JavaScript
        self.channel = QWebChannel()
        self.obj = MyObject()
        self.channel.registerObject('handler', self.obj)
        self.webview.page().setWebChannel(self.channel)

class MyObject(QObject):
    
    @pyqtSlot(result=QVariant)
    def getUsbFileList(self):
        print('call received')
        return QVariant(['https://picsum.photos/id/237/300/300', 'https://picsum.photos/id/238/300/300',
        'https://picsum.photos/id/239/300/300', 'https://picsum.photos/id/242/300/300'])
    
    # take an argument from javascript - JS:  handler.test1('hello!')
    @pyqtSlot(QVariant, result=QVariant)
    def test1(self, args):
      print('i got')
      print(args)
      return "ok"

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
