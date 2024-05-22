import tkinter as tk
import customtkinter as ctk
from consts import *

def mainButton(master, text, command, text_color="white"):
    button = ctk.CTkButton(
        master=master,
        text=text,
        fg_color=BUTTON_FG,
        hover_color=SEL_BUTTON_FG,
        cursor="hand2",
        text_color=text_color,
        command=command
    )
    return button