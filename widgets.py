import tkinter as tk
import customtkinter as ctk
from consts import *

def mainButton(master, text, command=None, width=None, height=None, text_color="white"):

    options = {
        "master": master,
        "text": text,
        "fg_color": BUTTON_FG,
        "hover_color": SEL_BUTTON_FG,
        "cursor": "hand2",
        "text_color": text_color,
    }

    if width is not None:
        options["width"] = width
    if height is not None:
        options["height"] = height
    if command is not None:
        options["command"] = command
    button = ctk.CTkButton(**options)
    return button