import sys
import subprocess
def install_dependencies():
 try:
 import PyQt5
 import PyQt5.QtWebEngineWidgets
 except ImportError:
 subprocess.check_call([sys.executable, "-m", "pip", "install", "PyQt5", "PyQtWebEngine"])

install_dependencies()
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
class CustomWebView(QWebEngineView):
 def contextMenuEvent(self, event):
 pass

class ClickFilter(QObject):
 def eventFilter(self, obj, event):
 if event.type() == QEvent.MouseButtonPress:
 if event.button() == Qt.LeftButton:
 return True
 return False

class SmartTVBrowser(QMainWindow):
 def __init__(self):
 super(SmartTVBrowser, self).__init__()
 self.user_agent = "Mozilla/5.0 (SMART-TV; Linux; Tizen 5.0) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.2 Chrome/63.0.3239.84 TV Safari/537.36"
 self.profile = QWebEngineProfile.defaultProfile()
 self.profile.setHttpUserAgent(self.user_agent)
 self.browser = CustomWebView()
 self.browser.setUrl(QUrl('https://www.youtube.com/tv')) 
 self.filter = ClickFilter()
 self.browser.focusProxy().installEventFilter(self.filter)

 self.setCentralWidget(self.browser)
 self.setWindowTitle("Smart TV")
 self.showMaximized()

if __name__ == "__main__":
 app = QApplication(sys.argv)
 window = SmartTVBrowser()
 sys.exit(app.exec_())
