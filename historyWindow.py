import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
import pywinstyles
import qdarktheme
import mysql.connector as sql


def showHistoryWindow():
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

    def clearHistory():
        cursor = sql_connection.cursor()
        cursor.execute("delete from history")
        sql_connection.commit()
        listwidget.clear()
    
    historyLabel = QLabel("History", navbar)
    navbar.setCornerWidget(historyLabel, Qt.TopLeftCorner)
    clearHistoryButton = QPushButton("Clear History", navbar)
    navbar.setCornerWidget(clearHistoryButton, Qt.TopRightCorner)
    clearHistoryButton.clicked.connect(clearHistory)
    
    cursor = sql_connection.cursor()
    cursor.execute("select * from history order by time desc;")
    history = cursor.fetchall()

    i = 0
    for site in history:
        print(site)
        listwidget.insertItem(i, f"{site[0]}   {site[1]}")
        i += 1

    layout.addWidget(navbar)
    layout.addWidget(listwidget)
    window.resize(750, 500)
    window.setLayout(layout)

    pywinstyles.apply_style(window, "mica")
    return window
