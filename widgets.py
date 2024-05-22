import tkinter as tk
import customtkinter as ctk
from consts import *

def mainButton(master, text, command, width=None, height=None, text_color="white"):

    options = {
        "master": master,
        "text": text,
        "fg_color": BUTTON_FG,
        "hover_color": SEL_BUTTON_FG,
        "cursor": "hand2",
        "text_color": text_color,
        "command": command
    }

    if width is not None:
        options["width"] = width
    if height is not None:
        options["height"] = height
    button = ctk.CTkButton(**options)
    return button