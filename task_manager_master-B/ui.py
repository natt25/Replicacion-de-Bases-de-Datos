import tkinter as tk
from tkinter import ttk, messagebox
from db import Database

class TaskManagerUI:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("650x400")

        # Formulario
        self.title_var = tk.StringVar()
        self.desc_var = tk.StringVar()
        self.status_var = tk.StringVar(value="pendiente")

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Título:").grid(row=0, column=0)
        tk.Entry(form_frame, textvariable=self.title_var, width=40).grid(row=0, column=1)

        tk.Label(form_frame, text="Descripción:").grid(row=1, column=0)
        tk.Entry(form_frame, textvariable=self.desc_var, width=40).grid(row=1, column=1)

        tk.Label(form_frame, text="Estado:").grid(row=2, column=0)
        ttk.Combobox(
            form_frame,
            textvariable=self.status_var,
            values=["pendiente", "en progreso", "completado"],
            width=37
        ).grid(row=2, column=1)

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Crear", command=self.create_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.update_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.delete_task).grid(row=0, column=2, padx=5)

        # Tabla
        self.tree = ttk.Treeview(root, columns=("ID", "Título", "Descripción", "Estado"), show="headings")
        self.tree.pack(fill="both", expand=True, pady=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Estado", text="Estado")

        self.tree.bind("<ButtonRelease-1>", self.populate_fields)

        self.load_tasks()

    def load_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        tasks = self.db.fetch()

        # MySQL devuelve diccionarios → convertirlos a tuplas
        for t in tasks:
            self.tree.insert("", tk.END, values=(t["id"], t["titulo"], t["descripcion"], t["estado"]))

    def create_task(self):
        self.db.insert(
            self.title_var.get(),
            self.desc_var.get(),
            self.status_var.get()
        )
        self.load_tasks()
        self.clear_fields()

    def update_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona una tarea para actualizar.")
            return

        item = self.tree.item(selected)
        task_id = item["values"][0]

        self.db.update(
            task_id,
            self.title_var.get(),
            self.desc_var.get(),
            self.status_var.get()
        )
        self.load_tasks()
        self.clear_fields()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona una tarea para eliminar.")
            return

        item = self.tree.item(selected)
        task_id = item["values"][0]

        self.db.delete(task_id)
        self.load_tasks()
        self.clear_fields()

    def populate_fields(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        task = self.tree.item(selected)["values"]

        self.title_var.set(task[1])
        self.desc_var.set(task[2])
        self.status_var.set(task[3])

    def clear_fields(self):
        self.title_var.set("")
        self.desc_var.set("")
        self.status_var.set("pendiente")
