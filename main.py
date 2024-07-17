from breezypythongui import EasyFrame

class Window1(EasyFrame):
    def __init__ (self):
        #initializes the first window
        EasyFrame.__init__ (self, width= 400, height= 400, title = "Pizza Palace Ordering", resizable= False)
        EasyFrame.addCanvas(background = "pizza_bg.jpg")
        self.Heading = self.addLabel(text= "Welcome to the Pizza Palace!", row = 0, column = 2, columnspan = 2)
class Window2(EasyFrame):
    def __init__ (self):
        #initializes the second window, though it is not created until needed.
        EasyFrame.__init__(self, title = "Temp Title", height = 400, width= 400, resizable= False) 
def main ():
    Window1().mainLoop()

if __name__== "__main__":
    main()