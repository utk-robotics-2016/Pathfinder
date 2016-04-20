from Tkinter import *
from tkFileDialog import asksaveasfilename
import json

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Application(Frame):
    def __init__(self, master=None):
        self.root = master
        Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        Label(self.root, text="Sample Count:").pack()
        self.sampleCountEntry = Entry(self.root)
        self.sampleCountEntry.pack()

        Label(self.root, text="Delta Time (s):").pack()
        self.deltaTimeEntry = Entry(self.root)
        self.deltaTimeEntry.pack()

        Label(self.root, text="Max Velocity (in/s):").pack()
        self.maxVelocityEntry = Entry(self.root)
        self.maxVelocityEntry.pack()

        Label(self.root, text="Max Acceleration (in/s^2):").pack()
        self.maxAccelerationEnry = Entry(self.root)
        self.maxAccelerationEnry.pack()

        Label(self.root, text="Max Jerk (in/s^3):").pack()
        self.maxJerkEntry = Entry(self.root)
        self.maxJerkEntry.pack()

        Label(self.root, text="Drivetrain").pack()
        self.drivetrainOption = StringVar(self.root)
        self.drivetrainOption.set("Tank")
        self.drivetrainEntry = OptionMenu(self.root, self.drivetrainOption, "Tank", "Swerve")
        self.drivetrainEntry.pack()

        Label(self.root, text="Wheelbase Width (in):").pack()
        self.wheelbaseWidthEntry = Entry(self.root)
        self.wheelbaseWidthEntry.pack()

        Label(self.root, text="Wheelbase Length (in):").pack()
        self.wheelbaseLengthEntry = Entry(self.root)
        self.wheelbaseLengthEntry.pack()

        self.errorLabel = Label(self.root, fg='red', text="")
        self.errorLabel.pack()

        Button(self.root, text="Save", command=self.save).pack()
        Button(self.root, text="Quit", command=self.quit).pack()

    def save(self):
        sampleCount = self.sampleCountEntry.get()
        deltaTime = self.deltaTimeEntry.get()
        maxVelocity = self.maxVelocityEntry.get()
        maxAcceleration = self.maxAccelerationEnry.get()
        maxJerk = self.maxJerkEntry.get()
        drivetrain = self.drivetrainOption.get()
        wheelbaseWidth = self.wheelbaseWidthEntry.get()
        wheelbaseLength = self.wheelbaseLengthEntry.get()

        error = False
        errorMessage = ""
        if not is_number(sampleCount):
            error = True
            errorMessage = "Sample Count needs to have a number\n"
            self.sampleCountEntry['bg'] = 'red'
        else:
            self.sampleCountEntry['bg'] = 'white'

        if not is_number(deltaTime):
            error = True
            errorMessage = errorMessage + "Delta Time needs to have a number\n"
            self.deltaTimeEntry['bg'] = 'red'
        else:
            self.deltaTimeEntry['bg'] = 'white'

        if not is_number(maxVelocity):
            error = True
            errorMessage = errorMessage + "Max Velocity Count needs to have a number\n"
            self.maxVelocityEntry['bg'] = 'red'
        else:
            self.maxVelocityEntry['bg'] = 'white'

        if not is_number(maxAcceleration):
            error = True
            errorMessage = errorMessage + "Max Acceleration needs to have a number\n"
            self.maxAccelerationEnry['bg'] = 'red'
        else:
            self.maxAccelerationEnry['bg'] = 'white'

        if not is_number(maxJerk):
            error = True
            errorMessage = errorMessage + "Max Jerk needs to have a number\n"
            self.maxJerkEntry['bg'] = 'red'
        else:
            self.maxJerkEntry['bg'] = 'white'

        if not is_number(wheelbaseWidth):
            error = True
            errorMessage = errorMessage + "Wheelbase Width needs to have a number\n"
            self.wheelbaseWidthEntry['bg'] = 'red'
        else:
            self.wheelbaseWidthEntry['bg'] = 'white'

        if not is_number(wheelbaseLength):
            error = True
            errorMessage = errorMessage + "Wheelbase Length needs to have a number\n"
            self.wheelbaseLengthEntry['bg'] = 'red'
        else:
            self.wheelbaseLengthEntry['bg'] = 'white'

        if error:
            self.errorLabel['text'] = errorMessage
            return

        output = dict()
        output['sample_count'] = float(sampleCount)
        output['delta_time'] = float(deltaTime)
        output['max_velocity'] = float(maxVelocity)
        output['max_acceleration'] = float(maxAcceleration)
        output['max_jerk'] = float(maxJerk)
        output['drivetrain'] = drivetrain
        output['wheelbase_width'] = float(wheelbaseWidth)
        output['wheelbase_length'] = float(wheelbaseLength)

        options = {
            'defaultextension': '.json',
            'filetypes': [('json files', '.json')],
            'initialfile': 'pathplanning_robot_config.json',
            'initialdir': '.',
            'parent': self.root
            }
        filename = asksaveasfilename(**options)
        f = open(filename, "w")
        f.write(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))

root = Tk()
root.title("Config Generator")
app = Application(master=root)
app.mainloop()
root.destroy()
