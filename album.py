import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
Config.set('graphics', 'resizable', '0')
Config.write()
class mainWidget(Widget):

    def __init__(self, **kwargs):
        super(mainWidget, self).__init__(**kwargs)
        Window.size = (1024, 640)
        self.img_num = 0
        self.images = images
        self.gl = GridLayout(cols = 3, rows = 1)
        self.gl.size = [Window.size[0], Window.size[1]]
        img_count = len(self.images)
        self.img = Image(source = self.images[self.img_num])
        previos_button = Button(text = 'Назад', on_press = self.prev, size_hint_x=.12, width=Window.size[0] )
        next_button = Button(text = 'Вперед', on_press = self.next, size_hint_x=.12, width=Window.size[0] )

        self.gl.add_widget(previos_button)
        self.gl.add_widget(self.img)
        self.gl.add_widget(next_button)
        self.add_widget(self.gl)
        print(self.images)

    def prev(self, btn):
        self.add_image(self.img_num-1)

    def next(self, btn):
        self.add_image(self.img_num + 1)

    def add_image(self, num):
        count = len(self.images)
        if num >= count:
            num = 0
        if num < 0:
            num = count-1
        self.img.source = images[num]
        print(self.images[num])
        self.img_num = num




class mainApp(App):
    def build(self):
        root = Widget()
        root.add_widget(mainWidget())
        return root

images = []
directory = (os.path.dirname(os.path.realpath(__file__)))
f = os.listdir(directory)
for file in f:
    filename, file_extension = os.path.splitext(file)
    if file_extension == '.jpg' or file_extension == '.img':
        images.append(filename + file_extension)

if __name__ == '__main__':
    mainApp().run()