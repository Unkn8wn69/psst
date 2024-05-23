try:
    import tkinter as tk
    import customtkinter as ctk

except ImportError:
    print("Required dependencies are missing. Install them with:")
    print("pip install click customtkinter tkinter")
    sys.exit(1)

# trezor shamir-mnemonic imports
import sys
sys.path.append('./python-shamir-mnemonic')
from shamir_mnemonic.recovery import RecoveryState
from shamir_mnemonic.share import Share
from shamir_mnemonic.utils import MnemonicError

# Local project imports
from consts import *
from widgets import *
from consts import recovery_state

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
    progress_label = ctk.CTkLabel(progress_frame, text=progress_text)

    button = mainButton(entry_frame, "Submit", width=30, command=lambda: do_recovery1(textbox.get(1.0, "end-1c"), progress_label, label, textbox))
    button.pack(side="right", padx=(5, 0), pady=(70, 0))

    progress_frame.pack(fill="both", expand=True, padx=10, pady=10)
    progress_label.pack()

    # display_shares(parent)

    return recover_frame

def do_recovery1(mnemonic, progress_label, label, textbox):
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
            label.configure(text="Share already entered.")
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

    def update_or_add_group(group_name, group_size, group_threshold, mnemonic):
        global stats_dict

        for group in stats_dict["groups"]:
            if group["group_name"] == group_name:
                group["group_size"] = group_size
                group["group_threshold"] = group_threshold
                group["shares"].append(str(mnemonic))
                return

        stats_dict["groups"].append({
            "group_name": group_name,
            "group_size": group_size,
            "group_threshold": group_threshold,
            "shares": [str(mnemonic)]
        })

    for i in range(stats_dict["group_count"]):
        group_size, group_threshold = recovery_state.group_status(i)
        group_name = recovery_state.group_prefix(i)

        
        update_or_add_group(group_name, group_size, group_threshold, mnemonic)


    print(stats_dict)
    update_progress(progress_label, label)
    

def update_progress(progress_label, label):
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

    progress_label.configure(text=text)

def display_shares(parent):
    shares = [{'name': 'Friends', 'shares': ['scandal veteran acrobat eclipse acne playoff briefing pancake salary syndrome alarm ocean flash manager home total kitchen browser unwrap ajar view item decent bulge together scramble duckling', 'scandal veteran acrobat emerald academic material result playoff glad blimp playoff ounce ceramic knife dictate mixture cluster speak laden crazy lift ceiling peasant branch robin bracelet ceramic', 'scandal veteran acrobat envelope acid august plan leaves marvel drove huge swing steady desert penalty counter emission equation listen avoid recover distance cover check agency regret alto', 'scandal veteran acrobat exact acquire cover artwork main custody vocal satisfy step problem safari wolf fridge carbon license both cause slush genius render center froth have briefing', 'scandal veteran acrobat eyebrow acquire distance plot disease arcade raisin dilemma teacher science pharmacy saver drove ancestor average extend ocean symbolic mansion tadpole moisture isolate industry metric'], 'total_shares': 5, 'threshold': 3}, {'name': 'Family', 'shares': ['scandal veteran beard eclipse acquire alarm raisin exclude adorn mouse guard furl lungs goat mountain lunar watch adapt prospect deal ivory recover type segment blind hazard surprise', 'scandal veteran beard emerald acquire plastic watch become hush moment legend density carpet chemical jerky skunk raspy photo gravity artist timely admit mortgage charity total adorn device', 'scandal veteran beard envelope acid dramatic dish hush aquatic percent resident frozen sniff mountain main building mule multiple exceed frequent total downtown sweater edge dragon critical hairy', 'scandal veteran beard exact acid modify injury crush language petition frost demand enemy spider grin failure step decrease necklace genuine judicial lecture pecan pickup sharp election leaves', 'scandal veteran beard eyebrow acne deadline impact guard ocean depict friar peanut military freshman upgrade mixture rumor fragment grin prize mansion kitchen sweater welfare soul liberty unfold', 'scandal veteran beard fiber acne leaf earth dragon traveler deny repeat smith album camera busy strike medical wine quarter mobile blessing script pecan buyer center true alto', 'scandal veteran beard flip academic blind yoga force mountain adequate leaves peaceful shame pleasure unknown aviation profile similar obtain salt biology yield type kind withdraw salon fortune'], 'total_shares': 7, 'threshold': 3}]
    group_threshold = 1

    bg_color = parent.cget("fg_color")

    scrollable_frame = ctk.CTkScrollableFrame(parent)
    scrollable_frame.pack(side="left", fill="both", expand=True)

    title_label = ctk.CTkLabel(scrollable_frame, text=f"These are your shares to restore your seed. At least {group_threshold} groups are required to restore the seed.", font=("Roboto", 15, "bold"), text_color=SEL_BUTTON_FG)
    title_label.pack(pady=(10, 5), padx=10, fill='x', anchor='center')

    for group in shares:
        group_label = ctk.CTkLabel(scrollable_frame, text=f"{group['name']} - Total Shares: {group['total_shares']}, Needed: {group['threshold']}", font=("Roboto", 16, "bold"))
        group_label.pack(pady=(10, 5), padx=10, fill='x', anchor='center')

        for i in range(0, len(group['shares']), 5):
            row_frame = ctk.CTkFrame(scrollable_frame, fg_color=bg_color)
            row_frame.pack(pady=10, padx=10, fill='x')
            for share in group['shares'][i:i+5]:
                share_textbox = ctk.CTkTextbox(row_frame, height=200, state='normal', width=190)
                share_textbox.insert("1.0", share)
                share_textbox.pack(side="left", padx=5, expand=True)
                share_textbox.configure(state="disabled")

    # Frame for buttons
    button_frame = ctk.CTkFrame(scrollable_frame)
    button_frame.pack(pady=(10, 0), padx=20, fill='x')

    save_button = mainButton(button_frame, text="Save to File",
                                command=lambda: save_shares_to_file())
    save_button.pack(side='right', pady=(10,10), padx=10)

    close_button = mainButton(button_frame, text="Close", command=lambda: popup.destroy)
    close_button.pack(side="right", pady=(10,10), padx=10)