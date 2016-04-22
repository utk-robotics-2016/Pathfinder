from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfilename
from PIL import Image, ImageTk
import cv2
import math
import json
import csv


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Application(Frame):
    def __init__(self, master=None):
        self.imageFilename = ""
        self.imageWidth = 0
        self.imageLength = 0
        self.waypoints = []
        self.root = master
        Frame.__init__(self, master)
        # width x height + x_offset + y_offset:
        self.root.geometry("175x400+30+30")
        self.createWidgets()

        self.opencv_image = None
        self.opencv_image_marked = None
        self.getting_theta = False
        self.first_click = True

    def createWidgets(self):
        self.widthLabel = Label(self.root, text="Course Width (in):")
        self.widthLabel.grid(row=0, column=1)
        self.widthEntry = Entry(self.root)
        self.widthEntry.grid(row=1, column=1)

        self.lengthLabel = Label(self.root, text="Course Length (in):")
        self.lengthLabel.grid(row=2, column=1)
        self.lengthEntry = Entry(self.root)
        self.lengthEntry.grid(row=3, column=1)

        self.open = Button(self.root, text="Open Image File", command=self.open)
        self.open.grid(row=4, column=1)
        self.openLabel = Label(self.root, text="")
        self.openLabel.grid(row=5, column=1)
        self.clearImage = Button(self.root, text="Clear Image", command=self.clearImage)
        self.clearImage.grid(row=6, column=1)

        self.saveWaypoints = Button(self.root, text="Save Waypoints", command=self.saveWaypoints)
        self.clearWaypoints = Button(self.root, text="Clear Waypoints", command=self.clearWaypoints)

        self.quit = Button(self.root, text="Quit", fg="red", command=self.quit)
        self.quit.grid(row=11, column=1)

        self.errorLabel = Label(self.root, fg="red", text="")
        self.errorLabel.grid(row=13, column=1)


        self.saveTheta = Button(self.root, text="Add Heading", command=self.saveTheta)
        self.thetaLabel = Label(self.root, text="Heading (degrees):")
        self.thetaEntry = Entry(self.root)

    def open(self):
        options = {
                'filetypes': [('JPEG', '.jpg'), ('PNG','.png')],
                'initialdir': '.',
                'parent': self.root
                }
        imageFilename = askopenfilename(**options)
        if(imageFilename != ""):
            dot = imageFilename.find(".")
            extension = imageFilename[dot:]
            if extension in ['.jpg', '.jpeg', '.png', '.tiff']:
                self.opencv_image = cv2.imread(imageFilename)
                cv2.putText(self.opencv_image, "X", (20, 15), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 255))
                cv2.line(self.opencv_image, (20, 20), (30, 20),  (0, 0, 255), 2)
                cv2.putText(self.opencv_image, "Y", (5, 30), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0))
                cv2.line(self.opencv_image, (20, 20), (20, 30),  (255, 0, 0), 2)
                self.opencv_image_marked = self.opencv_image.copy()
                self.setImage()
                imageFilename = imageFilename.rsplit('/', 1)[-1]
                self.openLabel['text'] = imageFilename

    def setImage(self):
        image = Image.fromarray(cv2.cvtColor(self.opencv_image_marked, cv2.COLOR_BGR2RGB))
        photoimage = ImageTk.PhotoImage(image)
        self.image = Label(self.root, image=photoimage)
        self.image.image = photoimage
        self.image.grid(row=0, column=0, rowspan=25)
        self.image.bind('<Button-1>', self.mouse_click)
        (self.imageWidth, self.imageLength) = image.size
        self.root.geometry("%dx%d+30+30" % (self.imageWidth + 175, self.imageLength))
        #self.moveWidgets(width+25)

    def clearImage(self):
        self.openLabel['text'] = ""
        self.image.destroy()
        self.root.geometry("175x400+30+30")
        self.saveWaypoints.grid_forget()
        self.clearWaypoints.grid_forget()
        #self.moveWidgets(25)

    def mouse_click(self, event):
        if self.first_click:
            self.first_click = False
            self.saveWaypoints.grid(row=8, column=1)
            self.clearWaypoints.grid(row=9, column=1)

        if not self.getting_theta:
            cv2.circle(self.opencv_image_marked, (event.x, event.y), 3, (0, 255, 0), 2)
            self.setImage()
            self.waypoints.append(dict({'x': float(event.x), 'y': float(event.y), 'theta': 0.0}))

            self.thetaLabel.grid(row=15, column=1)
            self.thetaEntry.grid(row=16, column=1)
            self.saveTheta.grid(row=17, column=1)

            self.getting_theta = True

    def saveTheta(self):
        theta = self.thetaEntry.get()
        if(is_number(theta)):
            self.thetaEntry['bg'] = "white"
            self.thetaEntry.delete(0, 'end')
            self.waypoints[len(self.waypoints)-1]['theta'] = float(theta)

            self.thetaLabel.grid_forget()
            self.thetaEntry.grid_forget()
            self.saveTheta.grid_forget()

            p1 = (int(self.waypoints[len(self.waypoints)-1]['x']), int(self.waypoints[len(self.waypoints)-1]['y']))
            line_length = 15
            p2 = (int(p1[0] + line_length * math.cos(math.radians(float(theta)))), int(p1[1] + line_length * math.sin(math.radians(float(theta)))))
            cv2.line(self.opencv_image_marked, p1, p2,  (0, 0, 255), 2)
            cv2.putText(self.opencv_image_marked, "%d" % len(self.waypoints), (p1[0], p1[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0))
            self.setImage()
            print "Waypoint #%d - x: %d y: %d theta: %d\n" % (len(self.waypoints), self.waypoints[len(self.waypoints)-1]['x'], self.waypoints[len(self.waypoints)-1]['y'], self.waypoints[len(self.waypoints)-1]['theta'])
            self.getting_theta = False
        else:
            self.errorLabel['text'] = "Heading must be a number"
            self.thetaEntry['bg'] = "red"

    def saveWaypoints(self):
        courseWidth = self.widthEntry.get()
        courseLength = self.lengthEntry.get()

        if not is_number(courseWidth) and not is_number(courseLength):
            self.errorLabel['text'] = "Course Width is not set\nCourse Length is not set"
            self.widthEntry['bg'] = "red"
            self.lengthEntry['bg'] = "red"
            return
        elif not is_number(courseWidth):
            self.errorLabel['text'] = "Course Width is not set"
            self.widthEntry['bg'] = "red"
            self.lengthEntry['bg'] = "white"
            return
        elif not is_number(courseLength):
            self.errorLabel['text'] = "Course Length is not set"
            self.lengthEntry['bg'] = "red"
            self.widthEntry['bg'] = "white"
            return
        else:
            self.errorLabel['text'] = ""
            self.lengthEntry['bg'] = "white"
            self.widthEntry['bg'] = "white"

        first_x = float(courseWidth) * self.waypoints[0]['x'] / float(self.imageWidth)
        first_y = float(courseLength) * self.waypoints[0]['y'] / float(self.imageLength)

        for i in range(len(self.waypoints)):
            self.waypoints[i]['x'] = float(courseWidth) * self.waypoints[i]['x'] / float(self.imageWidth) - first_x
            self.waypoints[i]['y'] = float(courseLength) * self.waypoints[i]['y'] / float(self.imageLength) - first_y

        options = {
                'defaultextension': '.csv',
                'filetypes': [('CSV', '.csv')],
                'initialfile': 'waypoints.csv',
                'initialdir': '.',
                'parent': self.root
                }

        filename = asksaveasfilename(**options)
        with open(filename, 'w') as csvfile:
            fieldnames = ['x', 'y', 'theta']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for waypoint in self.waypoints:
                writer.writerow({'x': waypoint['x'], 'y': waypoint['y'], 'theta': waypoint['theta']})

    def clearWaypoints(self):
        self.thetaEntry['bg'] = "white"
        self.thetaEntry.delete(0, 'end')
        self.waypoints = []
        self.opencv_image_marked = self.opencv_image.copy()
        self.setImage()
        self.first_click = True
        self.getting_theta = False
        self.saveWaypoints.grid_forget()
        self.clearWaypoints.grid_forget()
        self.thetaLabel.grid_forget()
        self.thetaEntry.grid_forget()
        self.saveTheta.grid_forget()

root = Tk()
root.title("Waypoint Generator")
app = Application(master=root)
app.mainloop()
root.destroy()
