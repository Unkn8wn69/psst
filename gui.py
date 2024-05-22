import tkinter as tk
import customtkinter as ctk
import webbrowser
from PIL import Image
import os
import subprocess

# Local Imports
from about import create_about_page
from create import create_create_page
from recover import *
from consts import *

tabs = ["Create", "Recover", "About"]
current_tab = "About"

# Dependency functions

def check_directory_exists(directory_path):
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

def clone_repo(popup):
    ctk.CTkLabel(popup, text="Installing python-shamir-mnemonic", font=("Roboto", 15), text_color=SEL_BUTTON_FG).pack(pady=0)

    Label = ctk.CTkLabel(popup, text="Loading...")
    Label.pack(pady=5)

    error_textbox = ctk.CTkTextbox(popup, height=10, state="normal")
    error_textbox.pack(pady=(5), padx=10, fill="both", expand=True)

    cmd = "git clone https://github.com/trezor/python-shamir-mnemonic"
    result = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode == 0:
        Label.configure(text="Done")
        error_textbox.pack_forget() 
        popup.after(200, popup.destroy)
    else:
        Label.configure(text="Error occurred, see details below:")

        error_message = result.stderr.strip() if result.stderr else "Failed to clone repository."
        error_textbox.insert("1.0", error_message)

def show_progress_window(parent):
    popup = ctk.CTkToplevel(parent)
    popup.geometry("550x350")
    popup.minsize(550, 350)
    popup.title("Downloading Dependencies")
    popup.focus()
    popup.after(100, lambda: clone_repo(popup))


def check_and_clone_dependency(app):
    if not check_directory_exists("python-shamir-mnemonic"):
        show_progress_window(app)
    else:
        print("All dependencies already installed.")

# Tab-Content Functions

def clear_main_content():
    for widget in main_content_frame.winfo_children():
        widget.destroy()

def update_main_content(tab):
    clear_main_content()
    if tab == "About":
        create_about_page(main_content_frame, switch_tab)
    elif tab == "Create":
        create_create_page(main_content_frame)
    elif tab == "Recover":
        create_recover_page(main_content_frame)

# Top bar functions

def switch_tab(tab):
    global current_tab
    current_tab = tab
    update_tab_buttons()
    update_main_content(current_tab)

def open_github():
    webbrowser.open(GITHUB_URL)

def tab_buttons(top_bar):
    for tab in tabs:
        button = ctk.CTkButton(top_bar, text=tab, command=lambda tab=tab: switch_tab(tab))
        button.pack(side="left", padx=5)
        button.tab_name = tab
        if tab == current_tab:
            button.configure(fg_color=SEL_BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="black", height=32)
        else:
            button.configure(fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="white", height=30)

def update_tab_buttons():
    for widget in app.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            for button in widget.winfo_children():
                if isinstance(button, ctk.CTkButton) and hasattr(button, 'tab_name'):
                    if button.tab_name == current_tab:
                        button.configure(fg_color=SEL_BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="black", height=32)
                    else:
                        button.configure(fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="white", height=30)

def create_top_bar(parent):
    top_bar = ctk.CTkFrame(parent, height=50)
    top_bar.pack(side="top", fill="x")

    title_label = ctk.CTkLabel(top_bar, text="Polyseed Secret Sharing Tool", font=("Roboto", 20), anchor="w")
    title_label.pack(side="left", padx=(10, 20))

    tab_buttons(top_bar)

    github_icon = ctk.CTkImage(dark_image=Image.open(GITHUB_LOGO_PATH), size=(45,45))
    github_icon_label = ctk.CTkLabel(top_bar, text="", image=github_icon, cursor="hand2")

    github_icon_label.pack(side="right", padx=10, pady=5)
    github_icon_label.bind("<Button-1>", lambda event: open_github())

    version_label = ctk.CTkLabel(top_bar, text=f"v{APP_VERSION}", anchor="e")
    version_label.pack(side="right")

    github_icon_label.image = github_icon

# Start of the application

app = ctk.CTk()
app.title(APP_TITLE)
app.geometry(APP_GEOMETRY)
app.minsize(int(APP_GEOMETRY.split("x")[0]), int(APP_GEOMETRY.split("x")[1]))
ctk.set_appearance_mode("dark")

create_top_bar(app)

main_content_frame = ctk.CTkFrame(app)
main_content_frame.pack(fill="both", expand=True)

check_and_clone_dependency(app)

update_main_content(current_tab)

app.mainloop()