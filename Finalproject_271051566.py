import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.tasks = []

class Team:
    def __init__(self, team_name, password):
        self.team_name = team_name
        self.password = password
        self.tasks = []

class Task:
    def __init__(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
        self.priority = priority
        self.completed = False

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Master")
        self.users = {}
        self.teams = {}
        self.current_user = None
        self.is_team_login = False

        self.login_frame = tk.LabelFrame(self.root, text="Login")
        self.login_frame.pack(padx=10, pady=10)

        self.user_type_var = tk.StringVar(value="Individual")
        self.individual_radiobutton = tk.Radiobutton(self.login_frame, text="Individual", variable=self.user_type_var, value="Individual", command=self.toggle_user_type)
        self.individual_radiobutton.grid(row=0, column=0, padx=5, pady=5)
        self.team_radiobutton = tk.Radiobutton(self.login_frame, text="Team", variable=self.user_type_var, value="Team", command=self.toggle_user_type)
        self.team_radiobutton.grid(row=0, column=1, padx=5, pady=5)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.signup_button = tk.Button(self.login_frame, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=4, column=0, columnspan=2)

    def toggle_user_type(self):
        if self.user_type_var.get() == "Team":
            self.username_label.config(text="Team Name:")
        else:
            self.username_label.config(text="Username:")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_type_var.get() == "Team":
            self.is_team_login = True
            if username in self.teams:
                if self.teams[username].password == password:
                    self.current_user = self.teams[username]
                    self.show_task_manager()
                else:
                    messagebox.showerror("Error", "Invalid password.")
            else:
                messagebox.showerror("Error", "Team does not exist. Please sign up.")
        else:
            self.is_team_login = False
            if username in self.users:
                if self.users[username].password == password:
                    self.current_user = self.users[username]
                    self.show_task_manager()
                else:
                    messagebox.showerror("Error", "Invalid password.")
            else:
                messagebox.showerror("Error", "User does not exist. Please sign up.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_type_var.get() == "Team":
            if username and password:
                if username not in self.teams:
                    self.teams[username] = Team(username, password)
                    messagebox.showinfo("Success", "Team created successfully. You can now login.")
                else:
                    messagebox.showerror("Error", "Team name already exists. Please choose a different name.")
            else:
                messagebox.showerror("Error", "Please enter both team name and password.")
        else:
            if username and password:
                if username not in self.users:
                    self.users[username] = User(username, password)
                    messagebox.showinfo("Success", "User created successfully. You can now login.")
                else:
                    messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            else:
                messagebox.showerror("Error", "Please enter both username and password.")

    def show_task_manager(self):
        self.login_frame.destroy()

        self.task_frame = tk.LabelFrame(self.root, text="Task Master")
        self.task_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.task_frame, width=50, height=15)
        self.task_listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.refresh_tasks()

        self.create_task_button = tk.Button(self.task_frame, text="Add Task", command=self.create_task)
        self.create_task_button.pack(pady=5)

        self.edit_task_button = tk.Button(self.task_frame, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(pady=5)

        self.remove_task_button = tk.Button(self.task_frame, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack(pady=5)

        self.logout_button = tk.Button(self.task_frame, text="Logout", command=self.logout)
        self.logout_button.pack(pady=5)

        self.save_tasks_button = tk.Button(self.task_frame, text="Save Tasks", command=self.save_tasks)
        self.save_tasks_button.pack(pady=5)

        self.start_reminder_thread()

    def create_task(self):
        create_task_window = tk.Toplevel(self.root)
        create_task_window.title("Create Task")

        title_label = tk.Label(create_task_window, text="Title:")
        title_label.grid(row=0, column=0, padx=5, pady=5)
        title_entry = tk.Entry(create_task_window)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        description_label = tk.Label(create_task_window, text="Description:")
        description_label.grid(row=1, column=0, padx=5, pady=5)
        description_entry = tk.Entry(create_task_window)
        description_entry.grid(row=1, column=1, padx=5, pady=5)

        due_date_label = tk.Label(create_task_window, text="Due Date (YYYY-MM-DD HH:MM):")
        due_date_label.grid(row=2, column=0, padx=5, pady=5)
        due_date_entry = tk.Entry(create_task_window)
        due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        priority_label = tk.Label(create_task_window, text="Priority:")
        priority_label.grid(row=3, column=0, padx=5, pady=5)
        priority_entry = tk.Entry(create_task_window)
        priority_entry.grid(row=3, column=1, padx=5, pady=5)

        create_button = tk.Button(create_task_window, text="Create", command=lambda: self.add_task(
            title_entry.get(), description_entry.get(), due_date_entry.get(), priority_entry.get(), create_task_window))
        create_button.grid(row=4, columnspan=2, padx=5, pady=10)

    def add_task(self, title, description, due_date, priority, window):
        if title and due_date:
            task = Task(title, description, due_date, priority)
            self.current_user.tasks.append(task)
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task created successfully.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Title and Due Date are required fields.")

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            task = self.current_user.tasks[task_index]

            edit_task_window = tk.Toplevel(self.root)
            edit_task_window.title("Edit Task")

            title_label = tk.Label(edit_task_window, text="Title:")
            title_label.grid(row=0, column=0, padx=5, pady=5)
            title_entry = tk.Entry(edit_task_window)
            title_entry.insert(0, task.title)
            title_entry.grid(row=0, column=1, padx=5, pady=5)

            description_label = tk.Label(edit_task_window, text="Description:")
            description_label.grid(row=1, column=0, padx=5, pady=5)
            description_entry = tk.Entry(edit_task_window)
            description_entry.insert(0, task.description)
            description_entry.grid(row=1, column=1, padx=5, pady=5)

            due_date_label = tk.Label(edit_task_window, text="Due Date (YYYY-MM-DD HH:MM):")
            due_date_label.grid(row=2, column=0, padx=5, pady=5)
            due_date_entry = tk.Entry(edit_task_window)
            due_date_entry.insert(0, task.due_date.strftime('%Y-%m-%d %H:%M'))
            due_date_entry.grid(row=2, column=1, padx=5, pady=5)

            priority_label = tk.Label(edit_task_window, text="Priority:")
            priority_label.grid(row=3, column=0, padx=5, pady=5)
            priority_entry = tk.Entry(edit_task_window)
            priority_entry.insert(0, task.priority)
            priority_entry.grid(row=3, column=1, padx=5, pady=5)

            save_button = tk.Button(edit_task_window, text="Save", command=lambda: self.save_task(
                task_index, title_entry.get(), description_entry.get(), due_date_entry.get(), priority_entry.get(), edit_task_window))
            save_button.grid(row=4, columnspan=2, padx=5, pady=10)
        else:
            messagebox.showerror("Error", "Please select a task to edit.")

    def save_task(self, task_index, title, description, due_date, priority, window):
        if title and due_date:
            updated_task = Task(title, description, due_date, priority)
            self.current_user.tasks[task_index] = updated_task
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task updated successfully.")
            window.destroy()
        else:
            messagebox.showerror("Error", "Title and Due Date are required fields.")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            del self.current_user.tasks[task_index]
            self.refresh_tasks()
            messagebox.showinfo("Success", "Task removed successfully.")
        else:
            messagebox.showerror("Error", "Please select a task to remove.")

    def logout(self):
        self.current_user = None
        self.is_team_login = False
        self.task_frame.destroy()
        self.login_frame = tk.LabelFrame(self.root, text="Login")
        self.login_frame.pack(padx=10, pady=10)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.current_user.tasks:
            self.task_listbox.insert(tk.END, f"{task.title} - Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M')}, Priority: {task.priority}")

    def save_tasks(self):
        if self.is_team_login:
            self.teams[self.current_user.team_name] = self.current_user
        else:
            self.users[self.current_user.username] = self.current_user

    def start_reminder_thread(self):
        self.reminder_thread = threading.Thread(target=self.reminder_check, daemon=True)
        self.reminder_thread.start()

    def reminder_check(self):
        while True:
            if self.current_user:
                now = datetime.now()
                for task in self.current_user.tasks:
                    if now > task.due_date - timedelta(minutes=30) and not task.completed:
                        self.notify(task.title)
            threading.Event().wait(60)

    def notify(self, task_title):
        messagebox.showinfo("Reminder", f"The task '{task_title}' is due soon!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
