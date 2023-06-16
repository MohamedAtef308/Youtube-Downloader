from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

app = QApplication([])
window = QWidget()

layout = QVBoxLayout()

button1 = QPushButton("Button 1")
layout.addWidget(button1)

button2 = QPushButton("Button 2")
layout.addWidget(button2)

window.setLayout(layout)
window.show()

app.exec_()