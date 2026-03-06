import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

FILE = "tasks.json"

# logic of code

tasks = json.load(open(FILE)) if os.path.exists(FILE) else []

def save():
    json.dump(tasks, open(FILE, 'w'), indent=2) ## SAVE JSON FILE 

def add_task(name, priority="low"):
    if name and name.strip():
        tasks.append({
            "name": name.strip(), 
            "done": False,
            "priority": priority}) ##  "append" מוסיף משימה חדשה  
        save()
        return True
    return False

def mark_done(num):
    if num and 0 < num <= len(tasks):
        tasks[num - 1]["done"] = True  ## מסמן שהמשימה הסתיימה 
        save()
        return True
    return False

def delete_task(num):
    if num and 0 < num <= len(tasks):
        tasks.pop(num - 1)   ## delete with -- pop = delete
        save()
        return True
    return False


def add_task_ui():
    name = styled_dialog("ADD TASK", "Enter task name:")  ## שואל שם של משימה 
    priority = styled_dialog("PRIORITY", "Enter priority (low / mid / high):")  # בוחרים עדיפות 
    if priority not in ("low", "mid", "high"):
        priority = "low"
    if add_task(name, priority):
        _info_popup("Task added.", f'"{name.strip()}" is on the list.')

def mark_done_ui():
    num = styled_dialog("MARK DONE", "Enter task number:", kind="int")  ## שואל איזה אחת אתה רוצה לסמן 
    if num is None:
        return
    if not mark_done(num):
        _info_popup("Invalid number.", "Check the task list and try again.")

def delete_task_ui():
    num = styled_dialog("DELETE TASK", "Enter task number:", kind="int")  ## שואל איזה אחד תרצה למחוק 
    if num is None:
        return
    if delete_task(num):
        _info_popup("Deleted.", f"Task {num} removed from the list.")
    else:
        _info_popup("Invalid number.", "Check the task list and try again.")


# DESIGN SECTION (User Interface)

#  Color Palette 
BG        = "#0d0d0d"
SURFACE   = "#1a1515"
ACCENT    = "#8b2e2e"
ACCENT2   = "#c0504a"
TEXT      = "#ede8e8"
TEXT_DIM  = "#6b5555"
SUCCESS   = "#4caf7d"
DANGER    = "#c0392b"
BORDER    = "#2e1f1f"

# Priority colors
PRIORITY_COLORS = {
    "high": "#e05252",
    "mid":  "#e0a852",
    "low":  "#5288e0",
}
PRIORITY_LABELS = {
    "high": "▲ HIGH",
    "mid":  "● MID",
    "low":  "▼ LOW",
}

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_LABEL  = ("Courier New", 10)
FONT_BTN    = ("Courier New", 10, "bold")
FONT_SMALL  = ("Courier New", 9)

def styled_dialog(title, prompt, kind="string"):
    """Custom styled input dialog."""
    dialog = tk.Toplevel()
    dialog.title("")
    dialog.configure(bg=BG)
    dialog.resizable(False, False)
    dialog.grab_set()

    w, h = 340, 180
    dialog.geometry(f"{w}x{h}")
    dialog.update_idletasks()
    x = dialog.winfo_screenwidth() // 2 - w // 2
    y = dialog.winfo_screenheight() // 2 - h // 2
    dialog.geometry(f"+{x}+{y}")

    bar = tk.Frame(dialog, bg=ACCENT, height=3)
    bar.pack(fill="x")

    tk.Label(dialog, text=title, font=("Courier New", 11, "bold"),
             bg=BG, fg=ACCENT2).pack(pady=(14, 2))
    tk.Label(dialog, text=prompt, font=FONT_SMALL,
             bg=BG, fg=TEXT_DIM).pack(pady=(0, 8))

    entry = tk.Entry(dialog, font=FONT_LABEL, bg=SURFACE, fg=TEXT,
                     insertbackground=ACCENT2, relief="flat",
                     bd=0, width=28, justify="center")
    entry.pack(ipady=6, pady=2)
    entry.focus_set()

    tk.Frame(dialog, bg=ACCENT, height=1, width=220).pack()

    result = [None]

    def confirm(e=None):
        val = entry.get()
        if kind == "int":
            try:
                result[0] = int(val)
            except ValueError:
                result[0] = None
        else:
            result[0] = val if val.strip() else None
        dialog.destroy()

    def cancel(e=None):
        dialog.destroy()

    btn_frame = tk.Frame(dialog, bg=BG)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="OK", font=FONT_BTN,
              bg=ACCENT, fg="#fff", relief="flat", bd=0,
              padx=18, pady=4, cursor="hand2",
              command=confirm).pack(side="left", padx=6)

    tk.Button(btn_frame, text="CANCEL", font=FONT_BTN,
              bg=SURFACE, fg=TEXT_DIM, relief="flat", bd=0,
              padx=14, pady=4, cursor="hand2",
              command=cancel).pack(side="left", padx=6)

    dialog.bind("<Return>", confirm)
    dialog.bind("<Escape>", cancel)
    dialog.wait_window()
    return result[0]


