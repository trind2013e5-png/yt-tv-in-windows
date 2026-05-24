import sys
import os

# --- CHƯƠNG TRÌNH CHÍNH ---
from PyQt5.QtCore import QUrl, QEvent, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings

# Lớp trình duyệt tùy chỉnh để chặn menu chuột phải
class CustomWebView(QWebEngineView):
    def contextMenuEvent(self, event):
        pass # Vô hiệu hóa menu chuột phải

# Lớp chặn chuột trái
class ClickFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                return True
        return False

class SmartTVBrowser(QMainWindow):
    def __init__(self):
        super(SmartTVBrowser, self).__init__()

        # Tối ưu cấu hình WebEngine để tăng hiệu năng và chất lượng video
        self.profile = QWebEngineProfile.defaultProfile()
        
        # Cập nhật User-Agent Smart TV đời mới để mở khóa 1080p/4K
        self.user_agent = "Mozilla/5.0 (LG Smart TV; OS LinuX; WebOS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 LG Browser/8.00.00(TAV;1.0.0)"
        self.profile.setHttpUserAgent(self.user_agent)

        # Bật các tính năng tăng tốc phần cứng và phát video chất lượng cao
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

        # Khởi tạo trình duyệt
        self.browser = CustomWebView()
        self.browser.setUrl(QUrl('https://www.youtube.com/tv')) 
        
        # Chặn chuột trái
        self.filter = ClickFilter()
        self.browser.focusProxy().installEventFilter(self.filter)

        # Đưa vào giao diện chính
        self.setCentralWidget(self.browser)
        self.setWindowTitle("YouTube Smart TV Client")
        self.showMaximized()

if __name__ == "__main__":
    # Đảm bảo tắt tính năng giải nén gây lỗi mã hóa của PyQt5 nếu chạy onefile
    os.environ["QT_ANARCHY"] = "1" 
    
    app = QApplication(sys.argv)
    window = SmartTVBrowser()
    sys.exit(app.exec_())
