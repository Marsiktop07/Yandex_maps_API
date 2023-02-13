import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
import requests


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.map_zoom = 3
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }
        response = requests.get(self.api_server, params=map_params)
        if not response:
            print(f"""Ошибка выполнения запроса:
            Http статус: {response.status_code} ({response.reason})""")

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.label.setPixmap(pixmap)



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())