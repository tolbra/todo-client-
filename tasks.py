from argparse import ArgumentParser
from datetime import datetime
from tabulate import tabulate
from typing import Literal, Callable, Generator
import json
import os
import sys
from colorama import init
init()
from colorama import Fore, Back, Style

TASKS_FILE = 'tasks.json'




def load_tasks(jsonfile: str = None):
    if jsonfile is None:
        jsonfile = TASKS_FILE
    if os.path.exists(jsonfile):
        with open(jsonfile, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []
def save_tasks(tasks, jsonfile: str = None):
    if jsonfile is None:
        jsonfile = TASKS_FILE
    with open(jsonfile, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    task_id = 1 if not tasks else tasks[-1]['id'] + 1
    task = {
        'id' : task_id,
        'description' : description,
        'status': 'todo',
        
        'createdAt' : datetime.now().ctime(),
        'updatedAt' : datetime.now().ctime(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully with ID: {task_id}')

def id_order(tasks):   
        for i in range(0, len(tasks)):
            tasks[i]['id'] = i+1
        return tasks

def delete_task(description):
    tasks = load_tasks()    
    
    id_order(tasks)


    id = int(description)
    
    tasks = tasks[:id] + tasks[id + 1:]

    id_order(tasks)

    save_tasks(tasks)
    print('The task was successfully deleted')

    list_tasks()

def update_task(task_id, description):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task["id"] == int(task_id):
            task["description"] = description
            task["updatedAt"] = datetime.now().ctime()
            found = True
            break
    if not found:
        print("Error: Task not found")
    save_tasks(tasks)
    list_tasks()

def update_status(id):
    print(f"""Choose status for task {id}:
    1 - To Do
    2 - In Progress
    3 - Done""")
    tasks = load_tasks()
    task_id = int(id)
    
    # Find task by ID
    for task in tasks:
        if task['id'] == task_id:
            user_input = input().strip()
            if user_input == "1":
                task['status'] = 'todo'  # Lowercase
            elif user_input == "2":
                task['status'] = 'in-progress'
            elif user_input == "3":
                task['status'] = 'done'
            else:
                print("Invalid input")
            task['updatedAt'] = datetime.now().ctime()
            break
    save_tasks(tasks)
    list_tasks()
     
def filter_tasks():
    tasks = load_tasks()
    print("""Choose which filters you want to apply:
    1 - Date descending
    2 - Status: Done
    3 - Status: In Progress
    4 - Status: To Do""")

    userFilter = input()
    
    if userFilter == '1':
        tasks = sorted(tasks, key=lambda task: task['createdAt'], reverse=True)
    elif userFilter == '2':
        tasks = [task for task in tasks if task['status'].lower() == 'done']
    elif userFilter == '3':
        tasks = [task for task in tasks if task['status'].lower() == 'in-progress']
    elif userFilter == '4':
        tasks = [task for task in tasks if task['status'].lower() == 'todo']
        
    list_tasks(tasks)
         
def search():
    tasks = load_tasks()
    userInput = input()
    matching_tasks = []
    for task in tasks:
        if userInput in task['description']:
            matching_tasks.append(task)
    list_tasks(matching_tasks)

def list_tasks(filtered=None):
    if filtered == None:
        tasks = load_tasks()
    else:
        tasks = filtered

    if not tasks:
        print('No tasks found')
        return
    print(Fore.GREEN + 'Tasks:')

    headers = ["ID", "Description", "Status", "Created", "Updated"]

    table = []
    for task in tasks:
        row = [task['id'], task['description'], task['status'], task['createdAt'], task['updatedAt']]
        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid"))



def main():
    parser = ArgumentParser(description='Simple Task Tracker CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # 'add' command
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('description', help='Description of the task')

    # 'List' command
    parser_list = subparsers.add_parser('list', help="List all tasks")

    # 'delete' command
    parser_delete = subparsers.add_parser('delete', help='Delete the task')
    parser_delete.add_argument('description', help="Write the ID of task you want to delete")

    # 'update tasks' command
    parser_update = subparsers.add_parser('update tasks', help='Update the task')
    parser_update.add_argument('id', help='Write the ID of the task you want to change')
    parser_update.add_argument('description', help='New description :')

    # 'update status' command
    parser_status = subparsers.add_parser('update status', help='Update the status')
    parser_status.add_argument('id', help = 'id')

    parser_filter = subparsers.add_parser('filter')

    parser_search = subparsers.add_parser('search')

    args = parser.parse_args()

    if args.command == 'add':
        add_task(args.description)
    elif args.command == 'list':
        list_tasks()
    elif args.command == "delete":
        print('Do you want to delete a task? Type y/N')
        conformation = input('y/N   ')
        if conformation == 'y':
            delete_task(args.description)
    elif args.command == 'update tasks':
        update_task(args.id, args.description)
    elif args.command == 'update status':
        update_status(args.id)
    elif args.command == 'filter':
        filter_tasks()
    elif args.command == 'search':
        search()

if __name__ == '__main__':
    main()