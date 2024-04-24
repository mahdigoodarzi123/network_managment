import tkinter as tk
from tkinter import messagebox
import sqlite3
from remote import rdp  


def create_database():
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS credentials
                 (label_name TEXT, host_ip TEXT, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()


def add_credential():
    label_name = entry_label_name.get()
    host_ip = entry_host_ip.get()
    username = entry_username.get()
    password = entry_password.get()

    if label_name and host_ip and username and password:
        conn = sqlite3.connect('credentials.db')
        c = conn.cursor()
        c.execute("INSERT INTO credentials VALUES (?, ?, ?, ?)", (label_name, host_ip, username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Credential Added", "Credential has been added successfully!")
        refresh_credential_buttons() 
    else:
        messagebox.showerror("Error", "Please fill in all fields.")



def connect_to_rdp(ip, username, password):
    rdp(ip, username, password)
    messagebox.showinfo("RDP Connection", "Connected successfully!")



def remove_credential(label_name):
    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("DELETE FROM credentials WHERE label_name=?", (label_name,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Credential Removed", "Credential has been removed successfully!")
    refresh_credential_buttons() 



def refresh_credential_buttons():
    for widget in credential_buttons_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('credentials.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credentials")
    credentials = c.fetchall()
    conn.close()


    for cred in credentials:
        label_name, host_ip, username, _ = cred
        button_frame = tk.Frame(credential_buttons_frame, bg="#f0f0f0", bd=1, relief=tk.RAISED)
        button_frame.pack(pady=5, fill=tk.X)
        
        button = tk.Button(button_frame, text=label_name, font=("Arial", 10), bg="#007bff", fg="white", padx=10, pady=5, command=lambda ip=host_ip, user=username: connect_to_rdp(ip, user, entry_password.get()))
        button.pack(side=tk.LEFT, padx=(5, 0), pady=2)

        remove_button = tk.Button(button_frame, text="Remove", font=("Arial", 10), bg="#dc3545", fg="white", padx=10, pady=5, command=lambda label=label_name: remove_credential(label))
        remove_button.pack(side=tk.RIGHT, padx=(0, 5), pady=2)


root = tk.Tk()
root.title("Credential Manager")
root.geometry("500x400")


create_database()


add_credential_frame = tk.LabelFrame(root, text="Add Credential", font=("Arial", 12), padx=10, pady=10)
add_credential_frame.pack(padx=10, pady=10, fill="both", expand=True)

label_label_name = tk.Label(add_credential_frame, text="Label Name:", font=("Arial", 10))
label_label_name.grid(row=0, column=0, padx=10, pady=5)
entry_label_name = tk.Entry(add_credential_frame, font=("Arial", 10))
entry_label_name.grid(row=0, column=1, padx=10, pady=5)

label_host_ip = tk.Label(add_credential_frame, text="Host IP:", font=("Arial", 10))
label_host_ip.grid(row=1, column=0, padx=10, pady=5)
entry_host_ip = tk.Entry(add_credential_frame, font=("Arial", 10))
entry_host_ip.grid(row=1, column=1, padx=10, pady=5)

label_username = tk.Label(add_credential_frame, text="Username:", font=("Arial", 10))
label_username.grid(row=2, column=0, padx=10, pady=5)
entry_username = tk.Entry(add_credential_frame, font=("Arial", 10))
entry_username.grid(row=2, column=1, padx=10, pady=5)

label_password = tk.Label(add_credential_frame, text="Password:", font=("Arial", 10))
label_password.grid(row=3, column=0, padx=10, pady=5)
entry_password = tk.Entry(add_credential_frame, font=("Arial", 10))
entry_password.grid(row=3, column=1, padx=10, pady=5)

add_button = tk.Button(add_credential_frame, text="Add Credential", font=("Arial", 10), bg="#28a745", fg="white", command=add_credential)
add_button.grid(row=4, columnspan=2, padx=10, pady=5)


credential_buttons_frame = tk.LabelFrame(root, text="Saved Credentials", font=("Arial", 12), padx=10, pady=10)
credential_buttons_frame.pack(padx=10, pady=10, fill="both", expand=True)


refresh_credential_buttons()

root.mainloop()
