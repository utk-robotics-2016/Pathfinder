import argparse
from Tkinter import *
from tkFileDialog import askopenfilename
import sys

courseWidth = 0
courseLength = 0
imageFilename = ""

class DimensionDialog:

    def __init__(self, parent):

        self.parent = parent

        top = self.top = Toplevel(parent)

        self.widthLabel = Label(top, text="Course Width (in):")
        self.widthLabel.pack(padx=5, pady=5)
        self.widthEntry = Entry(top)
        self.widthEntry.pack(padx=5, pady=5)

        self.lengthLabel = Label(top, text="Course Length (in):")
        self.lengthLabel.pack(padx=5, pady=5)
        self.lengthEntry = Entry(top)
        self.lengthEntry.pack(padx=5, pady=5)

        self.open = Button(top, text="Open Image File", command=self.open)
        self.open.pack(padx=5, pady=5)

        self.openLabel = Label(top, text="")
        self.openLabel.pack(padx=5, pady=5)

        self.save = Button(top, text="Save", command=self.save)
        self.save.pack(padx=5, pady=5)

    def open(self):
        global imageFilename
        imageFilename = askopenfilename(parent=self.parent)
        self.openLabel['text'] = imageFilename

    def save(self):
        global courseWidth, courseLength
        courseWidth = self.widthEntry.get()
        print "Course width (in):", courseWidth
        courseLength = self.lengthEntry.get()
        print "Course length (in):", courseLength
        self.top.destroy()

class Application(Frame):
    def setBackgroundImage(self, filename):
        self.waypoints = []

    def clear(self):
        self.waypoints = []

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "right"})

        self.CLEAR = Button(self)
        self.CLEAR["text"] = "Clear",
        self.CLEAR["command"] = self.clear

        self.CLEAR.pack({"side": "right"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        img = ImageTk.PhotoImage(Image.open(image_file))
        panel = tk.Label(root, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.pack()
        self.createWidgets()

root = Tk()
root.title("Waypoint Generator")
d = DimensionDialog(root)
root.wait_window(d.top)
app = Application( master=root)
app.mainloop()
root.destroy()