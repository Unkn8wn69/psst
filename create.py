import tkinter as tk
import customtkinter as ctk
import webbrowser
from consts import *

# Constants
groups = []

def group_table(frame):
    name = ctk.CTkLabel(master=frame, text="Name")
    name.grid(row=0, column=0, padx=(20, 60))

    shares = ctk.CTkLabel(master=frame, text="Shares")
    shares.grid(row=0, column=1, padx=20)

    threshold = ctk.CTkLabel(master=frame, text="Threshold")
    threshold.grid(row=0, column=2, padx=20)

    needed = ctk.CTkLabel(master=frame, text="Needed1")
    needed.grid(row=0, column=3, padx=20)

    options = ctk.CTkLabel(master=frame, text="Options")
    options.grid(row=0, column=4, padx=20)

    separator = ctk.CTkFrame(master=frame, height=2, fg_color="grey")
    separator.grid(row=1, columnspan=5, sticky='ew', padx=20, pady=(5, 5))

def delete_group(index, frame):
    global groups
    groups.pop(index)

    for widget in frame.winfo_children():
        widget.destroy()

    group_table(frame)
    generate_groups(frame)

def generate_groups(frame):
    global groups
    print(groups)
    row_index = 2
    for index, group in enumerate(groups):
        name = ctk.CTkLabel(master=frame, text=group["name"])
        name.grid(row=row_index, column=0, padx=(20, 60))

        shares = ctk.CTkLabel(master=frame, text=group["shares"])
        shares.grid(row=row_index, column=1, padx=20)

        threshold = ctk.CTkLabel(master=frame, text=group["threshold"])
        threshold.grid(row=row_index, column=2, padx=20)

        needed = ctk.CTkLabel(master=frame, text=str(group["needed"]))
        needed.grid(row=row_index, column=3, padx=20)

        delete = ctk.CTkButton(master=frame, text="Delete", command=lambda index=index: delete_group(index, frame))
        delete.grid(row=row_index, column=4, padx=20)

        row_index += 1

def add_group_popup(table_frame, parent):
    popup = ctk.CTkToplevel(parent)
    popup.geometry("350x250")
    popup.minsize(350, 250)
    popup.title("Add Group")

    row_index = 0

    # Name Entry
    name_label = ctk.CTkLabel(popup, text="Name:")
    name_label.grid(row=row_index, column=0, pady=(10, 0), sticky="w", padx=(20,10))
    name_entry = ctk.CTkEntry(popup)
    name_entry.grid(row=row_index, column=1, pady=(10, 0), sticky="ew", padx=20)
    row_index += 1

    # Number of Shares Entry
    shares_label = ctk.CTkLabel(popup, text="Number of Shares:")
    shares_label.grid(row=row_index, column=0, pady=(10, 0), sticky="w", padx=(20,10))
    shares_entry = ctk.CTkEntry(popup)
    shares_entry.grid(row=row_index, column=1, pady=(10, 0), sticky="ew", padx=20)
    row_index += 1

    # Threshold of Shares Entry
    threshold_label = ctk.CTkLabel(popup, text="Threshold of Shares:")
    threshold_label.grid(row=row_index, column=0, pady=(10, 0), sticky="w", padx=(20,10))
    threshold_entry = ctk.CTkEntry(popup)
    threshold_entry.grid(row=row_index, column=1, pady=(10, 0), sticky="ew", padx=20)
    row_index += 1

    # Checkbox for Needed
    needed_var = tk.BooleanVar()
    needed_check = ctk.CTkCheckBox(popup, text="Needed for Seed Recovery?", variable=needed_var, onvalue=True, offvalue=False)
    needed_check.grid(row=row_index, column=0, columnspan=2, pady=(10, 0), padx=20)
    row_index += 1

    # Submit Button
    submit_button = ctk.CTkButton(popup, text="Add Group", command=lambda: submit_group(table_frame, name_entry.get(), shares_entry.get(), threshold_entry.get(), needed_var.get(), popup, error_label))
    submit_button.grid(row=row_index, column=0, columnspan=2, pady=(20, 0), padx=20)

    # Error field

    error_label = ctk.CTkLabel(master=popup, text="", text_color="red", font=("Roboto", 12))
    error_label.grid(row=row_index+1, columnspan=5)

    popup.grid_columnconfigure(1, weight=1)


def submit_group(table_frame, name, shares, threshold, needed, popup, error_label):
    global groups
    if name == "" or shares == "" or threshold == "":
        error_label.configure(text="Please fill out all fields")
    else:
        try: 
            shares_int = int(shares)
            threshold_int = int(threshold)
        except ValueError:
            error_label.configure(text="Please enter valid numbers for shares and threshold.")
        finally:
            if int(threshold) > int(shares):
                error_label.configure(text="Threshold can't be higher than number of shares!")
            else:
                    shares_int = int(shares)
                    threshold_int = int(threshold)
                    print(needed)

                    groups.append({"name": name, "shares": shares_int, "threshold": threshold_int, "needed": needed})
                    popup.destroy()
                    generate_groups(table_frame)

def generate_shares():
    global groups
    
    shares = len(groups)
    shares_to_complete = 0
    for group in groups:
        if group["needed"] == True:
            shares_to_complete += 1

    print(shares)
    print(shares_to_complete)


def create_create_page(parent):
    create_frame = ctk.CTkFrame(parent, fg_color=parent.cget("fg_color"))
    create_frame.pack(fill="both", expand=True, padx=20, pady=20)

    group_header = ctk.CTkLabel(master=create_frame, text="Seed", font=("Roboto", 20))
    group_header.pack(anchor="nw", pady=(0, 10))

    textbox = ctk.CTkTextbox(master=create_frame, width=400, height=100, corner_radius=15)
    textbox.pack(anchor="nw", pady=(0,15))

    group_header = ctk.CTkLabel(master=create_frame, text="Groups", font=("Roboto", 20))
    group_header.pack(anchor="nw")

    table_frame = ctk.CTkFrame(master=create_frame)
    table_frame.pack(fill="both", expand=True, pady=20)

    button_frame = ctk.CTkFrame(create_frame, fg_color=create_frame.cget("fg_color"))
    button_frame.pack()

    create_button = ctk.CTkButton(master=button_frame, text="Generate Shares", command=generate_shares())
    create_button.pack(side="right", anchor="se", padx=50)

    add_button = ctk.CTkButton(master=button_frame, text="Add Group", command=lambda: add_group_popup(table_frame, create_frame))
    add_button.pack(side="right", anchor="se", padx=50)

    group_table(table_frame)

    generate_groups(table_frame)

    return create_frame