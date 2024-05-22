import tkinter as tk
import customtkinter as ctk
import webbrowser
import re
import json
import subprocess
from tkinter import filedialog, messagebox
from consts import *

# Constants
groups = []
seed = ""
group_threshold = 1

shares = []

# TODO: Make group table smaller and add small help / instruction field next to it

def group_table(frame):
    header_padx = (10, 40)
    name_padx = (20, 50)

    ctk.CTkLabel(master=frame, text="Name").grid(row=0, column=0, padx=name_padx)
    ctk.CTkLabel(master=frame, text="Shares").grid(row=0, column=1, padx=header_padx)
    ctk.CTkLabel(master=frame, text="Threshold").grid(row=0, column=2, padx=header_padx)
    ctk.CTkLabel(master=frame, text="Options").grid(row=0, column=4, padx=header_padx)
    
    separator = ctk.CTkFrame(master=frame, height=2, fg_color="grey")
    separator.grid(row=1, columnspan=7, sticky='ew', pady=(5, 5))

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
    name_padx = (20, 50)
    column_padx = (10, 40)
    for index, group in enumerate(groups):
        ctk.CTkLabel(master=frame, text=group["name"]).grid(row=row_index, column=0, padx=name_padx)
        ctk.CTkLabel(master=frame, text=str(group["shares"])).grid(row=row_index, column=1, padx=column_padx)
        ctk.CTkLabel(master=frame, text=str(group["threshold"])).grid(row=row_index, column=2, padx=column_padx)
        
        delete_button = ctk.CTkButton(master=frame, text="Delete", width=50, height=20, command=lambda index=index: delete_group(index, frame))
        delete_button.grid(row=row_index, column=4, padx=column_padx)
        
        row_index += 1

def add_group_popup(table_frame, parent):
    popup = ctk.CTkToplevel(parent)
    popup.geometry("350x200")
    popup.minsize(350, 200)
    popup.title("Add Group")

    row_index = 0

    # Name Entry
    name_label = ctk.CTkLabel(popup, text="Name:")
    name_label.grid(row=row_index, column=0, pady=(10, 0), sticky="w", padx=(20,10))
    name_entry = ctk.CTkEntry(popup)
    name_entry.grid(row=row_index, column=1, pady=(10, 0), sticky="ew", padx=20)
    row_index += 1

    # Number of Shares Entry
    shares_label = ctk.CTkLabel(popup, text="Number of Shares:")
    shares_label.grid(row=row_index, column=0, pady=(10, 0), sticky="w", padx=(20,10))
    shares_entry = ctk.CTkEntry(popup)
    shares_entry.grid(row=row_index, column=1, pady=(10, 0), sticky="ew", padx=20)
    row_index += 1

    # Threshold of Shares Entry
    threshold_label = ctk.CTkLabel(popup, text="Threshold of Shares:")
    threshold_label.grid(row=row_index, column=0, pady=(10, 0), sticky="w", padx=(20,10))
    threshold_entry = ctk.CTkEntry(popup)
    threshold_entry.grid(row=row_index, column=1, pady=(10, 0), sticky="ew", padx=20)
    row_index += 1

    # Submit Button
    submit_button = ctk.CTkButton(popup, text="Add Group", command=lambda: submit_group(table_frame, name_entry.get(), shares_entry.get(), threshold_entry.get(), popup, error_label))
    submit_button.grid(row=row_index, column=0, columnspan=2, pady=(20, 0), padx=20)

    # Error field

    error_label = ctk.CTkLabel(master=popup, text="", text_color="red", font=("Roboto", 12))
    error_label.grid(row=row_index+1, columnspan=5)

    popup.grid_columnconfigure(1, weight=1)


def submit_group(table_frame, name, shares, threshold, popup, error_label):
    global groups
    if name == "" or shares == "" or threshold == "":
        error_label.configure(text="Please fill out all fields")
    elif any(group['name'] == name for group in groups):
        error_label.configure(text="Group already exists")
    else:
        try: 
            shares_int = int(shares)
            threshold_int = int(threshold)
            if int(threshold) > int(shares):
                error_label.configure(text="Threshold can't be higher than number of shares!")
            elif int(threshold) >= 16 or int(shares) >= 16:
                error_label.configure(text="Shares and Threshold can't be over 16!")
            else:
                    shares_int = int(shares)
                    threshold_int = int(threshold)

                    groups.append({"name": name, "shares": shares_int, "threshold": threshold_int})
                    popup.destroy()
                    generate_groups(table_frame)
        except ValueError:
            error_label.configure(text="Please enter valid numbers for shares and threshold.")

