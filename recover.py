import json
try:
    import tkinter as tk
    import customtkinter as ctk
    
    # trezor shamir-mnemonic imports
    from shamir_mnemonic.recovery import RecoveryState
    from shamir_mnemonic.share import Share
    from shamir_mnemonic.utils import MnemonicError

except ImportError:
    print("Required dependencies are missing. Install them with:")
    print("pip install click customtkinter tkinter")
    sys.exit(1)

# Local project imports
import consts
from utils import *
from consts import recovery_state, stats_dict, BUTTON_FG, SEL_BUTTON_FG

# instruction field | textbox field : small button 
# groups shown like in display shares

def create_recover_page(parent):

    recover_frame = ctk.CTkFrame(parent)
    recover_frame.pack(fill="both", expand=True, padx=20, pady=20)

    scrollable_frame =  ctk.CTkScrollableFrame(recover_frame)
    scrollable_frame.pack(fill="both", expand=True)

    row_frame = ctk.CTkFrame(scrollable_frame, fg_color=scrollable_frame.cget("fg_color"))
    row_frame.pack(fill="x", padx=10, pady=10)

    info_frame = ctk.CTkFrame(row_frame, width=180, height=100)
    info_frame.pack(side="left", padx=(0, 10))

    label = ctk.CTkLabel(info_frame, text="Enter a share:", anchor="nw", width=180, height=100, wraplength=180)
    label.pack(side="left", padx=(5, 10), pady=(5,5))

    entry_frame = ctk.CTkFrame(row_frame, fg_color=scrollable_frame.cget("fg_color"))
    entry_frame.pack(side="right", expand=True)

    textbox = ctk.CTkTextbox(master=row_frame, width=600, height=100, corner_radius=15)
    textbox.pack(side="left", fill="both", expand=True)

    progress_text = "Enter your first share so you can start the recovery"

    progress_frame = ctk.CTkFrame(scrollable_frame)
    progress_label = ctk.CTkLabel(progress_frame, text=progress_text, font=("Roboto", 18, "bold"),)

    button = mainButton(entry_frame, "Submit", width=30, command=lambda: do_recovery1(textbox.get(1.0, "end-1c"), progress_label, label, textbox, scrollable_frame, show_seed_button))
    button.pack(side="right", padx=(5, 0), pady=(70, 0))

    progress_frame.pack(fill="both", expand=True, padx=10, pady=(10,0))
    progress_label.pack()

    show_seed_button = mainButton(scrollable_frame, width=50, text="Show seed", command=lambda: show_seed(parent=parent))
    show_seed_button.pack()
    show_seed_button.configure(state="disabled")

    return recover_frame

def do_recovery1(mnemonic, progress_label, label, textbox, parent, show_seed_button):
    global recovery_state
    global stats_dict

    if recovery_state == None:
        recovery_state = RecoveryState()

    # print("mnemonic: " + mnemonic)

    try:
        share = Share.from_mnemonic(str(mnemonic))

        if not recovery_state.matches(share):
            label.configure(text="This mnemonic is not part of the current set. Please try again.", text_color="red")
            return
        if share in recovery_state:
            label.configure(text="Share already entered.", text_color="red")
            return

        recovery_state.add_share(share)
    
    except MnemonicError as e:
        label.configure(text=f"{e}", text_color="red")
        return
        
    except ValueError as e:
        label.configure(text=f"{e}", text_color="red")
        return

    textbox.delete("1.0", "end")
    label.configure(text="Enter a share:")

    stats_dict["groups_completed"] = recovery_state.groups_complete()
    stats_dict["group_threshold"] = recovery_state.parameters.group_threshold
    stats_dict["group_count"] = recovery_state.parameters.group_count

    def update_or_add_group(group_name, group_size, group_threshold, mnemonic=None):
        global stats_dict

        print(f"Name: {group_name}\nSize: {group_size}\nThreshold: {group_threshold}\nMnemonic: {mnemonic}")
        
        is_new_group = not any(group['group_name'] == group_name for group in stats_dict['groups'])

        if mnemonic and is_new_group:
            new_group = {
                "group_name": group_name,
                "group_size": group_size,
                "group_threshold": group_threshold,
                "shares": [str(mnemonic)]
            }
            stats_dict["groups"].append(new_group)
        
        if mnemonic and not is_new_group:
            for group in stats_dict["groups"]:
                if group["group_name"] == group_name:
                    group["group_size"] = group_size
                    group["group_threshold"] = group_threshold
                    group["shares"].append(str(mnemonic))

        if not mnemonic and is_new_group:
            new_group = {
                "group_name": group_name,
                "group_size": group_size,
                "group_threshold": group_threshold,
                "shares": []
            }
            stats_dict["groups"].append(new_group)


    for i in range(stats_dict["group_count"]):
        group_size, group_threshold = recovery_state.group_status(i)
        group_name = recovery_state.group_prefix(i)

        if i != share.group_index:
            update_or_add_group(group_name, group_size, group_threshold)
        else:
            update_or_add_group(group_name, group_size, group_threshold, mnemonic)

        print("-----------------------------------------------------------------------------")
        print(stats_dict)


    #print(stats_dict)
    update_progress(progress_label, label, parent, show_seed_button)
    display_shares(parent)
    

