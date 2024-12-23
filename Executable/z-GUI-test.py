import tkinter as tk
from tkinter import ttk

# Function to be called when the button is clicked
def migrate_action(old_drive_var,new_drive_var):
    old_drive = old_drive_var.get()
    new_drive = new_drive_var.get()
    print(f"Updating track location from {old_drive} to {new_drive}")

# Function that executes certain code and then shows the entry fields and button
def execute_and_show_widgets():
    # Label and Entry for "Old Drive"
    old_drive_label = ttk.Label(root, text="Old Drive:")
    old_drive_label.pack(pady=5)

    old_drive_entry = ttk.Entry(root, textvariable=old_drive_var)
    old_drive_entry.pack(pady=5)

    # Label and Entry for "New Drive"
    new_drive_label = ttk.Label(root, text="New Drive:")
    new_drive_label.pack(pady=5)

    new_drive_entry = ttk.Entry(root, textvariable=new_drive_var)
    new_drive_entry.pack(pady=5)

    # Create the "Migrate" button
    migrate_button = tk.Button(root, text="Migrate", command=migrate_action)
    migrate_button.pack(pady=20)

    # RETURN
    dict = {}
    dict["old"] = old_drive_var
    dict["new"] = new_drive_var
    return dict

# Create the main window
root = tk.Tk()
root.title("Drive Migration Tool")

# Set the size of the window (width x height)
root.geometry("400x300")

# Add the message label
message_label = ttk.Label(root, text="Reading XML file...")
message_label.pack(pady=10)

message_label = ttk.Label(root, text="Press Enter to continue...")
message_label.pack(pady=10)

# Execute the function and show widgets
dict = execute_and_show_widgets()
old_drive_var = dict["old"] 
new_drive_var = dict["new"]

# Create the "Migrate" button
migrate_button = tk.Button(root, text="Migrate", command=lambda: migrate_action(old_drive_var.get(), new_drive_var.get()))
# migrate_button = tk.Button(root, text="Migrate", command=migrate_action)
migrate_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
