import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
import qdarktheme
import pywinstyles

qss = """
QToolBar *{font-size: 12pt;}
"""

app = QApplication(sys.argv)
qdarktheme.setup_theme(additional_qss=qss)
browser = QWebEngineView()
browser.setUrl(QUrl("http://google.com"))
app.setApplicationName("Browser")
qdarktheme.setup_theme("auto")

main_window = QMainWindow()

# Navbar
navbar = QToolBar()


def navigate_home():
    browser.setUrl(QUrl("https://www.google.com"))


def navigate_to_url():
    url = url_bar.text()
    if "http" in url:
        browser.setUrl(QUrl(url))
    else:
        browser.setUrl(QUrl(f"https://www.google.com/search?q={url}"))


def loading_started():
    main_window.setWindowTitle("Browser: Loading")


def update_url(q):
    url_bar.setText(q.toString())


def update_title():
    main_window.setWindowTitle(f"Browser: {browser.title()}")


back_btn = QAction(
    QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowLeft)), "Back", browser
)
back_btn.triggered.connect(browser.back)
navbar.addAction(back_btn)

forward_btn = QAction(
    QIcon(QApplication.style().standardIcon(QStyle.SP_ArrowRight)), "Forward", browser
)
forward_btn.triggered.connect(browser.forward)
navbar.addAction(forward_btn)

reload_btn = QAction(
    QIcon(QApplication.style().standardIcon(QStyle.SP_BrowserReload)), "Reload", browser
)
reload_btn.triggered.connect(browser.reload)
navbar.addAction(reload_btn)

home_btn = QAction(
    QIcon(QApplication.style().standardIcon(QStyle.SP_DirHomeIcon)), "Home", browser
)
home_btn.triggered.connect(navigate_home)
navbar.addAction(home_btn)

url_bar = QLineEdit(browser)
url_bar.returnPressed.connect(navigate_to_url)
navbar.addWidget(url_bar)

browser.urlChanged.connect(update_url)
browser.urlChanged.connect(loading_started)
browser.titleChanged.connect(update_title)
browser.loadFinished.connect(update_title)
browser.setZoomFactor(1.3)

main_window.setCentralWidget(browser)
main_window.addToolBar(navbar)
main_window.showMaximized()

pywinstyles.apply_style(main_window,"mica")
pywinstyles.apply_style(browser,"mica")

sys.exit(app.exec_())
