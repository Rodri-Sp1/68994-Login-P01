# Royfran Rodrigo Santini Pacheco Tercer Semestre ITS
import tkinter as tk
from tkinter import messagebox
import hashlib
import os
import json

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Login")
        self.root.geometry("400x300")
        self.root.configure(bg='#f0f0f0')

        # Archivo donde se guardan los usuarios
        self.db_file = "users.json"
        self.users = self.load_users()

        self.create_widgets()

    def load_users(self):
        """Carga usuarios desde el archivo si existe, sino arranca vacío"""
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {}

    def save_users(self):
        """Guarda los usuarios en el archivo JSON"""
        with open(self.db_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def hash_password(self, password):
        """Convierte la contraseña en un hash seguro"""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        # Título
        title_label = tk.Label(
            main_frame,
            text="Inicio de Sesión",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=(0, 30))

        # Frame de entradas
        input_frame = tk.Frame(main_frame, bg='#f0f0f0')
        input_frame.pack(pady=10)

        # Usuario
        user_label = tk.Label(input_frame, text="Usuario:", font=('Arial', 12),
                              bg='#f0f0f0', anchor='w', width=15)
        user_label.grid(row=0, column=0, padx=5, pady=10, sticky='w')

        self.user_entry = tk.Entry(input_frame, font=('Arial', 12), width=20)
        self.user_entry.grid(row=0, column=1, padx=5, pady=10)
        self.user_entry.focus()

        # Contraseña
        pass_label = tk.Label(input_frame, text="Contraseña:", font=('Arial', 12),
                              bg='#f0f0f0', anchor='w', width=15)
        pass_label.grid(row=1, column=0, padx=5, pady=10, sticky='w')

        self.pass_entry = tk.Entry(input_frame, font=('Arial', 12), width=20, show='*')
        self.pass_entry.grid(row=1, column=1, padx=5, pady=10)
        self.pass_entry.bind('<Return>', lambda event: self.login())

        # Botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)

        login_btn = tk.Button(button_frame, text="Iniciar Sesión",
                              font=('Arial', 12, 'bold'),
                              bg='#4CAF50', fg='white', width=12,
                              command=self.login)
        login_btn.pack(pady=5)

        signup_btn = tk.Button(button_frame, text="Registrarse",
                               font=('Arial', 12, 'bold'),
                               bg="#4C65AF", fg='white', width=12,
                               command=self.signin)
        signup_btn.pack(pady=1)

        clear_btn = tk.Button(button_frame, text="Limpiar",
                              font=('Arial', 10),
                              bg='#f44336', fg='white', width=10,
                              command=self.clear_fields)
        clear_btn.pack(pady=5)

    def signin(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Complete usuario y contraseña")
            return

        if username in self.users:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        # Guardar el nuevo usuario con su contraseña encriptada
        self.users[username] = self.hash_password(password)
        self.save_users()

        messagebox.showinfo("Registro", "Usuario registrado correctamente")
        self.clear_fields()

    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        if username in self.users:
            if self.users[username] == self.hash_password(password):
                messagebox.showinfo("Éxito", f"¡Bienvenido, {username}!")
                self.open_dashboard(username)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

    def clear_fields(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)
        self.user_entry.focus()

    def open_dashboard(self, username):
        self.root.destroy()

        dashboard = tk.Tk()
        dashboard.title("Dashboard Principal")
        dashboard.geometry("600x400")
        dashboard.configure(bg='#ffffff')

        welcome_label = tk.Label(
            dashboard,
            text=f"Bienvenido al Sistema, {username}!",
            font=('Arial', 16, 'bold'),
            bg='#ffffff',
            fg='#333333'
        )
        welcome_label.pack(pady=50)

        logout_btn = tk.Button(
            dashboard,
            text="Cerrar Sesión",
            font=('Arial', 12),
            bg='#ff9800',
            fg='white',
            command=dashboard.quit
        )
        logout_btn.pack(pady=20)

        dashboard.mainloop()


def main():
    root = tk.Tk()

    # Centrar ventana
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    app = LoginApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
