import tkinter as tk
import customtkinter as ctk
import webbrowser
from consts import *

# Constants
TEXT_COLOR = "white"
groups = [{"name": "test", "shares": 5, "threshold": 1, "needed": True}]

def group_table(frame):
    name = ctk.CTkLabel(master=frame, text="Name")
    name.grid(row=0, column=0, padx=(20, 60))

    shares = ctk.CTkLabel(master=frame, text="Shares")
    shares.grid(row=0, column=1, padx=20)

    threshold = ctk.CTkLabel(master=frame, text="Threshold")
    threshold.grid(row=0, column=2, padx=20)

    needed = ctk.CTkLabel(master=frame, text="Needed?")
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

def create_create_page(parent):
    create_frame = ctk.CTkFrame(parent, fg_color=parent.cget("fg_color"))
    create_frame.pack(fill="both", expand=True, padx=20, pady=20)

    textbox = ctk.CTkTextbox(master=create_frame, width=400, height=100, corner_radius=15)
    textbox.pack(anchor="nw", pady=(0,15))

    group_header = ctk.CTkLabel(master=create_frame, text="Groups", font=("Roboto", 20))
    group_header.pack(anchor="nw")

    table_frame = ctk.CTkFrame(master=create_frame)
    table_frame.pack(fill="both", expand=True, pady=20)

    button_frame = ctk.CTkFrame(create_frame, fg_color=create_frame.cget("fg_color"))
    button_frame.pack()

    create_button = ctk.CTkButton(master=button_frame, text="Generate Shares")
    create_button.pack(side="right", anchor="se", padx=50)

    add_button = ctk.CTkButton(master=button_frame, text="Add Group")
    add_button.pack(side="right", anchor="se", padx=50)

    group_table(table_frame)

    generate_groups(table_frame)

    return create_frame