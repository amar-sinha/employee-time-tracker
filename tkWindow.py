from tkinter import *

class tkWindow():
    def __init__(self):
        self.root = Tk()
        
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()
        
         # get horizontal and vertical screen sizes
        positionHorizontal = int(self.root.winfo_screenwidth()/2 - windowWidth/2)
        positionVertical = int(self.root.winfo_screenheight()/2 - windowHeight/2)
        
        # position window in center of the screen
        self.root.geometry("+{}+{}".format(positionHorizontal, positionVertical))
        self.root.resizable(0, 0) # prevent window resizing

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()

    def close(self):
        self.root.destroy()