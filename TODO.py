import json
import os
import tkinter as tk
from tkinter import ttk

FILE = "tasks.json"
tasks = json.load(open(FILE)) if os.path.exists(FILE) else []

def save():
    json.dump(tasks, open(FILE, 'w'), indent=2)

def show_tasks_gui():
    win = tk.Tk()
    win.title("Tasks")
    win.geometry("300x250")

    for i, t in enumerate(tasks, 1):
        status = "✓" if t["done"] else "☐"
        label = tk.Label(win, text=f"{i}. {status} {t['name']}", font=("Arial", 12))
        label.pack(anchor="w", padx=20, pady=3)

    close_button = tk.Button(win, text="Close", command=win.destroy)
    close_button.pack(pady=10)

    win.mainloop()

while True:
    print("1. Show  2. Add  3. Done  4. Delete  5. Exit")
    choice = input(" ")

    if choice == "1":
        show_tasks_gui()

    elif choice == "2":
        name = input("Task: ")
        task = {"name": name, "done": False}
        tasks.append(task)
        save()

    elif choice == "3":
        number = int(input("Number: "))
        tasks[number - 1]["done"] = True
        save()


    elif choice == "5":
        break