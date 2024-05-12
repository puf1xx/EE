import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog, QApplication, QWidget, QButtonGroup, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QLineEdit, QTextEdit, QListWidget, QFileDialog
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtGui import QPixmap
app = QApplication([])
win = QWidget()

win.setWindowTitle('Easy Editor')
btn_dir = QPushButton('Папка')
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
rez = QPushButton('Резкость')
bw = QPushButton('Ч/Б')
list_widget = QListWidget()
paint = QLabel('Картинка')

win.resize(700, 400)
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()


col1.addWidget(btn_dir)
col1.addWidget(list_widget)


row_tools = QHBoxLayout()
row_tools.addWidget(left)
row_tools.addWidget(right)
row_tools.addWidget(mirror)
row_tools.addWidget(rez)
row_tools.addWidget(bw)

col2.addWidget(paint)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)
#win.setLayout(row_tools)
#win.setLayout(col1)
#win.setLayout(col2)
win.show()

workdir = ''

def chooseWorkdir():
    global workdir 
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for i in files:
        for g in extensions:
            if i.endswith(g):
                result.append(i)
#    return(result) - а-я-яй
    return result

def showFilenamesList():
    extensions = ['.bmp', '.jpg', '.png', '.gif', '.jpeg']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_widget.clear()
    for j in filenames:
        list_widget.addItem(j)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = "Modified/"
    def loadImage(self, workdir, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        paint.hide()
        pixmapimage = QPixmap(path)
        w, h = paint.width(), paint.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        paint.setPixmap(pixmapimage)
        paint.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def l(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def r(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def rezk(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)




workimage = ImageProcessor()

def showChosenImage():
    if list_widget.currentRow() >= 0:
        filename = list_widget.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)
    

list_widget.currentRowChanged.connect(showChosenImage)
bw.clicked.connect(workimage.do_bw)
mirror.clicked.connect(workimage.flip)
left.clicked.connect(workimage.l)
right.clicked.connect(workimage.r)
rez.clicked.connect(workimage.rezk)
app.exec()
