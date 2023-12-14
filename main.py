import os
import time
import subprocess
import json
import re
import random

final_hex = ""
groups = []
group_threshold = 0
polyseed_wordlist = []

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def word_to_index(word, wordlist):
    try:
        return wordlist.index(word)
    except ValueError:
        raise ValueError(f"Word '{word}' not found in the wordlist.")

def index_to_word(index, wordlist):
    return wordlist[index]

def seed_to_hex(seed, wordlist):
    words = seed.split()
    indexes = [wordlist.index(word) for word in words]
    hex_string = ''.join(format(index, '03x') for index in indexes)
    return hex_string

def hex_to_seed(hex_string, wordlist):
    n = 3
    chunks = [hex_string[i:i+n] for i in range(0, len(hex_string), n)]
    seed = ' '.join(wordlist[int(chunk, 16)] for chunk in chunks)
    return seed

def is_valid_seed(seed):
    words = seed.split()
    return all(word in polyseed_wordlist for word in words)

def seed_input():
    global final_hex
    choice = input("Please enter your seed:\n")
    if is_valid_seed(choice):
        final_hex = seed_to_hex(choice, polyseed_wordlist)
        print(final_hex)
        create_groups()
    else:
        print("This seed is not valid")
        seed_input()

def is_valid_string(input_string):
    global final_hex
    try:
        hex_representation = input_string.encode().hex()

        if len(hex_representation) >= 4:
            final_hex = hex_representation
            #print(final_hex)
            return True
        else:
            return False
    except UnicodeEncodeError:
        return False

def string_input():
    choice = input("Please enter your string:\n")
    if is_valid_string(choice):
        print("valid")
    else:
        clear_screen()
        print("Your string isn't valid or too short")
        string_input()

def type_of_input():
    clear_screen()
    print("Choose type of input:")
    print("1: Monero/BIP39 seed")
    print("2: Arbitrary string")
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        clear_screen()
        seed_input()
    else:
        clear_screen()
        string_input()

def validate_shares_and_threshold(num_shares, threshold):
    if num_shares > 16:
        print("The number of shares cannot exceed 16.")
        return False
    if threshold < 1 or threshold > num_shares:
        print("Threshold must be at least 1 and not more than the number of shares.")
        return False
    return True

def display_groups(groups):
    if not groups:
        print("No groups created yet.")
        return

    # Table headers
    print(f"{'Group No.':<10} {'Name':<15} {'Shares':<10} {'Threshold':<10}")
    print('-' * 45)

    # Table rows
    for i, group in enumerate(groups, start=1):
        print(f"{str(i):<10} {group['name']:<15} {group['num_shares']:<10} {group['threshold']:<10}")

    print()

def edit_group(groups):
    display_groups(groups)
    group_number = int(input("Enter the group number to edit: ")) - 1
    if 0 <= group_number < len(groups):
        group = groups[group_number]
        group_name = group['name']
        name_prompt = "Enter the new name: " if group_name != "default" else "Enter the name: "
        group['name'] = input(name_prompt)

        while True:
            shares_prompt = "Enter the new number of shares: "
            threshold_prompt = "Enter the new threshold: "
            num_shares = int(input(shares_prompt))
            threshold = int(input(threshold_prompt))

            if validate_shares_and_threshold(num_shares, threshold):
                group['num_shares'] = num_shares
                group['threshold'] = threshold
                break
    else:
        print("Invalid group number.")

def delete_group(groups):
    display_groups(groups)
    group_number = int(input("Enter the group number to delete: ")) - 1
    if 0 <= group_number < len(groups):
        del groups[group_number]
    else:
        print("Invalid group number.")

def create_groups():
    global groups
    global group_threshold
    clear_screen()
    groups = []
    use_multiple_groups = input("Do you want to use multiple groups? (yes/no): ").strip().lower()

    if use_multiple_groups == 'yes' and group_threshold == 0:
        while True:
            group_threshold = int(input("How many groups should be needed to complete?\n"))
            if 1 <= group_threshold <= 16:
                break
            print("Group threshold must be between 1 and 16.")

    while True:
        group_name = "default" if not groups and use_multiple_groups != 'yes' else input("Enter the group name: ")
        while True:
            shares_prompt = "Enter the number of shares: "
            threshold_prompt = "Enter the threshold: "
            num_shares = int(input(shares_prompt))
            threshold = int(input(threshold_prompt))

            if validate_shares_and_threshold(num_shares, threshold):
                groups.append({
                    'name': group_name,
                    'num_shares': num_shares,
                    'threshold': threshold
                })
                break

        clear_screen()
        display_groups(groups)

        if use_multiple_groups == 'yes':
            another_group = input("Do you want to add another group? (yes/no): ").strip().lower()
            if another_group != 'yes':
                break

        if use_multiple_groups == 'no':
            break

    manage_groups()

