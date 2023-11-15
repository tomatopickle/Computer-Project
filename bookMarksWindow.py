import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
import pywinstyles
import qdarktheme
import mysql.connector as sql


def showBookMarksWindow():
    qss = """
    QMenuBar *{font-size: 12pt;}
    QListWidget {font-size:10pt;}
    """

    sql_connection = sql.connect(
        host="localhost", user="root", passwd="mysqls", database="browser"
    )

    if sql_connection.is_connected:
        print("Connected to Server")

    qdarktheme.setup_theme(additional_qss=qss)

    window = QDialog()
    layout = QVBoxLayout()
    navbar = QMenuBar()
    listwidget = QListWidget()

    def clearbookMarks():
        cursor = sql_connection.cursor()
        cursor.execute("delete from bookmarks")
        sql_connection.commit()
        listwidget.clear()

    bookMarksLabel = QLabel("BookMarks", navbar)
    navbar.setCornerWidget(bookMarksLabel, Qt.TopLeftCorner)
    clearbookMarksButton = QPushButton("Clear BookMarks", navbar)
    navbar.setCornerWidget(clearbookMarksButton, Qt.TopRightCorner)
    clearbookMarksButton.clicked.connect(clearbookMarks)

    cursor = sql_connection.cursor()
    cursor.execute("select * from bookmarks order by time desc;")
    bookmarks = cursor.fetchall()

    i = 0
    for site in bookmarks:
        print(site)
        listwidget.insertItem(i, f"{site[1]}   {site[0]}")
        i += 1

    layout.addWidget(navbar)
    layout.addWidget(listwidget)
    window.resize(750, 500)
    window.setLayout(layout)

    pywinstyles.apply_style(window, "mica")
    return window
