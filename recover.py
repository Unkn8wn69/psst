import tkinter as tk
import customtkinter as ctk
from consts import *
from widgets import *

def create_recover_page(parent):

    recover_frame = ctk.CTkFrame(parent, fg_color=parent.cget("fg_color"))
    recover_frame.pack(fill="both", expand=True, padx=20, pady=20)

    display_shares(parent)

    return recover_frame

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