import json

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

todo_list = load_tasks()

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(todo_list, file, indent=4)

def add_task(task):
    todo_list.append({"task": task, "done": False})
    print(f"Task '{task}' added to the list.")
    save_tasks()

def show_tasks():
    if not todo_list:
        print("No tasks in the list.")
    else:
        print("To-Do List:")
        for i, item in enumerate(todo_list, start=1):
            status = "✓" if item["done"] else "✗"
            print(f"{i}. {item['task']} [{status}]")

def mark_done(index):
    index -= 1 
    if 0 <= index < len(todo_list):
        todo_list[index]["done"] = True
        print(f"Task '{todo_list[index]['task']}' marked as done.")
        save_tasks()
    else:
        print("Invalid task number.")

def remove_task(index):
    index -= 1 
    if 0 <= index < len(todo_list):
        removed_task = todo_list.pop(index)
        print(f"Task '{removed_task['task']}' removed from the list.")
        save_tasks()
    else:
        print("Invalid task number.")

def filter_by_status(done_status):
    filtered = [item for item in todo_list if item["done"] == done_status]
    if not filtered:
        print("No matching tasks found.")
        return
    
    print("Filtered Tasks:")
    for i, item in enumerate(filtered, start=1):
        status = "✓" if item["done"] else "✗"
        print(f"{i}. {item['task']} [{status}]")

def search_tasks(keyword):
    keyword = keyword.lower()
    results = [item for item in todo_list if keyword in item['task'].lower()]

    if not results:
        print("No tasks found matching that keyword.")
        return
    
    print(f"Tasks matching '{keyword}':")

    for i, item in enumerate(results, start=1):
        status = "✓" if item["done"] else "✗"
        print(f"{i}. {item['task']} [{status}]")

def main():
    while True:
        print("\nTo-Do List Menu:")
        print("1. Add Task")
        print("2. Show Tasks")
        print("3. Mark Task as Done")
        print("4. Remove Task")
        print("5. Filter Tasks by Status")
        print("6. Search Tasks by Keyword")
        print("7. Exit")
        
        choice = input("Choose an option (1-7): ")
        
        if choice == '1':
            task = input("Enter the task: ")
            add_task(task)
        elif choice == '2':
            show_tasks()
        elif choice == '3':
            try:
                index = int(input("Enter the task number to mark as done: "))
                mark_done(index)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            try:
                index = int(input("Enter the task number to remove: "))
                remove_task(index)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '5':
            status_input = input("Show tasks (done/pending): ").strip().lower()
            if status_input == 'done':
                filter_by_status(True)
            elif status_input == 'pending':
                filter_by_status(False)
            else:
                print("Invalid input. Type 'done' or 'pending'.")
        elif choice == '6':
            keyword = input("Enter keyword to search: ")
            search_tasks(keyword)
        elif choice == '7':
            print("Exited the To-Do List.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()