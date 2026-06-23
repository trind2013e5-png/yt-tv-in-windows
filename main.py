import sys
import os
from PyQt5.QtCore import QUrl, QEvent, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEngineScript
)
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

# 🛡️ PATCH 3: URL Navigation Policy - Chặn đứng các trang web độc hại
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

# Lớp trình duyệt vô hiệu hóa menu chuột phải
class CustomWebView(QWebEngineView):
    def contextMenuEvent(self, event):
        pass

# Lớp chặn tương tác chuột trái
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
        
        # 📺 USER AGENT: Sony Bravia 4K Android TV (Chuẩn, không dính lỗi Cast)
        self.user_agent = (
            "Mozilla/5.0 (Linux; aarch64; Android 11; BRAVIA 4K VH21 Build/RBT1.210323.011) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 SMART-TV"
        )
        self.profile.setHttpUserAgent(self.user_agent)

        # 🚀 ANTI-DETECT PRO JAVASCRIPT INJECTION: Giả mạo phần cứng toàn diện
        stealth_script = QWebEngineScript()
        stealth_script.setSourceCode("""
            // 1. Ẩn cờ tự động hóa (Webdriver)
            Object.defineProperty(navigator, 'webdriver', {get: () => false});
            
            // 2. Đổi nền tảng thành chip ARM của TV
            Object.defineProperty(navigator, 'platform', {get: () => 'Linux armv8l'});
            
            // 3. Giả lập RAM 4GB và CPU 8 nhân
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 4});
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 8});
            
            // 4. Giả mạo GPU (WebGL) thành chip đồ họa của TV thay vì Card màn hình PC
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'ARM'; // UNMASKED_VENDOR_WEBGL
                }
                if (parameter === 37446) {
                    return 'Mali-G71'; // UNMASKED_RENDERER_WEBGL
                }
                return getParameter.call(this, parameter);
            };
            
            // 5. Qua mặt User-Agent Client Hints (API phát hiện trình duyệt mới của Google)
            if (navigator.userAgentData) {
                Object.defineProperty(navigator.userAgentData, 'platform', {get: () => 'Android'});
                Object.defineProperty(navigator.userAgentData, 'mobile', {get: () => false});
            }
        """)
        stealth_script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        stealth_script.setWorldId(QWebEngineScript.MainWorld)
        self.profile.scripts().insert(stealth_script)

        # Kích hoạt bộ chặn bảo mật URL
        self.security_interceptor = SecurityInterceptor()
        self.profile.setRequestInterceptor(self.security_interceptor)

        # Tối ưu đồ họa và bật DRM (Widevine) để phân giải cao nhất
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True) 
        
        # 🛡️ PATCH 1: Khóa chặt lỗ hổng RCE từ file cục bộ
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)

        # Khởi tạo trình duyệt
        self.browser = CustomWebView()
        self.browser.setUrl(QUrl('https://www.youtube.com/tv'))

        # Lọc sự kiện click chuột
        self.filter = ClickFilter()
        self.browser.focusProxy().installEventFilter(self.filter)

        self.setCentralWidget(self.browser)
        self.setWindowTitle("YouTube Smart TV Client (Ultimate Anti-Detect Mode)")
        self.showMaximized()

if __name__ == "__main__":
    # 🛡️ PATCH 2: Kích hoạt Security Sandbox
    if getattr(sys, 'frozen', False):
        os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "0"
    
    app = QApplication(sys.argv)
    window = SmartTVBrowser()
    sys.exit(app.exec_())
