import tkinter as tk
import customtkinter as ctk
import webbrowser
from consts import *

# Constants
TEXT_COLOR = "white"
groups = []

def group_table(frame):
    name = ctk.CTkLabel(master=frame, text="Name")
    name.grid(row=0, column=0, padx=(20, 40))

    shares = ctk.CTkLabel(master=frame, text="Shares")
    shares.grid(row=0, column=1, padx=20)

    threshold = ctk.CTkLabel(master=frame, text="Threshold")
    threshold.grid(row=0, column=2, padx=20)

    needed = ctk.CTkLabel(master=frame, text="Needed?")
    needed.grid(row=0, column=3, padx=20)

    options = ctk.CTkLabel(master=frame, text="Options")
    options.grid(row=0, column=4, padx=20)

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

    return create_frame