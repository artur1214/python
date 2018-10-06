import osmanager
import tags
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import time
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import Qt


class StartWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.loadUI()
        self.currentPhoto = None


    def writeTags(self, file):
        tags.readTags(file)


    def openFolder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self)
        start_time = time.time()
        files = osmanager.checkPath(folder)
        for f in files:
            if not f:
                print('пусто')
            else:
                print(f)
        print("--- %s seconds ---" % (time.time() - start_time))


    def openFile(self):
        try:
            filepath = QtWidgets.QFileDialog.getOpenFileName(self)[0]
            ph = self.smallPhoto
            pxmap = QtGui.QPixmap(filepath)
            pxmap = pxmap.scaled(ph.width(), ph.height(), aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            ph.setPixmap(pxmap)
            tag = tags.readTags(filepath)
            if tag is None:
                self.currentTagsLabel.setText('')
                self.tagsEdit.setText('')
            else:
                self.currentTagsLabel.setText(" ".join(str(x) for x in tag))
                self.tagsEdit.setText(" ".join(str(x) for x in tag))
            self.currentPhoto = filepath
        except Exception as e:
            print(e)


    def loadUI(self):
        uic.loadUi('main.ui', self)
        self.fileOpenAction.triggered.connect(self.openFile)
        self.saveTagsButton.clicked.connect(self.saveTagsHandler)
        self.tagsDeleteButton.clicked.connect(self.tagsDeleteHandler)

    def updateUI(self):
        tag = tags.readTags(self.currentPhoto)
        if tag is None:
            self.currentTagsLabel.setText('')
            self.tagsEdit.setText('')
        else:
            self.currentTagsLabel.setText(" ".join(str(x) for x in tag))
            self.tagsEdit.setText(" ".join(str(x) for x in tag))

    def saveTagsHandler(self):
        try:
            tag = self.tagsEdit.toPlainText()
            print(tag)
            tags.removeTags(self.currentPhoto)
            tags.addTags(self.currentPhoto, tag)
            self.updateUI()
        except Exception as e:
            print(e)


    def tagsDeleteHandler(self):
        try:
            tags.removeTags(self.currentPhoto)
            self.updateUI()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = StartWindow()
    window.setWindowTitle('TagManager 0.1')
    #window.setFixedSize(window.width(), window.height())
    window.show()

    sys.exit(app.exec_())
