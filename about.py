import tkinter as tk
import customtkinter as ctk
from PIL import Image
import webbrowser
import consts
from consts import SEL_BUTTON_FG, BUTTON_FG

# Constants
TEXT_COLOR = "white"

def toggle_button_state(button, label, copied_label, qr_code_frame):
    # Toggle the visual state of the button and the visibility of the label
    if button.cget('fg_color') == BUTTON_FG:
        button.configure(fg_color=SEL_BUTTON_FG)
        label.pack(pady=(10, 0))
        copied_label.place(relx=1.0, rely=1.0, anchor="se")
    else:
        button.configure(fg_color=BUTTON_FG)
        qr_code_frame.configure(height=0)
        label.pack_forget()        
        copied_label.place_forget()

def copy_to_clipboard(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def create_about_page(parent, switch_tab):
    about_frame = ctk.CTkFrame(parent)
    about_frame.pack(fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(
        about_frame,
        text="Polyseed Secret Sharing Tool",
        font=("Roboto", 24), anchor="center",
        text_color=TEXT_COLOR)
    title_label.pack(pady=(20, 10))

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

    create_tab_button = ctk.CTkButton(
        about_frame,
        text="Create a shared seed",
        fg_color=SEL_BUTTON_FG, hover_color=SEL_BUTTON_FG,
        cursor="hand2",
        font=("Roboto", 16),
        text_color="black",
        command=lambda: switch_tab("Create"))
    create_tab_button.pack(pady=(5, 20))

    # title

    more_info_text = "More Info:"
    more_info_label = ctk.CTkLabel(
        about_frame,
        text=more_info_text,
        text_color=TEXT_COLOR,
        font=("Roboto", 15))
    more_info_label.pack()

    # More Info Section
    more_info_frame = ctk.CTkFrame(about_frame, fg_color=about_frame.cget("fg_color"))
    more_info_frame.pack(pady=(0, 0))

    # GitHub Link
    github_button = ctk.CTkButton(
        more_info_frame,
        text="GitHub Repository",
        fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG,
        cursor="hand2",
        text_color="white",
        command=lambda: webbrowser.open("https://github.com/Unkn8wn69/psst"))
    github_button.pack(side="left", padx=(0, 10))

    # SSSS Info Link
    ssss_info_button = ctk.CTkButton(
        more_info_frame,
        text="What is SSSS?",
        fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG,
        cursor="hand2",
        text_color="white",
        command=lambda: webbrowser.open("https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing"))
    ssss_info_button.pack(side="right")

    # Donation Text
    donation_label = ctk.CTkLabel(
        about_frame,
        text="Support with Monero: (Click to Copy or QR)",
        font=("Roboto", 14),
        text_color="white")
    donation_label.pack(pady=(10,0))

    qr_code_frame = ctk.CTkFrame(about_frame, height=0, fg_color=about_frame.cget("fg_color"))
    qr_code_frame.pack(pady=(0, 10))

    # Monero Address Button
    monero_address_button = ctk.CTkButton(
        about_frame,
        fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG,
        cursor="hand2",
        text_color="black",
        text=consts.MONERO_ADDRESS,
        command=lambda: [copy_to_clipboard(about_frame, consts.MONERO_ADDRESS),
                         toggle_button_state(monero_address_button, qr_label, copied_label, qr_code_frame)]
    )
    monero_address_button.pack()

    # Load QR Code Image


    qr_image = ctk.CTkImage(dark_image=Image.open(consts.MONERO_QR_PATH), size=(115,115))
    qr_label = ctk.CTkLabel(qr_code_frame, text="", image=qr_image)
    

    # Label to show "address copied to clipboard" message
    copied_label = ctk.CTkLabel(about_frame,
        anchor="se",
        height=10,
        font=("Roboto", 15),
        text="Address copied to clipboard!",
        text_color="white")

    return about_frame