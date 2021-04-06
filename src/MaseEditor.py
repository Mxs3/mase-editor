from tkinter import *
from tkinter import filedialog
import os, sys, select, subprocess
import serial.tools.list_ports

app = Tk()
app.resizable(True, True)
app.title("Mase Editor")
frameMain = Frame(app)
textArea = Text(app, width="125", height="40", bg="black", fg="lightgreen", insertbackground="white")

def getPorts():
    ports = serial.tools.list_ports.comports()
    return ports

def findPico(port_list):
    com_port = None
    connections = len(port_list)

    for _ in range(0, connections):
        port = port_list[_]
        strPort = str(port)

        if "Board" in strPort:
            split_port = strPort.split(" ")
            com_port = (split_port[0])

    return com_port

def connectPico():
    ports_found = getPorts()
    target_port = findPico(ports_found)

    if target_port != None:
        ser = serial.Serial(target_port, baudrate=115200, timeout=1)
        connected = StringVar()
        status = Label(app, textvariable=connected, relief=RAISED)
        connected.set("Connected to {}".format(str(ser.name)))
        status.pack(side=TOP)

    else:
        print("Connection Failed.")

def saveFile():
    file_path = filedialog.asksaveasfilename(initialdir = "/",
    title = "Save file as",filetypes = (("Python Files","*.py"),("All Files","*.*")))
    try:
        with open(file_path, "w") as file:
            contents = textArea.get("1.0", END)
            file.write(contents)
    except Exception:
        pass

def openFile():
    file_path = filedialog.askopenfilename(initialdir = "/",
    title = "Select file",filetypes = (("Python Files","*.py"),("All Files","*.*")))
    textArea.delete("1.0", END)
    filename = StringVar()
    file_label = Label(app, textvariable=filename, relief=RAISED)
    filename.set(str(os.path.basename(file_path)))
    file_label.pack(side=TOP)
    try:
        with open(file_path, "r") as file:
            contents = file.read()
            textArea.insert(INSERT, contents)
    except Exception:
        pass

def execute():
    contents = textArea.get("1.0", END)
    exec(contents)

def compile():
    file_path = filedialog.asksaveasfilename(initialdir = "/",
    title = "Select file",filetypes = (("ASM Files","*.asm"),("All Files","*.*")))
    try:
        with open(file_path, "w") as file:
            contents = textArea.get("1.0", END)
            file.write(contents)
    except Exception:
        pass

    try:
        os.system("nasm -f bin {} -o {}.bin".format(str(file_path), str(file_path)))
    except Exception as ex:
        print("You need to install nasm. {}".format(ex))
        pass

def initApp():
    menuBar = Frame(app)
    menuBar.pack(side=TOP, fill=X)
    app.config(menu=menuBar)
    savef= Button(menuBar, text="Save", command=saveFile)
    savef.pack(side=LEFT)
    openf = Button(menuBar, text="Open", command=openFile)
    openf.pack(side=LEFT)
    serial = Button(menuBar, text="Connect", command=connectPico)
    serial.pack(side=RIGHT)
    exect = Button(menuBar, text="Run", command=execute)
    exect.pack(side=RIGHT)
    compl = Button(menuBar, text="Compile", command=compile)
    compl.pack(side=RIGHT)
    frameMain.pack()
    textArea.pack(expand=True, fill="both")

def run():
    app.mainloop()

initApp()
run()