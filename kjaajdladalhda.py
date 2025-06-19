import tkinter as tk
from tkinter import messagebox
import requests
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class StudentSystemGUI:
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url.rstrip('/')
        self.root = ttk.Window(themename="journal")  # Red-accent theme
        self.root.title("PUP Student Grade System")
        self.root.geometry("1200x750")  # Bigger window
        self.root.minsize(1100, 650)

        self.student_id = None
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Segoe UI', 11))
        self.style.configure('TLabel', font=('Segoe UI', 11))

        self.create_login_window()

    def create_login_window(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(expand=True)

        card = ttk.Frame(main_frame, padding=30, bootstyle="light", relief="ridge")
        card.pack(pady=50)

        ttk.Label(
            card,
            text="PUP Student Grade System",
            font=("Segoe UI", 22, "bold"),
            bootstyle="danger"
        ).pack(pady=(0, 20))

        ttk.Label(card, text="Student ID", font=("Segoe UI", 12)).pack(anchor="w")
        self.id_entry = ttk.Entry(card, width=25, font=("Segoe UI", 11))
        self.id_entry.pack(pady=10)
        self.id_entry.focus()

        ttk.Button(
            card,
            text="Login",
            bootstyle="danger",
            width=20,
            command=self.handle_login
        ).pack(pady=(10, 5))

        self.id_entry.bind("<Return>", lambda e: self.handle_login())

    def handle_login(self):
        student_id = self.id_entry.get().strip()
        if not re.match(r'^S\d{4}$', student_id):
            messagebox.showerror("Invalid ID", "Format: S1234")
            self.id_entry.delete(0, tk.END)
            return

        try:
            response = requests.get(f"{self.api_base_url}/api/grades/{student_id}", timeout=5)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")
            return

        if 'error' in data:
            messagebox.showerror("Login Failed", data['error'])
            self.id_entry.delete(0, tk.END)
            return

        self.student_id = student_id
        self.student_data = data
        self.create_grades_window()

    def create_grades_window(self):
        self.clear_window()

        ttk.Label(
            self.root,
            text=f"{self.student_data['name']} (ID: {self.student_id})",
            font=("Segoe UI", 20, "bold"),
            bootstyle="danger"
        ).pack(pady=(30, 10))

        # Elegant center container
        container = ttk.Frame(self.root)
        container.pack(expand=True)

        card = ttk.Frame(container, padding=25, bootstyle="light", relief="ridge")
        card.pack(padx=30, pady=10)

        if not self.student_data['grades']:
            ttk.Label(card, text="No grades found.", font=("Segoe UI", 12, "italic")).pack(pady=20)
        else:
            for semester, details in self.student_data['grades'].items():
                semester_frame = ttk.Labelframe(card, text=semester, padding=15, bootstyle="danger")
                semester_frame.pack(pady=15)

                # Wider Treeview for bigger table but still centered
                tree = ttk.Treeview(
                    semester_frame,
                    columns=("Subject", "Units", "Grade", "Status"),
                    show="headings",
                    height=15,  # Bigger height
                    bootstyle="danger"
                )
                tree.pack(pady=5)

                tree.heading("Subject", text="Subject")
                tree.heading("Units", text="Units")
                tree.heading("Grade", text="Grade")
                tree.heading("Status", text="Status")

                tree.column("Subject", width=600, anchor="w")
                tree.column("Units", width=100, anchor="center")
                tree.column("Grade", width=100, anchor="center")
                tree.column("Status", width=200, anchor="center")

                for subj in details['subjects']:
                    tree.insert("", "end", values=(
                        subj['subject'],
                        subj['units'],
                        subj['grade'],
                        subj['status']
                    ))

                ttk.Label(
                    semester_frame,
                    text=f"GPA: {details['gpa']}",
                    font=("Segoe UI", 11, "italic"),
                    bootstyle="secondary"
                ).pack(anchor="e", pady=(5, 0))

        ttk.Button(
            self.root,
            text="← Logout",
            bootstyle="danger-outline",
            width=15,
            command=self.create_login_window
        ).pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    api_url = "http://127.0.0.1:5000"
    app = StudentSystemGUI(api_url)
    app.run()
