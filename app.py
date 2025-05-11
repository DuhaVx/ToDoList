import tkinter as tk
from tkinter import ttk, messagebox
from database import create_tables, register_user, check_user, add_task, get_tasks, mark_task_done

create_tables()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To Do List")
        self.geometry("400x520")
        self.resizable(False, False)
        self.user_id = None
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, TaskFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)
        self.show_frame(LoginFrame)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

class LoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Вход", font=('Arial', 16, 'bold')).pack(pady=18)
        ttk.Label(self, text="Логин:").pack()
        self.username = ttk.Entry(self, width=30)
        self.username.pack(pady=4)
        ttk.Label(self, text="Пароль:").pack()
        self.password = ttk.Entry(self, show="*", width=30)
        self.password.pack(pady=4)
        ttk.Button(self, text="Войти", command=self.login).pack(pady=8, fill='x', padx=70)
        ttk.Button(self, text="Регистрация", command=lambda: master.show_frame(RegisterFrame)).pack(pady=4, fill='x', padx=70)
    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        user_id = check_user(user, pwd)
        if user_id:
            self.master.user_id = user_id
            self.master.frames[TaskFrame].update_tasks()

            self.master.show_frame(TaskFrame)
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль!")

class RegisterFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Регистрация", font=('Arial', 16, 'bold')).pack(pady=18)
        ttk.Label(self, text="Логин:").pack()
        self.username = ttk.Entry(self, width=30)
        self.username.pack(pady=4)
        ttk.Label(self, text="Электронная почта:").pack()
        self.email = ttk.Entry(self, width=30)
        self.email.pack(pady=4)
        ttk.Label(self, text="Пароль:").pack()
        self.password = ttk.Entry(self, show="*", width=30)
        self.password.pack(pady=4)
        ttk.Button(self, text="Зарегистрироваться", command=self.register).pack(pady=8, fill='x', padx=70)
        ttk.Button(self, text="Назад", command=lambda: master.show_frame(LoginFrame)).pack(pady=4, fill='x', padx=70)
    def register(self):
        user = self.username.get().strip()
        email = self.email.get().strip()
        pwd = self.password.get().strip()
        if not user or not email or not pwd:
            messagebox.showwarning("Внимание", "Заполните все поля.")
            return
        if '@' not in email or '.' not in email:
            messagebox.showwarning("Внимание", "Неверный формат e-mail.")
            return
        if len(pwd) < 5:
            messagebox.showwarning("Внимание", "Пароль слишком короткий.")
            return
        if register_user(user, email, pwd):
            messagebox.showinfo("Успех", "Регистрация прошла успешно! Войдите.")
            self.master.show_frame(LoginFrame)
        else:
            messagebox.showerror("Ошибка", "Пользователь или email уже существуют!")

class TaskFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        ttk.Label(self, text="Ваши задачи", font=('Arial', 15, 'bold')).pack(pady=10)
        self.task_list = tk.Listbox(self, font=('Arial', 12), height=15, selectbackground="#b2c9e6", activestyle='none')
        self.task_list.pack(pady=7, padx=20, fill='both', expand=True)
        self.task_list.bind('<Double-Button-1>', self.finish_task)
        self.entry_frame = ttk.Frame(self)
        self.entry_frame.pack(pady=7)
        self.newtask = ttk.Entry(self.entry_frame, width=25)
        self.newtask.pack(side='left', padx=(0, 5))
        ttk.Button(self.entry_frame, text="Добавить", command=self.on_add).pack(side='left')
        ttk.Button(self, text="Выйти", command=self.logout).pack(pady=10, fill='x', padx=80)

    def update_tasks(self):
        self.task_list.delete(0, tk.END)
        for tid, title, status in get_tasks(self.master.user_id):
            s = "✅" if status == "done" else "⏳"
            self.task_list.insert(tk.END, f"{tid}: {title} {s}")

    def on_add(self):
        txt = self.newtask.get().strip()
        if txt:
            add_task(self.master.user_id, txt)
            self.newtask.delete(0, tk.END)
            self.update_tasks()

    def finish_task(self, event):
        if not self.task_list.curselection():
            return
        tid_title = self.task_list.get(self.task_list.curselection()[0])
        tid = int(tid_title.split(":")[0])
        mark_task_done(tid)
        self.update_tasks()

    def logout(self):
        self.master.user_id = None
        self.master.show_frame(LoginFrame)

if __name__ == "__main__":
    App().mainloop()
