import tkinter as tk
from tkinter import ttk
import pickle

scheduleFile = "schedule.pkl"
daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def loadSchedule():
    try:
        with open(scheduleFile, 'rb') as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return {}

def saveSchedule(scheduleData):
    with open(scheduleFile, 'wb') as file:
        pickle.dump(scheduleData, file)

def addToSchedule(day, timeSlot, task):
    schedule = loadSchedule()
    key = (day, timeSlot)
    schedule[key] = task
    saveSchedule(schedule)
    displaySchedule()

def removeFromSchedule(day, timeSlot):
    schedule = loadSchedule()
    key = (day, timeSlot)
    if key in schedule:
        del schedule[key]
    saveSchedule(schedule)
    displaySchedule()

def gridButtonClick(day, timeSlot):
    dayVar.set(day)
    timeVar.set(timeSlot)
    schedule = loadSchedule()
    taskTextWidget.delete(1.0, tk.END)
    if (day, timeSlot) in schedule:
        taskTextWidget.insert(tk.END, schedule[(day, timeSlot)])

def displaySchedule():
    schedule = loadSchedule()
    for day in daysOfWeek:
        for i, timeSlot in enumerate(timeValues):
            btn = gridButtons[day][i]
            if (day, timeSlot) in schedule:
                btn.config(text=schedule[(day, timeSlot)], bg="#4CAF50", activebackground="#60FF70")
            else:
                btn.config(text="", bg=alternateColors[i % 2], activebackground=alternateActiveColors[i % 2])

def addTask():
    selectedDay = dayVar.get()
    selectedTime = timeVar.get()
    task = taskEntry.get()
    if selectedDay and task:
        addToSchedule(selectedDay, selectedTime, task)
        taskEntry.delete(0, tk.END)

def removeTask():
    selectedDay = dayVar.get()
    selectedTime = timeVar.get()
    if selectedDay and selectedTime:
        removeFromSchedule(selectedDay, selectedTime)

root = tk.Tk()
root.title("Schedule")
root.geometry("1600x800")
root.configure(bg="#505050")

alternateColors = ["#3B3B3B", "#474747"]
alternateActiveColors = ["#5B5B5B", "#676767"]

timeValues = [f"{hour:02d}:00" for hour in range(24)]

topFrame = tk.Frame(root, bg="#505050")
topFrame.pack(fill="x", pady=5, padx=15)

dayVar = tk.StringVar()
dayDropdown = ttk.Combobox(topFrame, textvariable=dayVar, values=daysOfWeek, state="readonly", width=15, font=("Arial", 10))
dayDropdown.set("Monday")
dayDropdown.grid(row=0, column=0, padx=5, pady=5)

timeVar = tk.StringVar()
timeDropdown = ttk.Combobox(topFrame, textvariable=timeVar, values=timeValues, state="readonly", width=5, font=("Arial", 10))
timeDropdown.set("08:00")
timeDropdown.grid(row=0, column=1, padx=5, pady=5)

taskEntry = tk.Entry(topFrame, bg="#707070", fg="white", font=("Arial", 10))
taskEntry.grid(row=0, column=2, padx=5, sticky="ew")

addButton = tk.Button(topFrame, text="Add Task", command=addTask, bg="#4CAF50", fg="#2E2E2E", borderwidth=1, relief=tk.RAISED, activebackground="#60FF70", font=("Arial", 10))
addButton.grid(row=0, column=3, padx=5)

removeButton = tk.Button(topFrame, text="Remove Task", command=removeTask, bg="#FF5733", fg="#2E2E2E", borderwidth=1, relief=tk.RAISED, activebackground="#FF8B73", font=("Arial", 10))
removeButton.grid(row=0, column=4, padx=5)

scrollFrame = tk.Frame(root) 
scrollFrame.pack(fill="both", expand=True, side="left")

canvas = tk.Canvas(scrollFrame, bg="#505050")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(scrollFrame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="left", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

innerFrame = tk.Frame(canvas, bg="#505050")
canvas.create_window((0, 0), window=innerFrame, anchor="nw")

gridButtons = {day: [] for day in daysOfWeek}

for day in daysOfWeek:
    lbl = tk.Label(innerFrame, text=day, bg="#505050", fg="white", font=("Arial", 10))
    lbl.grid(row=1, column=daysOfWeek.index(day) + 1, sticky="nsew", pady=2)

for i, timeSlot in enumerate(timeValues):
    tk.Label(innerFrame, text=timeSlot, bg="#505050", fg="white", width=5, font=("Arial", 10)).grid(row=i + 2, column=0, sticky="nsew", padx=2)
    for day in daysOfWeek:
        btn = tk.Button(innerFrame, text="", bg=alternateColors[i % 2], activebackground=alternateActiveColors[i % 2], relief=tk.GROOVE, borderwidth=1, width=12, height=1, font=("Arial", 8), command=lambda d=day, t=timeSlot: gridButtonClick(d, t))
        btn.grid(row=i + 2, column=daysOfWeek.index(day) + 1, sticky="nsew", padx=2, pady=2)
        gridButtons[day].append(btn)

taskTextWidget = tk.Text(root, wrap=tk.WORD, bg="#707070", fg="white", font=("Arial", 10), padx=10, pady=10)
taskTextWidget.pack(fill="both", expand=True, side="right", padx=5, pady=5)

displaySchedule()
root.mainloop()