def show_tasks_ui():
    if not tasks:
        _info_popup("No tasks yet.", "Start adding tasks to get going.")
        return

    win = tk.Toplevel()
    win.title("")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    w, h = 480, 500
    win.update_idletasks()
    x = win.winfo_screenwidth() // 2 - w // 2
    y = win.winfo_screenheight() // 2 - h // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

    tk.Frame(win, bg=ACCENT, height=5).pack(fill="x")

    hdr = tk.Frame(win, bg=BG)
    hdr.pack(fill="x", padx=28, pady=(22, 0))

    tk.Label(hdr, text="MY TASKS", font=("Courier New", 20, "bold"),
             bg=BG, fg=TEXT).pack(side="left")

    done_count = sum(1 for t in tasks if t["done"])
    badge_col = SUCCESS if done_count == len(tasks) else ACCENT
    badge = tk.Label(hdr, text=f" {done_count} / {len(tasks)} ",
                     font=("Courier New", 11, "bold"),
                     bg=badge_col, fg=BG, padx=6, pady=2)
    badge.pack(side="right")

    tk.Label(win, text=f"{len(tasks) - done_count} remaining",
             font=("Courier New", 9), bg=BG, fg=TEXT_DIM).pack(anchor="w", padx=30)

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(10, 6))

    container = tk.Frame(win, bg=BG)
    container.pack(fill="both", expand=True, padx=0)

    canvas = tk.Canvas(container, bg=BG, highlightthickness=0, bd=0)
    scroll = tk.Scrollbar(container, orient="vertical", command=canvas.yview,
                          bg=SURFACE, troughcolor=BG, width=8)
    inner = tk.Frame(canvas, bg=BG)

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw", width=w - 28)
    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
    scroll.pack(side="right", fill="y", padx=(0, 8))

    for i, t in enumerate(tasks, 1):
        done = t["done"]
        priority = t.get("priority", "low")
        card_bg    = "#13131c" if done else "#1c1c2a"
        stripe_col = SUCCESS if done else PRIORITY_COLORS.get(priority, ACCENT)

        wrap = tk.Frame(inner, bg=BG)
        wrap.pack(fill="x", pady=5, padx=(4, 16))

        card = tk.Frame(wrap, bg=card_bg)
        card.pack(fill="x")

        # left stripe - color changes by priority
        tk.Frame(card, bg=stripe_col, width=5).pack(side="left", fill="y")

        body = tk.Frame(card, bg=card_bg)
        body.pack(side="left", fill="both", expand=True, padx=(16, 16), pady=14)

        # row: number pill + name + status
        row = tk.Frame(body, bg=card_bg)
        row.pack(fill="x")

        num_bg = "#2a2a40" if not done else "#1a2a1a"
        tk.Label(row, text=f" {i} ", font=("Courier New", 9, "bold"),
                 bg=num_bg, fg=ACCENT2 if not done else SUCCESS,
                 padx=4).pack(side="left", padx=(0, 12))

        name_fg = TEXT if not done else TEXT_DIM
        lbl = tk.Label(row, text=t["name"], font=("Courier New", 13),
                       bg=card_bg, fg=name_fg, anchor="w")
        lbl.pack(side="left", fill="x", expand=True)

        if done:
            tk.Label(row, text="✓", font=("Courier New", 14, "bold"),
                     bg=card_bg, fg=SUCCESS).pack(side="right", padx=(8, 0))
        else:
            tk.Label(row, text="—", font=("Courier New", 12),
                     bg=card_bg, fg=TEXT_DIM).pack(side="right", padx=(8, 0))

        # priority badge - shown below task name
        if not done:
            p_color = PRIORITY_COLORS.get(priority, ACCENT2)
            p_label = PRIORITY_LABELS.get(priority, "▼ LOW")
            tk.Label(body, text=p_label, font=("Courier New", 8, "bold"),
                     bg=card_bg, fg=p_color).pack(anchor="w", pady=(4, 0))

    tk.Frame(win, bg=BORDER, height=1).pack(fill="x", padx=28, pady=(8, 0))

    footer = tk.Frame(win, bg=BG)
    footer.pack(fill="x", padx=28, pady=14)

    tk.Button(footer, text="CLOSE", font=FONT_BTN,
              bg=ACCENT, fg="#fff", relief="flat", bd=0,
              padx=32, pady=8, cursor="hand2",
              command=win.destroy).pack(side="right")


