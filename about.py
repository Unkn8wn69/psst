import tkinter as tk
import customtkinter as ctk
import webbrowser
from consts import *

# Constants
TEXT_COLOR = "white"

def create_about_page(parent, switch_tab):
    about_frame = ctk.CTkFrame(parent)
    about_frame.pack(fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(
        about_frame,
        text="Polyseed Secret Sharing Tool",
        font=("Roboto", 24), anchor="center",
        text_color=TEXT_COLOR)
    title_label.pack(pady=(10, 20))

    # Description

    description_text = """
    PSST is a tool that splits a 16-word Monero seed into multiple parts, called shares.
    You can group these shares and define how many it needs of them to recreate the original seed.
    The tool uses Shamir's Secret Sharing Scheme, a well known Cryptographic Scheme to split the seed up.
    
    If you're ready to start:"""
    description_label = ctk.CTkLabel(
        about_frame,
        text=description_text,
        text_color=TEXT_COLOR,
        font=("Roboto", 15))
    description_label.pack()

    # Jump to create button

    create_tab_button = ctk.CTkButton(about_frame, text="Create a shared seed", command=lambda: switch_tab("Create"))
    create_tab_button.pack(pady=10)

    return about_frame