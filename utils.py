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

def center_popup(popup, parent, popup_width, popup_height):
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    x = parent_x + (parent_width - popup_width) // 2
    y = parent_y + (parent_height - popup_height) // 2

    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

def hex_to_seed(hex_string, wordlist):
    n = 3
    chunks = [hex_string[i:i+n] for i in range(0, len(hex_string), n)]
    seed = ' '.join(wordlist[int(chunk, 16)] for chunk in chunks)
    return seed