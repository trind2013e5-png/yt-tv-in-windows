import sys
import os
from PyQt5.QtCore import QUrl, QEvent, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEngineScript
)
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# 🛡️ PATCH 3: URL Navigation Policy
class SecurityInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self):
        super().__init__()
        self.allowed_domains = [
            'youtube.com', 'www.youtube.com', 'googlevideo.com',
            'ytimg.com', 'google.com', 'gstatic.com', 'ggpht.com'
        ]
    
    def interceptRequest(self, info):
        url = info.requestUrl()
        host = url.host()
        if not any(host.endswith(domain) for domain in self.allowed_domains):
            info.block(True)
            return
        info.block(False)

class CustomWebView(QWebEngineView):
    def contextMenuEvent(self, event):
        pass  # Vô hiệu hóa menu chuột phải

class ClickFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                return True
        return False

class SmartTVBrowser(QMainWindow):
    def __init__(self):
        super(SmartTVBrowser, self).__init__()

        self.profile = QWebEngineProfile.defaultProfile()
        
        # 📺 USER AGENT: Chromecast with Google TV (Mới, chuẩn Google, ít bị nghi ngờ nhất)
        self.user_agent = (
            "Mozilla/5.0 (Linux; Android 12; Chromecast with Google TV Build/STTE.220621.019.A2; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 "
            "CrKey/1.66.332856"
        )
        self.profile.setHttpUserAgent(self.user_agent)

        # 🚀 ANTI-DETECT JAVASCRIPT INJECTION: Xóa dấu vết PC, giả mạo thông số phần cứng
        # Đoạn script này chạy trước khi YouTube kịp load để lừa hệ thống kiểm tra
        stealth_script = QWebEngineScript()
        stealth_script.setSourceCode("""
            // Ẩn cờ tự động hóa (Webdriver)
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            // Đổi nền tảng thành chip ARM của TV thay vì Win32/x86
            Object.defineProperty(navigator, 'platform', {get: () => 'Linux armv8l'});
            // Giả lập RAM 4GB và CPU 8 nhân của TV Box cao cấp
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 4});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            // Chặn báo cáo ngôn ngữ thực tế của máy tính nếu cần
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        """)
        stealth_script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        stealth_script.setWorldId(QWebEngineScript.MainWorld)
        self.profile.scripts().insert(stealth_script)

        self.security_interceptor = SecurityInterceptor()
        self.profile.setRequestInterceptor(self.security_interceptor)

        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        # Bật Plugins để hỗ trợ Widevine DRM (Giúp giải mã video 1080p/4K bản quyền nếu có)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True) 
        
        # 🛡️ PATCH 1: RCE Protection
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)

        self.browser = CustomWebView()
        self.browser.setUrl(QUrl('https://www.youtube.com/tv'))

        self.filter = ClickFilter()
        self.browser.focusProxy().installEventFilter(self.filter)

        self.setCentralWidget(self.browser)
        self.setWindowTitle("YouTube Smart TV Client (Anti-Detect Mode)")
        self.showMaximized()

if __name__ == "__main__":
    # 🛡️ PATCH 2: Security Sandbox
    if getattr(sys, 'frozen', False):
        os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "0"
    
    app = QApplication(sys.argv)
    window = SmartTVBrowser()
    sys.exit(app.exec_())
