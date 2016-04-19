from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import math
import json

class RobotConfigDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        Label(top, text="Sample Count:").pack()
        self.sampleCountEntry = Entry(top)
        self.sampleCountEntry.pack()

        Label(top, text="Delta Time (ms):").pack()
        self.deltaTimeEntry = Entry(top)
        self.deltaTimeEntry.pack()

        Label(top, text="Max Velocity:").pack()
        self.maxVelocityEntry = Entry(top)
        self.maxVelocityEntry.pack()

        Label(top, text="Max Acceleration:").pack()
        self.maxAccelerationEnry = Entry(top)
        self.maxAccelerationEnry.pack()

        Label(top, text="Max Jerk:").pack()
        self.maxJerkEntry = Entry(top)
        self.maxJerkEntry.pack()

        Button(top, text="Save", command=self.save).pack()
        Button(top, text="Close", command=self.close).pack()

    def save(self):
        sampleCount = self.sampleCountEntry.get()
        deltaTime = self.deltaTimeEntry.get()
        maxVelocity = self.maxVelocityEntry.get()
        maxAcceleration = self.maxAccelerationEnry.get()
        maxJerk = self.maxJerkEntry.get()

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        if is_number(sampleCount) and is_number(deltaTime) and is_number(maxVelocity) and is_number(maxAcceleration) and is_number(maxJerk):
            output = dict()
            output['sample_count'] = sampleCount
            output['delta_time'] = deltaTime
            output['max_velocity'] = maxVelocity
            output['max_acceleration'] = maxAcceleration
            output['max_jerk'] = maxJerk
            f = open("pathfinder_config.json", "w")
            f.write(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

    def close(self):
        self.top.destroy()

class Application(Frame):
    def __init__(self, master=None):
        self.courseWidth = 0
        self.courseLength = 0
        self.imageFilename = ""
        self.waypoints = []
        self.root = master
        Frame.__init__(self, master)
        # width x height + x_offset + y_offset:
        self.root.geometry("175x400+30+30")
        self.createWidgets()

        self.opencv_image = None
        self.opencv_image_marked = None
        self.getting_theta = False

    def createWidgets(self):
        self.image = Label(self.root)
        self.image.grid(row=0, column=0)
        
        self.widthLabel = Label(self.root, text="Course Width (in):")
        self.widthLabel.grid(row=0, column=1)
        self.widthEntry = Entry(self.root)
        self.widthEntry.grid(row=1, column=1)
        
        self.lengthLabel = Label(self.root, text="Course Length (in):")
        self.lengthLabel.grid(row=2,column=1)
        self.lengthEntry = Entry(self.root)
        self.lengthEntry.grid(row=3,column=1)
        
        self.open = Button(self.root, text="Open Image File", command=self.open)
        self.open.grid(row=4,column=1)
        self.openLabel = Label(self.root, text="")
        self.openLabel.grid(row=5, column=1)
        self.clearImage = Button(self.root, text="Clear Image", command=self.clearImage)
        self.clearImage.grid(row=6, column=1)
        
        self.saveWaypoints = Button(self.root, text="Save Waypoints", command=self.saveWaypoints)
        self.saveWaypoints.grid(row=8, column=1)
        self.clearWaypoints = Button(self.root, text="Clear Waypoints", command=self.clearWaypoints)
        self.clearWaypoints.grid(row=9, column=1)
        

        self.quit = Button(self.root, text="Quit", fg="red", command=self.quit)
        self.quit.grid(row=11, column=1)

    def open(self):
        imageFilename = askopenfilename(parent=self.root)
        if(imageFilename != ""):
            dot = imageFilename.find(".")
            extension = imageFilename[dot:]
            if extension in ['.jpg', '.jpeg', '.png', '.tiff']:
                self.opencv_image = cv2.imread(imageFilename)
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
        (width, height) = image.size
        self.root.geometry("%dx%d+30+30" % (width + 175, height))
        #self.moveWidgets(width+25)

    def clearImage(self):
        self.openLabel['text'] = ""
        self.image.destroy()
        self.root.geometry("175x400+30+30")
        #self.moveWidgets(25)

    def mouse_click(self, event):
        if not self.getting_theta:
            cv2.circle(self.opencv_image_marked, (event.x, event.y), 3, (0, 255, 0), 2)
            self.setImage()
            self.waypoints.append(dict({'x': event.x, 'y': event.y, 'theta': 0.0}))
            height, width, channels = self.opencv_image_marked.shape

            if not hasattr(self, 'saveLabel'):
                self.saveTheta = Button(self.root, text="Save Heading", command=self.saveTheta)
                self.thetaLabel = Label(self.root, text="Heading (degrees):")
                self.thetaEntry = Entry(self.root)

            print self.saveTheta['command']

            self.thetaLabel.grid(row=15, column=1)
            self.thetaEntry.grid(row=16, column=1)
            self.saveTheta.grid(row=17, column=1)

            self.getting_theta = True

    def saveTheta(self):
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        theta = self.thetaEntry.get()
        if(is_number(theta)):
            self.waypoints[len(self.waypoints)-1]['theta'] = float(theta)

            self.thetaLabel.grid_forget()
            self.thetaEntry.grid_forget()
            self.saveTheta.grid_forget()

            p1 = (self.waypoints[len(self.waypoints)-1]['x'], self.waypoints[len(self.waypoints)-1]['y'])
            line_length = 15
            p2 = (int(p1[0] + line_length * math.cos(math.radians(float(theta)))), int(p1[1] + line_length * math.sin(math.radians(float(theta)))))
            cv2.line(self.opencv_image_marked, p1, p2,  (0, 0, 255), 2)
            cv2.putText(self.opencv_image_marked, "%d" % len(self.waypoints), (p1[0], p1[1] - 10), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0))
            self.setImage()
            print "Waypoint #%d - x: %d y: %d theta: %d\n" % (len(self.waypoints), self.waypoints[len(self.waypoints)-1]['x'], self.waypoints[len(self.waypoints)-1]['y'], self.waypoints[len(self.waypoints)-1]['theta'])
            self.getting_theta = False
        else:
            print "Heading must be a number"

    def saveWaypoints(self):
        f = open("pathfinder_waypoints.json", "w")
        f.write(json.dumps(self.waypoints, sort_keys=True, indent=4, separators=(',', ': ')))

    def clearWaypoints(self):
        self.waypoints = []
        self.opencv_image_marked = self.opencv_image.copy()
        self.setImage()
        if hasattr(self, 'thetaLabel'):
            self.thetaLabel.grid_forget()
            self.thetaEntry.grid_forget()
            self.saveTheta.grid_forget()



root = Tk()
root.title("Waypoint Generator")
d = RobotConfigDialog(root)
root.wait_window(d.top)
app = Application(master=root)
app.mainloop()
root.destroy()
