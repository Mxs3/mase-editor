from tkinter import *
from tkinter import filedialog
import os

app = Tk()
app.resizable(True, True)
app.title("Mase Editor")
frameMain = Frame(app)
textArea = Text(app, width="125", height="40", bg="black", fg="yellow", insertbackground="yellow")

def saveFile():
    filename = filedialog.asksaveasfilename(initialdir = "/",
    title = "Select file",filetypes = (("Python Files","*.py"),("All Files","*.*")))
    try:
        with open(filename, "w") as file:
            contents = textArea.get("1.0", END)
            file.write(contents)
    except Exception:
        pass

def openFile():
    filename = filedialog.askopenfilename(initialdir = "/",
    title = "Select file",filetypes = (("Python Files","*.py"),("All Files","*.*")))
    textArea.delete("1.0", END)
    try:
        with open(filename, "r") as file:
            contents = file.read()
            textArea.insert(INSERT, contents)
    except Exception:
        pass

def execute():
    contents = textArea.get("1.0", END)
    exec(contents)

def initApp():
    menuBar = Frame(app)
    menuBar.pack(side=TOP, fill=X)
    app.config(menu=menuBar)
    savef= Button(menuBar, text="Save", command=saveFile)
    savef.pack(side=LEFT)
    openf = Button(menuBar, text="Open", command=openFile)
    openf.pack(side=LEFT)
    exect = Button(menuBar, text="Run", command=execute)
    exect.pack(side=RIGHT)
    frameMain.pack()
    textArea.pack(expand=True, fill="both")

def run():
    app.mainloop()

initApp()
run()