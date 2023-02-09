import os
import shutil
import tempfile
import tkinter as tk
from tkinter import END, filedialog
import tkinter.messagebox
from tkinter.ttk import Progressbar

def setPath():
    tempVal.configure(state="normal")
    tempVal.delete(0,END)
    tempVal.insert(END, "C:\Windows\Temp")
    tempVal.configure(state="disabled")

    temp2Val.configure(state="normal")
    temp2Val.delete(0,END)
    temp2Val.insert(END, tempfile.gettempdir())
    temp2Val.configure(state="disabled")

def cleanContent(folder):
    pb.stop()
    pb["value"] = 0
    counter = 0
    total = len(os.listdir(folder))
    for filename in os.listdir(folder):
        counter += 1
        try:
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            error = ["Failed to delete",file_path, e]
            output_list.insert(tk.END, error)

        pb["value"] = (counter / total) * 100
        pb.update()

def select_error(event):
    global selected_error
    index = output_list.curselection()[0]

    selected_error = output_list.get(index)
    tk.messagebox.showinfo(title="Error info", message=f"{selected_error[0]}\n{selected_error[1]}:\n{selected_error[2]}")

def run():
    output_list.delete(0, tk.END)
    cleanContent(tempVal.get())
    cleanContent(temp2Val.get())
    tk.messagebox.showinfo(title="Done!", message="Finish cleaning your cache")

app = tk.Tk()

tempFrame = tk.Frame(app)
tempFrame.pack(fill=tk.X, padx=5, pady=2.5)

tempFrame.columnconfigure(0)
tempFrame.columnconfigure(1, weight=1)

tempLabel = tk.Label(tempFrame, text="TEMP", justify="left", width=8)
tempVal = tk.Entry(tempFrame, disabledforeground="black", font=('bold', 11), state="disabled")
tempLabel.grid(row=0, column=0, sticky=tk.W+tk.E)
tempVal.grid(row=0, column=1, sticky=tk.W+tk.E)

# next line
temp2Frame = tk.Frame(app)
temp2Frame.pack(fill=tk.X, padx=5, pady=2.5)

temp2Frame.columnconfigure(0)
temp2Frame.columnconfigure(1, weight=1)

temp2Label = tk.Label(temp2Frame, text="%TEMP%", justify="left", width=8)
temp2Val = tk.Entry(temp2Frame, disabledforeground="black", font=('bold', 11), state="disabled")

temp2Label.grid(row=0, column=0, sticky=tk.W+tk.E)
temp2Val.grid(row=0, column=1, sticky=tk.W+tk.E)

runButton = tk.Button(app, text='Run Cleaner', bg="blue", foreground="white", command=run)
runButton.pack(fill=tk.X, padx=5, pady=2.5)

output_list = tk.Listbox(app, height=8, width=70)
output_list.pack(fill=tk.X, padx=5)
output_list.bind('<<ListboxSelect>>', select_error)

pb = Progressbar(app, orient='horizontal', mode='determinate', length=100)
pb.pack(fill=tk.X, padx=5, pady=2.5)

setPath()

app.title("Cache Cleaner")
# app.geometry('400x250')
app.mainloop()