def update_progress(progress_label, label, parent, show_seed_button):
    global stats_dict

    groups_text = ""

    FINISHED = "\u2713"
    EMPTY = "\u2717"
    INPROGRESS = "\u25cf"

    for i in range(stats_dict["group_count"]):

        group_size = stats_dict["groups"][i]["group_size"]
        group_name = stats_dict["groups"][i]["group_name"]
        group_threshold = stats_dict["groups"][i]["group_threshold"]

        prefix = FINISHED if group_size >= group_threshold else INPROGRESS

        if group_threshold > 0:
            groups_text = groups_text + f"\n {prefix} {str(group_size)} of {str(group_threshold)} shares from group {str(group_name)}"
        else:
            groups_text = groups_text + f"\n {EMPTY} 0 shares from group {str(group_name)}"

    text = f"""
You completed {stats_dict["groups_completed"]}/{stats_dict["group_threshold"]} groups{groups_text}
"""
    if stats_dict["groups_completed"] >= stats_dict["group_threshold"]:
        text = f"""
You completed the recovery!{groups_text}
"""    
        display_seed(parent)
        show_seed_button.configure(state="normal")

        

    progress_label.configure(text=text, font=("Roboto", 18, "bold"), justify="left")

def display_shares(parent):
    global stats_dict

    if hasattr(parent, 'shares_container'):

        for widget in parent.shares_container.winfo_children():
            widget.destroy()
    else:

        parent.shares_container = ctk.CTkFrame(parent)
        parent.shares_container.pack(fill='both', expand=True, padx=10, pady=10)

    bg_color = parent.cget("fg_color")

    for group in stats_dict["groups"]:
        # print(group)
        
        group_label = ctk.CTkLabel(parent.shares_container, text_color=SEL_BUTTON_FG, text=f"{group['group_name']} - Shares: {group['group_size']} of {group['group_threshold']} needed", font=("Roboto", 18, "bold"))
        if group["group_threshold"] < 1:
            group_label = ctk.CTkLabel(parent.shares_container,  text_color=SEL_BUTTON_FG, text=f"{group['group_name']} - No shares yet", font=("Roboto", 18, "bold"))

        group_label.pack(pady=(10, 5), padx=10, fill='x', anchor='center')

        if group["group_threshold"] > 0:
            for i in range(0, len(group["shares"]), 4):
                row_frame = ctk.CTkFrame(parent.shares_container, fg_color=bg_color)
                row_frame.pack(pady=10, padx=10, fill='x')
                for share in group['shares'][i:i+4]:
                    share_textbox = ctk.CTkTextbox(row_frame, height=200, state='normal', width=190)
                    share_textbox.insert("1.0", share)
                    share_textbox.pack(side="left", padx=5, expand=True)
                    share_textbox.configure(state="disabled")


def display_seed(parent):

    popup = ctk.CTkToplevel(parent)
    center_popup(popup, parent, 250, 150)
    popup.minsize(250, 150)
    popup.title("Recovered seed")

    popup.focus_force()

    label = ctk.CTkLabel(popup, text="Recovery done!\nShow seed?", font=("Roboto", 18, "bold"))
    label.pack(pady=(10))

    button_frame = ctk.CTkFrame(popup)
    button_frame.pack(pady=(0, 0), padx=20, fill='x')

    cancel_button = ctk.CTkButton(button_frame, text="No", fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG,
        cursor="hand2", width=(50),
        text_color="white", command=popup.destroy)
    cancel_button.pack(side='left', fill='both', expand=True, padx=5)

    done_button = ctk.CTkButton(button_frame, text="Yes", fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG,
        cursor="hand2", width=(50),
        text_color="white", command=lambda: show_seed(parent, popup))
    done_button.pack(side='right',  fill='both', expand=True, padx=5)

def show_seed(parent, popup=None):
    global recovery_state

    if popup != None:
        popup.destroy()

    popup = ctk.CTkToplevel(parent)
    center_popup(popup, parent, 250, 150)
    popup.minsize(250, 150)
    popup.title("Recovered seed")

    popup.focus_force()

    textbox = ctk.CTkTextbox(master=popup, width=250, height=100, corner_radius=15, text_color=SEL_BUTTON_FG, fg_color=popup.cget("fg_color"))
    textbox.pack(fill="both", expand=True, padx=5, pady=(5, 0))

    ok_button = ctk.CTkButton(popup, text="Done", fg_color=BUTTON_FG, hover_color=SEL_BUTTON_FG,
                              cursor="hand2", anchor="center",
                              text_color="white", width=100, height=30, command=popup.destroy)
    ok_button.pack(pady=(10, 10))


    try:
        master_secret = recovery_state.recover(b"").hex()
    except MnemonicError as e:
        print(str(e))
    finally:
        with open(consts.WORDLIST_PATH, 'r') as file:
            polyseed_wordlist = json.load(file)
        # print(master_secret)
        
        seed = hex_to_seed(master_secret, polyseed_wordlist)
        # print(seed)

        textbox.insert(ctk.END, seed)
        textbox.configure(state="disabled")

        


