import tkinter as tk
import customtkinter as ctk
import webbrowser

# Local Imports
from about import create_about_page
from create import create_create_page
from consts import *

tabs = ["Create", "Recover", "About"]
current_tab = "About"

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

# Top bar functions

def switch_tab(tab):
    global current_tab
    current_tab = tab
    print(f"Tab changed to: {tab}")
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
            button.configure(fg_color=SEL_BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="black")
        else:
            button.configure(fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="white")

def update_tab_buttons():
    for widget in app.winfo_children():
        if isinstance(widget, ctk.CTkFrame):
            for button in widget.winfo_children():
                if isinstance(button, ctk.CTkButton) and hasattr(button, 'tab_name'):
                    if button.tab_name == current_tab:
                        button.configure(fg_color=SEL_BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="black")
                    else:
                        button.configure(fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG, text_color="white")

def create_top_bar(parent):
    top_bar = ctk.CTkFrame(parent, height=50)
    top_bar.pack(side="top", fill="x")

    title_label = ctk.CTkLabel(top_bar, text="Polyseed Secret Sharing Tool", font=("Roboto", 20), anchor="w")
    title_label.pack(side="left", padx=(10, 20))

    tab_buttons(top_bar)

    original_icon = tk.PhotoImage(file=GITHUB_LOGO_PATH)
    small_icon = original_icon.subsample(6, 6)
    icon_label = ctk.CTkLabel(top_bar, text="", image=small_icon, cursor="hand2")
    icon_label.pack(side="right", padx=10, pady=5)
    icon_label.bind("<Button-1>", lambda event: open_github())

    version_label = ctk.CTkLabel(top_bar, text=f"v{APP_VERSION}", anchor="e")
    version_label.pack(side="right")

    icon_label.image = small_icon

# Start of the application

app = ctk.CTk()
app.title(APP_TITLE)
app.geometry(APP_GEOMETRY)
app.minsize(int(APP_GEOMETRY.split("x")[0]), int(APP_GEOMETRY.split("x")[1]))
ctk.set_appearance_mode("dark")

create_top_bar(app)

main_content_frame = ctk.CTkFrame(app)
main_content_frame.pack(fill="both", expand=True)

update_main_content(current_tab)

app.mainloop()