import click #to creat a command line interface
import json #to store and load data tasks from a file
import os #to check if the file exists

TODO_FILE = "todo.json"


#function to load task from the json file
def load_tasks():
    if not os.path.exists(TODO_FILE): #check if the file exists
        return [] #if not, return an empty list
    with open(TODO_FILE, "r") as file: #open the file in read mode
        return json.load(file) #load the data from the file and return it
    

#function to save tasks to the json file
def save_tasks(tasks): #takes a list of tasks as an argument
    with open(TODO_FILE, "w") as file: #open the file in write mode
        json.dump(tasks, file, indent=4) #save task as formated json 


@click.group() #define a click command group (main cli)
def cli():
    """Simple To-do list Manager""" #docstring for the main cli
    pass  #no action, acts as a container for other commands


@click.command() #define a new command called add
@click.argument("task") #accept a required argument called task
def add(task):
    """Add a new task to the list""" #docstring for the add command
    tasks = load_tasks() #load existing tasks 
    tasks.append({"task": task, "done": False}) #add a new task (default:not done)
    save_tasks(tasks) #save the updated tasks
    click.echo(f"Task added successfuly: {task}") #print a message to the user


@click.command() #define a new command called list
def list():
    """List all tasks"""
    tasks = load_tasks() #load existing tasks
    if not tasks: #check if there are no tasks
        click.echo("No tasks found") #print a message to the user
        return #exit the function
    for i, task in enumerate(tasks, 1): #loop through the tasks with numbring
        status = "✅" if task["done"] else "❌ " #check if the task is done
        click.echo(f"{i}. {task['task']} [{status}]") #print the task with status


@click.command() #define a new command called complete
@click.argument("task_number", type=int) #accepy a task number as an integer
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks() #load existing tasks
    if 0 < task_number <= len(tasks): #check if the task number is valid
        tasks[task_number - 1]["done"] = True #mark the task as done
        save_tasks(tasks) #save the updated tasks
        click.echo(f"Task {task_number} marked as completed") #print a message to the user
    else:
        click.echo(f"Invalid task number") #print a message to the user


@click.command() #define a new command called remove
@click.argument("task_number", type=int) #accept a task number as an integer
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks() #load existing tasks
    if 0 < task_number <= len(tasks): #check if the task number is valid
        removed_task = tasks.pop(task_number - 1) #remove the task from the list
        save_tasks(tasks) #save the updated tasks
        click.echo(f"Task removed: {removed_task['task']}") #print a message to the user
    else:
        click.echo(f"Invalid task number:") #print a message to the user


#add the commands to the main cli
cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)

#if the script is run directly,start the main cli
if __name__ == "__main__":
    cli()
