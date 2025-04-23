import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import pyperclip
from random import choice, randint, shuffle
import os
print("🤖 Current working directory:", os.getcwd())


# --- Setup Window ---
root = ttk.Window(themename="flatly", iconphoto="")
root.title("🔐 Password Manager")
root.geometry("400x450")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "passwords.json")

# --- Password Generation Logic ---
def generate_password():
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")
    symbols = list("!#$%&()*+")

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, "end")
    password_entry.insert(0, password)
    status_label.config(text="✅ Password generated & copied!")
    return password

# --- Save Password Logic ---
def save_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not password:
        status_label.config(text="⚠️ Website and password required.")
        return

    new_data = {website: {"email": email, "password": password}}

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data.update(new_data)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)
    status_label.config(text=f"💾 Saved for {website}")

# --- Find Password Logic ---
def find_password():
    website = website_entry.get().strip()

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        status_label.config(text="🚫 No data file found.")
        return

    if website in data:
        creds = data[website]
        email_entry.delete(0, "end")
        email_entry.insert(0, creds["email"])
        password_entry.delete(0, "end")
        password_entry.insert(0, creds["password"])
        pyperclip.copy(creds["password"])
        status_label.config(text="🔍 Found! Password copied.")
    else:
        status_label.config(text="❌ No entry found.")

# --- Theme Dropdown ---
def change_theme(choice):
    root.style.theme_use(choice)

themes = root.style.theme_names()
theme_menu = ttk.Combobox(root, values=themes, bootstyle=INFO)
theme_menu.set("flatly")
theme_menu.pack(pady=10)
theme_menu.bind("<<ComboboxSelected>>", lambda e: change_theme(theme_menu.get()))

# --- Entry Fields ---
website_entry = ttk.Entry(root, width=30)
website_entry.pack(pady=5)
website_entry.insert(0, "example.com")

email_entry = ttk.Entry(root, width=30)
email_entry.pack(pady=5)
email_entry.insert(0, "user@example.com")

password_entry = ttk.Entry(root, width=30)
password_entry.pack(pady=5)

# --- Action Buttons ---
ttk.Button(root, text="🔐 Generate Password", command=generate_password, bootstyle="info").pack(pady=4)
ttk.Button(root, text="💾 Save Password", command=save_password, bootstyle="success").pack(pady=4)
ttk.Button(root, text="🔎 Find Password", command=find_password, bootstyle="warning").pack(pady=4)

# --- Status Message ---
status_label = ttk.Label(root, text="", bootstyle="secondary")
status_label.pack(pady=10)

# --- Start the GUI ---
root.mainloop()