def _info_popup(title, body=""):
    win = tk.Toplevel()
    win.title("")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()
    w, h = 300, 140
    win.geometry(f"{w}x{h}")
    win.update_idletasks()
    x = win.winfo_screenwidth() // 2 - w // 2
    y = win.winfo_screenheight() // 2 - h // 2
    win.geometry(f"+{x}+{y}")
    tk.Frame(win, bg=ACCENT, height=3).pack(fill="x")
    tk.Label(win, text=title, font=("Courier New", 11, "bold"),
             bg=BG, fg=TEXT).pack(pady=(18, 4))
    if body:
        tk.Label(win, text=body, font=FONT_SMALL, bg=BG, fg=TEXT_DIM).pack()
    tk.Button(win, text="OK", font=FONT_BTN,
              bg=ACCENT, fg="#fff", relief="flat", bd=0,
              padx=22, pady=5, cursor="hand2",
              command=win.destroy).pack(pady=14)
    win.bind("<Return>", lambda e: win.destroy())
    win.bind("<Escape>", lambda e: win.destroy())


def main_menu():
    root = tk.Tk()
    root.title("Task Manager")
    root.configure(bg=BG)
    root.resizable(False, False)

    w, h = 320, 420
    root.geometry(f"{w}x{h}")
    root.update_idletasks()
    x = root.winfo_screenwidth() // 2 - w // 2
    y = root.winfo_screenheight() // 2 - h // 2
    root.geometry(f"+{x}+{y}")

    tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")

    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=28, pady=(30, 6))

    tk.Label(header, text="TASK", font=("Courier New", 32, "bold"),
             bg=BG, fg=TEXT).pack(anchor="w")
    tk.Label(header, text="MANAGER", font=("Courier New", 32, "bold"),
             bg=BG, fg=ACCENT).pack(anchor="w")
    tk.Label(header, text="________________", font=FONT_SMALL,
             bg=BG, fg=BORDER).pack(anchor="w", pady=(4, 0))

    btn_area = tk.Frame(root, bg=BG)
    btn_area.pack(fill="x", padx=28, pady=20)

    def make_btn(parent, label, sublabel, cmd, danger=False):
        fg_col = DANGER if danger else ACCENT2
        f = tk.Frame(parent, bg=SURFACE, cursor="hand2")
        f.pack(fill="x", pady=5)

        inner = tk.Frame(f, bg=SURFACE)
        inner.pack(fill="x", padx=16, pady=10)

        tk.Label(inner, text=label, font=FONT_BTN,
                 bg=SURFACE, fg=fg_col, anchor="w").pack(side="left")
        tk.Label(inner, text=sublabel, font=FONT_SMALL,
                 bg=SURFACE, fg=TEXT_DIM, anchor="e").pack(side="right")

        stripe = tk.Frame(f, bg=fg_col, width=3)
        stripe.place(x=0, y=0, relheight=1)

        def on_enter(e):
            f.configure(bg="#24243a")
            inner.configure(bg="#24243a")
            for w in inner.winfo_children():
                w.configure(bg="#24243a")

        def on_leave(e):
            f.configure(bg=SURFACE)
            inner.configure(bg=SURFACE)
            for w in inner.winfo_children():
                w.configure(bg=SURFACE)

        def on_click(e):
            cmd()

        for widget in [f, inner] + list(inner.winfo_children()):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)

    actions = [
        ("SHOW TASKS",  "view list",    show_tasks_ui,  False),
        ("ADD TASK",    "create new",   add_task_ui,    False),
        ("MARK DONE",   "check off",    mark_done_ui,   False),
        ("DELETE TASK", "remove",       delete_task_ui, False),
        ("EXIT",        "quit",         root.quit,      True),
    ]

    for label, sub, cmd, danger in actions:
        make_btn(btn_area, label, sub, cmd, danger)

    tk.Label(root, text="v1.0  //  SHARK EDITION",
             font=("Courier New", 8), bg=BG, fg=TEXT_DIM).pack(side="bottom", pady=10)

    root.mainloop()


main_menu()