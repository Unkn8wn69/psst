import tkinter as tk
import customtkinter as ctk
import webbrowser
import json
from consts import *

# Constants
groups = []

def group_table(frame):
    header_padx = (10, 40)
    name_padx = (20, 50)

    ctk.CTkLabel(master=frame, text="Name").grid(row=0, column=0, padx=name_padx)
    ctk.CTkLabel(master=frame, text="Shares").grid(row=0, column=1, padx=header_padx)
    ctk.CTkLabel(master=frame, text="Threshold").grid(row=0, column=2, padx=header_padx)
    ctk.CTkLabel(master=frame, text="Needed").grid(row=0, column=3, padx=header_padx)
    ctk.CTkLabel(master=frame, text="Options").grid(row=0, column=4, padx=header_padx)
    
    separator = ctk.CTkFrame(master=frame, height=2, fg_color="grey")
    separator.grid(row=1, columnspan=7, sticky='ew', pady=(5, 5))

def delete_group(index, frame):
    global groups
    groups.pop(index)

    for widget in frame.winfo_children():
        widget.destroy()

    group_table(frame)
    generate_groups(frame)

def generate_groups(frame):
    global groups
    row_index = 2
    name_padx = (20, 50)
    column_padx = (10, 40)
    for index, group in enumerate(groups):
        ctk.CTkLabel(master=frame, text=group["name"]).grid(row=row_index, column=0, padx=name_padx)
        ctk.CTkLabel(master=frame, text=str(group["shares"])).grid(row=row_index, column=1, padx=column_padx)
        ctk.CTkLabel(master=frame, text=str(group["threshold"])).grid(row=row_index, column=2, padx=column_padx)
        
        needed = tk.BooleanVar(value=group["needed"])
        needed_checkbox = ctk.CTkCheckBox(master=frame, text="", variable=needed, onvalue=True, offvalue=False, state=ctk.DISABLED)
        needed_checkbox.grid(row=row_index, column=3, padx=(40, 0))
        
        delete_button = ctk.CTkButton(master=frame, text="Delete", width=50, height=20, command=lambda index=index: delete_group(index, frame))
        delete_button.grid(row=row_index, column=4, padx=column_padx)
        
        row_index += 1

def validate_input(textbox, error_label):
    with open('wordlist.json', 'r') as file:
        wordlist = json.load(file)
    
    input_words = textbox.get("1.0", "end-1c").strip().split(" ")
    
    if "\n" in textbox.get("1.0", "end-1c"):
        error_label.configure(text="Input must not contain new lines.")
        return
    if len(input_words) != 16:
        error_label.configure(text="Input must contain exactly 16 words.")
        return

    if not all(word in wordlist for word in input_words):
        error_label.configure(text="All words must be a correct polyseed words.")
        return

    error_label.configure(text="")

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
    elif any(group['name'] == name for group in groups):
        error_label.configure(text="Group already exists")
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

                    groups.append({"name": name, "shares": shares_int, "threshold": threshold_int, "needed": needed})
                    popup.destroy()
                    generate_groups(table_frame)

def generate_shares(textbox, error_label):
    global groups

    validate_input(textbox, error_label)
    
    shares = len(groups)
    shares_to_complete = 0
    for group in groups:
        if group["needed"] == True:
            shares_to_complete += 1
    
    


def create_create_page(parent):
    create_frame = ctk.CTkFrame(parent, fg_color=parent.cget("fg_color"))
    create_frame.pack(fill="both", expand=True, padx=20, pady=20)

    seed_header = ctk.CTkLabel(master=create_frame, text="Seed", font=("Roboto", 20))
    seed_header.pack(anchor="nw", pady=(0, 10))

    seed_frame = ctk.CTkFrame(master=create_frame, fg_color=parent.cget("fg_color"))
    seed_frame.pack(fill='x', pady=(0, 10))

    textbox = ctk.CTkTextbox(master=seed_frame, width=500, height=100, corner_radius=15)
    textbox.pack(side="left", padx=(0, 10), anchor="w")

    error_label = ctk.CTkLabel(master=seed_frame, text="", text_color="red")
    error_label.pack(side="right", padx=(10, 50))

    group_header = ctk.CTkLabel(master=create_frame, text="Groups", font=("Roboto", 20))
    group_header.pack(anchor="nw")

    table_frame = ctk.CTkFrame(master=create_frame)
    table_frame.pack(fill="both", expand=True, pady=20)

    button_frame = ctk.CTkFrame(create_frame, fg_color=create_frame.cget("fg_color"))
    button_frame.pack()

    create_button = ctk.CTkButton(master=button_frame, text="Generate Shares", command=lambda: generate_shares(textbox, error_label))
    create_button.pack(side="right", anchor="se", padx=50)

    add_button = ctk.CTkButton(master=button_frame, text="Add Group", command=lambda: add_group_popup(table_frame, create_frame))
    add_button.pack(side="right", anchor="se", padx=50)

    group_table(table_frame)

    generate_groups(table_frame)

    return create_frame