def manage_groups():
    global groups
    while True:
        action = input("Do you want to edit/delete any group, or are you done? (edit/delete/done): ").strip().lower()
        if action == 'edit':
            edit_group(groups)
            clear_screen()
            display_groups(groups)
        elif action == 'delete':
            delete_group(groups)
            clear_screen()
            display_groups(groups)
        elif action == 'done':
            output_type()
            break
        

def output_type():
    clear_screen()
    share_data = run_shamir_mnemonic_command()
    while True:
        print("Choose a output type:")
        print("1: Output secrets as mnemonic phrases")
        print("2: Output secrets in hexedecimal")
        print("3: Output secrets in both mnemonic phrases and hexedecimal")
        choice = input("==> ")
        if choice == "1":
            print_groups_with_color(share_data)
        elif choice == "2":
            print_groups_with_color_hex(share_data)
        elif choice == "3":
            print_groups_with_color_and_hex(share_data)
        else:
            clear_screen()
            print("Please choose a valid option.")

def run_shamir_mnemonic_command():
    global final_hex
    global groups
    global group_threshold
    
    base_command = 'cd python-shamir-mnemonic && python3 -m shamir_mnemonic.cli create'

    if len(groups) > 1 or groups[0]['name'] != 'default':
        command = f"{base_command} custom --group-threshold {group_threshold} --master-secret {final_hex}"
        for group in groups:
            command += f" --group {group['threshold']} {group['num_shares']}"
    else:
        single_group = groups[0]
        command = f"{base_command} {single_group['threshold']}of{single_group['num_shares']} --master-secret {final_hex}"

    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # print("Command Output:\n", result.stdout)

        print("-" * 50)
        groups_output = re.split(r'Group \d+ of \d+ - \d+ of \d+ shares required:\n', result.stdout.strip())
        group_info_output = re.findall(r'Group (\d+) of \d+ - (\d+) of (\d+) shares required:', result.stdout)
        group_data = []
        for info, group in zip(group_info_output, groups_output[1:]):  # Skip the first element as it's empty
            #print(groups)
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

        return group_data

    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")

RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"
colors = [YELLOW, BLUE, MAGENTA, CYAN]

def print_groups_with_color(groups):
    for group in groups:
        color = random.choice(colors)
        print("\033[32m" + f"{group['name']} {RESET} - \033[1m {group['threshold']} of {group['total_shares']} {RESET} shares required:" + RESET)
        for i, share in enumerate(group['shares']):
            print(color + share + "\n" + RESET)

def print_groups_with_color_hex(groups):
    for group in groups:
        color = random.choice(colors)
        print("\033[32m" + f"{group['name']} {RESET} - \033[1m {group['threshold']} of {group['total_shares']} {RESET} shares required:" + RESET)
        for i, share in enumerate(group['shares']):
            print(color + share.encode().hex() + "\n" + RESET)
            
def print_groups_with_color_and_hex(groups):
    for group in groups:
        color = random.choice(colors)
        print("\033[32m" + f"{group['name']} {RESET} - \033[1m {group['threshold']} of {group['total_shares']} {RESET} shares required:" + RESET)
        for i, share in enumerate(group['shares']):
            print(color + share + "\n" + share.encode().hex() + "\n" + RESET)

def main():
    print("Monero Seed Converter")
    print("Choose an operation:")
    print("1: Create a set of shared secrets from a seed or string")
    print("2: Recover seed or string from set of shared secrets")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        type_of_input()
    elif choice == '2':
        recover()
    else:
        print("Invalid choice. Please enter 1 or 2.")

def recover():
    while True:
        print("Recovery options")
        print("Choose an operation:")
        print("1: Recover the secret hexstring from mnemonics")
        print("2: Recover the seed from the secret hexstring")
        print("3: Recover the secret hexstring from hexstrings")
        print("4: Exit")
        choice = input("==> ")

        if choice == '1':
            subprocess.run('cd python-shamir-mnemonic && python3 -m shamir_mnemonic.cli recover', shell=True)
        elif choice == '2':
            hex_string = input("Enter the hexadecimal string: ")
            print("Recovered seed phrase:")
            print(hex_to_seed(hex_string, polyseed_wordlist))
        elif choice == '3':
            print("Not implemented yet")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter 1,2,3 or 4.")

if __name__ == "__main__":
    with open('wordlist.json', 'r') as file:
        polyseed_wordlist = json.load(file)
    main()