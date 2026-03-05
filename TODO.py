import json, os

FILE = "tasks.json"
tasks = json.load(open(FILE)) if os.path.exists(FILE) else []

def save():
    json.dump(tasks, open(FILE, 'w'), indent=2)

while True:
    print("\n1. Show  2. Add  3. Done  4. Delete  5. Exit")
    choice = input("> ")

    if choice == "1":
        for i, t in enumerate(tasks, 1):
            print(f"{i}. [{'✓' if t['done'] else ' '}] {t['name']}")

    elif choice == "2":
        tasks.append({"name": input("Task: "), "done": False})
        save()

    elif choice == "3":
        tasks[int(input("Number: ")) - 1]["done"] = True
        save()

    elif choice == "4":
        tasks.pop(int(input("Number: ")) - 1)
        save()

    elif choice == "5":
        break