def validate_input(textbox, error_label):
    global seed

    with open('wordlist.json', 'r') as file:
        wordlist = json.load(file)
    
    input_words = textbox.get("1.0", "end-1c").strip().split(" ")
    
    if "\n" in textbox.get("1.0", "end-1c"):
        error_label.configure(text="Input must not contain new lines.")
        return
    if len(input_words) != 16:
        error_label.configure(text="Input must contain exactly 16 words.")
        return

    if not all(word in wordlist for word in input_words):
        error_label.configure(text="All words must be a correct polyseed words.")
        return

    error_label.configure(text="")
    seed = textbox.get("1.0", "end-1c")
    return True

def generate_shares(textbox, error_label, parent):
    global groups

    if validate_input(textbox, error_label):
        if len(groups) < 1:
            error_label.configure(text="You have to at least add one group")
        else:
            if len(groups) == 1:
                generate_shares_command(error_label, parent)
            else:
                group_threshold_popup(parent, error_label)

def seed_to_hex(seed, json_filepath):
    with open(json_filepath, 'r') as file:
        data = json.load(file)
    wordlist = data
    
    words = seed.split()
    
    indexes = [wordlist.index(word) for word in words]
    hex_string = ''.join(format(index, '03x') for index in indexes)
    
    return hex_string

