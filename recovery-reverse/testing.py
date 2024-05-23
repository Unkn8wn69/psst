import sys
import click
from click import style
sys.path.append('../python-shamir-mnemonic')
from shamir_mnemonic.recovery import RecoveryState
from shamir_mnemonic.share import Share

FINISHED = style("\u2713", fg="green", bold=True)
EMPTY = style("\u2717", fg="red", bold=True)
INPROGRESS = style("\u25cf", fg="yellow", bold=True)

def own_recovery():
    recovery_state = RecoveryState()

    mnemonic_str = "home indicate acrobat eclipse acne pecan corner oasis practice emerald join literary lamp fiscal breathe desire phantom source pulse main level verdict lair market harvest marathon warn"
    share = Share.from_mnemonic(mnemonic_str)

    if not recovery_state.matches(share):
        print("This mnemonic is not part of the current set. Please try again.")
        exit(0)
    if share in recovery_state:
        print("Share already entered.")
        exit(0)
    
    recovery_state.add_share(share)

    def print_group_status(idx: int) -> None:
        group_size, group_threshold = recovery_state.group_status(idx)
        group_prefix = style(recovery_state.group_prefix(idx), bold=True)
        bi = style(str(group_size), bold=True)
        if not group_size:
            click.echo(f"{EMPTY} {bi} shares from group {group_prefix}")
        else:
            prefix = FINISHED if group_size >= group_threshold else INPROGRESS
            bt = style(str(group_threshold), bold=True)
            click.echo(f"{prefix} {bi} of {bt} shares needed from group {group_prefix}")

    def print_status() -> None:

        groups_completed = recovery_state.groups_complete()
        group_threshold = recovery_state.parameters.group_threshold
        group_count = recovery_state.parameters.group_count

        print("groups_complete: " + str(groups_completed))
        print("group_threshold: " + str(group_threshold))
        print("group_count: " + str(group_count))

        # group_size is how many already from this group you got
        # group threshold how many shares needed to recover this group
        group_size, group_threshold = recovery_state.group_status(0) # group size and threshold of given id of group starting at 0
        group_name = recovery_state.group_prefix(0) # group name of given id

        print(f"Group '{group_name}'" + " group_size = " + str(group_size) + " group_threshold = " + str(group_threshold))

 

    print_status()
    


def recover(passphrase_prompt: bool) -> None:
    recovery_state = RecoveryState()

    def print_group_status(idx: int) -> None:
        group_size, group_threshold = recovery_state.group_status(idx)
        group_prefix = style(recovery_state.group_prefix(idx), bold=True)
        bi = style(str(group_size), bold=True)
        if not group_size:
            click.echo(f"{EMPTY} {bi} shares from group {group_prefix}")
        else:
            prefix = FINISHED if group_size >= group_threshold else INPROGRESS
            bt = style(str(group_threshold), bold=True)
            click.echo(f"{prefix} {bi} of {bt} shares needed from group {group_prefix}")

    def print_status() -> None:
        bn = style(str(recovery_state.groups_complete()), bold=True)
        assert recovery_state.parameters is not None
        bt = style(str(recovery_state.parameters.group_threshold), bold=True)
        click.echo()
        if recovery_state.parameters.group_count > 1:
            click.echo(f"Completed {bn} of {bt} groups needed:")
        for i in range(recovery_state.parameters.group_count):
            print_group_status(i)

    while not recovery_state.is_complete():
        try:
            mnemonic_str = click.prompt("Enter a recovery share")
            share = Share.from_mnemonic(mnemonic_str)
            if not recovery_state.matches(share):
                print("This mnemonic is not part of the current set. Please try again.")
                continue
            if share in recovery_state:
                print("Share already entered.")
                continue

            recovery_state.add_share(share)
            print_status()

        except click.Abort:
            return
        except Exception as e:
            print(str(e))

    passphrase_bytes = b""
    if passphrase_prompt:
        while True:
            passphrase = click.prompt(
                "Enter passphrase", hide_input=True, confirmation_prompt=True
            )
            try:
                passphrase_bytes = passphrase.encode("ascii")
                break
            except UnicodeDecodeprint:
                click.echo("Passphrase must be ASCII. Please try again.")

    try:
        master_secret = recovery_state.recover(passphrase_bytes)
    except MnemonicError as e:
        print(str(e))
        click.echo("Recovery failed")
        sys.exit(1)
    click.secho("SUCCESS!", fg="green", bold=True)
    click.echo(f"Your master secret is: {master_secret.hex()}")

# recover(False)
own_recovery()