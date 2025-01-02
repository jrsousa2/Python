import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Function to be called when the button is clicked
def migrate_action(old_drive_var,new_drive_var):
    old_drive = old_drive_var.get()
    new_drive = new_drive_var.get()
    message_label = ttk.Label(root, text=f"Updating track location from {old_drive} to {new_drive}")
    message_label.pack(pady=10)
    # Display a message box and wait for user to press "OK"
    messagebox.showinfo("Press Enter to Continue", "Press OK to finish...")
    root.quit()  # Close the Tkinter main loop

def execute_and_show_widgets():
    # Label and Entry for "Old Drive"
    old_drive_label = ttk.Label(root, text="Enter Old drive:")
    old_drive_label.pack(pady=5)

    old_drive_var = tk.StringVar()
    old_drive_entry = ttk.Entry(root, textvariable=old_drive_var)
    old_drive_entry.pack(pady=5)

    # Label and Entry for "New Drive"
    new_drive_label = ttk.Label(root, text="Enter New drive:")
    new_drive_label.pack(pady=5)

    new_drive_var = tk.StringVar()
    new_drive_entry = ttk.Entry(root, textvariable=new_drive_var)
    new_drive_entry.pack(pady=5)

    # RETURN
    dict = {}
    dict["old"] = old_drive_var
    dict["new"] = new_drive_var
    return dict

def on_enter_pressed(event):
    if event.keysym == "Return":
        #message_label.pack_forget()  # Remove message label
        #old_drive_var, new_drive_var = execute_and_show_widgets()

        # Create the "Migrate" button
        #migrate_button = tk.Button(root, text="Migrate", command=lambda: migrate_action(old_drive_var, new_drive_var))
        #migrate_button.pack(pady=20)

        # Unbind the Enter key after it's used
        root.unbind('<Return>')

# Create the main window
root = tk.Tk()
root.title("iTunes Library Drive Migration Tool")

# Add the message label
message_label = ttk.Label(root, text="Reading XML file...")
message_label.pack(pady=10)

# Set the size of the window (width x height)
root.geometry("400x400")

# Add the message label
message_label = ttk.Label(root, text="Press enter to continue...")
message_label.pack(pady=10)
input("Press Enter to continue...")

# Bind Enter key press event to function
#root.bind('<Return>', on_enter_pressed)

dict = execute_and_show_widgets()
old_drive_var = dict["old"] 
new_drive_var = dict["new"]

# Create the "Migrate" button
migrate_button = tk.Button(root, text="Update track location", command=lambda: migrate_action(old_drive_var, new_drive_var))
# migrate_button = tk.Button(root, text="Migrate", command=migrate_action)
migrate_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
