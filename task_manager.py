import json
from datetime import datetime

class Task():
    instance_count = 0
    def __init__(self, task_name, task_status= "todo"):
        Task.instance_count += 1
        self.task_id = Task.instance_count
        self.task_name = task_name
        self.task_status = task_status
        self.createdAt = self.created_at()
        self.updatedAt = self.updated_at()
        self.description = ""


    

    
    def add_description(self, description):
        self.description = description

    def change_task_status(self, task_status):
        self.task_status = task_status


    def current_time(self):
        date_now = datetime.now()
        hour = datetime.time(date_now).hour
        minute = datetime.time(date_now).minute
        return f"{hour}:{minute}"
    
    def current_date(self):
        date_now = datetime.now()
        return date_now.date()
    
    def created_at(self):
        return f"{self.current_time()} on {self.current_date()}"
    
    def updated_at(self):
        return f"{self.current_time()} on {self.current_date()}"

    



class Task_Tracker():
    def __init__(self): 
        self.tasks = self.load_tasks()

        if self.tasks:
            Task.instance_count = max(task.task_id for task in self.tasks)
        else:
            Task.instance_count = 0


    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f:
                tasks_data = json.load(f)
                return [Task(t["name"], t["status"]) for t in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    def add_task(self, user_command: str, description: str):
        try:
            chunks = user_command.split()
            task_name = " ".join(chunks[1:])
            task = Task(task_name)
            task.add_description(description)
            self.tasks.append(task)
        except IndexError:
            print("Please give a valid task input. Example. add <task-name>")
        
        
        
    
    def update_task_name(self, user_command: str):
        try:
            chunks = user_command.split()
            task_id = int(chunks[1])
            new_name = " ".join(chunks[2:])
            for task in self.tasks:
                if task_id == task.task_id:
                    task.task_name = new_name
                    task.updatedAt = task.updated_at()
        except IndexError:
            print("Enter a valid input to update the task. Example update <id-of-task> <new-name>")
        except ValueError:
            print("Please enter valid values. Example update <id-of-task> <new_name>")

    def update_task_description(self, user_command: str):
        try:
            chunks = user_command.split()
            task_id = int(chunks[1])
            new_description = input("modify desc: ")
            for task in self.tasks:
                if task_id == task.task_id:
                    task.description = new_description
        except ValueError:
            print("Please enter a numeric value for task_id, Example: update-description <task_id>")
        except IndexError:
            print("Please enter the value of task_id, Example: update-description <task_id>")

    def delete_task(self, user_command: str):
        try:
            chunks = user_command.split()
            task_id = int(chunks[1])
            for task in self.tasks:
                if task_id == task.task_id:
                    self.tasks.remove(task)
        except ValueError:
            print("Please enter a valid int value, Example: delete <task-id>")
       

        

    def mark_in_progress(self, task_id: int):
        for task in self.tasks:
            if task_id == task.task_id:
                task.task_status = "in-progress"
                task.updatedAt = task.updated_at()



    def mark_done(self, task_id: int):
        for task in self.tasks:
            if task_id == task.task_id:
                task.task_status = "done"
                task.updatedAt = task.updated_at()


    def mark_todo(self, task_id: int):
        for task in self.tasks:
            if task_id == task.task_id:
                task.task_status = "todo"
                task.updatedAt = task.updated_at()

    def list_all_tasks(self):
        for task in self.tasks:
            print(f"{task.task_id}. {task.task_name}")

    def list_done_tasks(self):
        for task in self.tasks:
            if task.task_status == "done":
                print(f"{task.task_id}. {task.task_name}")

    def list_todo_tasks(self):
        for task in self.tasks:
            if task.task_status == "todo":
                print(f"{task.task_id}. {task.task_name}")
                      
    def list_in_progress_tasks(self):
        for task in self.tasks:
            if task.task_status == "in-progress":
                print(f"{task.task_id}. {task.task_name}")

    def mark_task(self, user_command: str):
        chunks  = user_command.split()
        mark_chunk = chunks[0]
        task_id = int(chunks[1])
        if mark_chunk.endswith("done"):
            self.mark_done(task_id)
        elif mark_chunk.endswith("progress"):
            self.mark_in_progress(task_id)
        elif mark_chunk.endswith("todo"):
            self.mark_todo(task_id)

    def listing_tasks(self, user_command: str):
        chunks = user_command.split()
        if len(chunks)> 1:  
            status = chunks[1]
        else:
            status = "all"
        if status == "done":
            self.list_done_tasks()
        elif status == "in-progress":
            self.list_in_progress_tasks()
        elif status == "todo":
            self.list_todo_tasks()
        else:
            self.list_all_tasks()

    def display_task_description(self, user_command: str):
        try:
            chunks = user_command.split()
            task_id = int(chunks[1])
            for task in self.tasks:
                if task_id == task.task_id:
                    print(f"Desc: {task.description}")
        except IndexError:
            print("please enter the value of task_id, Example: show-description <task-id>")
        except ValueError:
            print("Please enter a numeric task-id, example: show-description <task-id>")
    def file_content():
        with open("tasks.json", "w") as f:
            content = json.loads(f)
            return content


   

    


def main():
    task_tracker = Task_Tracker()
    while True:
     
        usr_input = input("> ")
        chunks = usr_input.split()
        if usr_input.startswith(("add", "update", "delete", "mark-", "list", "show-" )):
            command = chunks[0].lower()
            if command == "add":
                description = input("add description ")
                task_tracker.add_task(usr_input, description)

            elif command.startswith("update-desc"):
                task_tracker.update_task_description(usr_input)
            elif command == "update":
                task_tracker.update_task_name(usr_input)
                
            elif command == "delete":
                task_tracker.delete_task(usr_input)

            elif command.startswith("mark-"):
                task_tracker.mark_task(usr_input)
            
            elif command == "list":
                task_tracker.listing_tasks(usr_input)

            elif usr_input.startswith("show-"):
                task_tracker.display_task_description(usr_input)
        else:
            print("please enter a valid command")
        with open("tasks.json", "w") as f:
            tasks_details = []
            for task in task_tracker.tasks:
                task_info_dict = {"id": task.task_id,
                                  "name": task.task_name,
                                  "description": task.description,
                                  "status": task.task_status,
                                  "createdAt": task.createdAt,
                                  "updatedAt": task.updatedAt}
                tasks_details.append(task_info_dict)
            json.dump(tasks_details, f,indent=4)



main()
                
          