def generate_shares_command(error_label, parent):
    global seed
    global groups
    global shares
    global group_threshold
    
    base_command = 'cd python-shamir-mnemonic && python3 -m shamir_mnemonic.cli create'

    hex_seed = seed_to_hex(seed, "wordlist.json")
    group_parts = []

    for group in groups:
        group_parts.append(f"--group {group['threshold']} {group['shares']}")
    
    command_string = f" custom --group-threshold {group_threshold} " + " ".join(group_parts)

    command_string =  base_command + command_string + f" --master-secret {hex_seed}"

    print(command_string)

    try:
        result = subprocess.run(command_string, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        groups_output = re.split(r'Group \d+ of \d+ - \d+ of \d+ shares required:\n', result.stdout.strip())
        group_info_output = re.findall(r'Group (\d+) of \d+ - (\d+) of (\d+) shares required:', result.stdout)
        group_data = []
        for info, group in zip(group_info_output, groups_output[1:]):
            group_name = groups[int(info[0])-1]['name']
            threshold = int(info[1])
            total_shares = int(info[2])
            shares = [share.strip() for share in group.strip().split('\n')]

            group_data.append({
                "name": group_name,
                "shares": shares,
                "total_shares": total_shares,
                "threshold": threshold
            })

        print(group_data)

        shares = group_data

        error_label.configure(text="Successfully generated shares", text_color="green")
        
        create_share_popup(parent)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")


def create_create_page(parent):
    create_frame = ctk.CTkFrame(parent, fg_color=parent.cget("fg_color"))
    create_frame.pack(fill="both", expand=True, padx=20, pady=20)

    seed_header = ctk.CTkLabel(master=create_frame, text="Seed", font=("Roboto", 20))
    seed_header.pack(anchor="nw", pady=(0, 10))

    seed_frame = ctk.CTkFrame(master=create_frame, fg_color=parent.cget("fg_color"))
    seed_frame.pack(fill='x', pady=(0, 10))

    textbox = ctk.CTkTextbox(master=seed_frame, width=500, height=100, corner_radius=15)
    textbox.pack(side="left", padx=(0, 10), anchor="w")

    error_label = ctk.CTkLabel(master=seed_frame, text="", text_color="red")
    error_label.pack(side="right", padx=(10, 50))

    group_header = ctk.CTkLabel(master=create_frame, text="Groups", font=("Roboto", 20))
    group_header.pack(anchor="nw")

    table_frame = ctk.CTkFrame(master=create_frame)
    table_frame.pack(fill="both", expand=True, pady=20)

    button_frame = ctk.CTkFrame(create_frame, fg_color=create_frame.cget("fg_color"))
    button_frame.pack()

    create_button = ctk.CTkButton(master=button_frame, text="Generate Shares", command=lambda: generate_shares(textbox, error_label, parent))
    create_button.pack(side="right", anchor="se", padx=50)

    add_button = ctk.CTkButton(master=button_frame, text="Add Group", command=lambda: add_group_popup(table_frame, create_frame))
    add_button.pack(side="right", anchor="se", padx=50)

    group_table(table_frame)

    generate_groups(table_frame)

    return create_frame

# Functions for group-threshold popup

def group_threshold_popup(parent, error_label):
    global group_threshold
    global groups

    popup = ctk.CTkToplevel(parent)
    popup.geometry("350x200")
    popup.minsize(350, 200)
    popup.title("Set group threshold")

    popup.focus_force()

    # Label above the buttons
    label = ctk.CTkLabel(popup, text=f"How many of your {len(groups)} groups\nshould be needed for recovery?", font=("Roboto", 20))
    label.pack(pady=(20, 20), padx=20)

    # Label to display the current threshold
    threshold_label = ctk.CTkLabel(popup, text=f"Current Threshold: {group_threshold}", font=("Roboto", 18))
    threshold_label.pack(pady=(0, 10))

    def set_group_threshold(value):
        global group_threshold
        group_threshold = int(float(value))
        threshold_label.configure(text=f"Current Threshold: {group_threshold}", font=("Roboto", 18))

    slider = ctk.CTkSlider(popup, from_=1, to=len(groups), command=set_group_threshold, number_of_steps=len(groups)-1)
    slider.set(group_threshold) 
    slider.pack(pady=(0, 5), padx=20, fill='x')

    # Frame for buttons
    button_frame = ctk.CTkFrame(popup)
    button_frame.pack(pady=(10, 0), padx=20, fill='x')

    # Cancel button to close the popup without saving
    cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=popup.destroy)
    cancel_button.pack(side='left', expand=True, fill='x', padx=(0, 5))

    # Done button to save changes and close the popup
    done_button = ctk.CTkButton(button_frame, text="Done", command=lambda: close_threshold_popup(popup, parent, error_label))
    done_button.pack(side='left', expand=True, fill='x', padx=(5, 0))
    
def close_threshold_popup(popup, parent, error_label):
    popup.destroy()
    generate_shares_command(error_label, parent)



# Functions for share saving popup

def save_shares_to_file():
    global shares
    # Save shares to a file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(f"{group_threshold} of the {len(shares)} groups have to be gathered for full recovery.\n\n")
            for group in shares:

                file.write(f"Group Name: {group['name']}\n")
                file.write(f"Total Shares: {group['total_shares']}\n")
                file.write(f"Threshold: {group['threshold']}\n")
                file.write("Shares:\n")
                for share in group['shares']:
                    file.write(f"    {share}\n")
                file.write("\n")
        messagebox.showinfo("Success", "Shares saved successfully!")

def create_share_popup(parent):
    popup = ctk.CTkToplevel(parent)
    popup.geometry("350x150")
    popup.minsize(350, 150)
    popup.title("Save shares")
    
    popup.grab_set()
    popup.focus_force()

    # Label above the buttons
    label = ctk.CTkLabel(popup, text="Choose an option")
    label.pack(pady=(20, 10), padx=20)

    # Frame for buttons
    button_frame = ctk.CTkFrame(popup)
    button_frame.pack(pady=(10, 0), padx=20, fill='x')

    # Buttons for actions
    display_button = ctk.CTkButton(button_frame, text="Display Shares",
                                   command=lambda: display_shares(popup, shares))
    display_button.pack(side='left', expand=True, fill='x', padx=(0, 5))

    save_button = ctk.CTkButton(button_frame, text="Save to File",
                                command=lambda: save_shares_to_file())
    save_button.pack(side='left', expand=True, fill='x', padx=5)

    close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
    close_button.pack(side='right', expand=True)