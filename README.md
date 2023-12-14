# Polyseed Secret Sharing Tool 🤫

This is a python cli tool that can be used to backup a monero polyseed using shared secrets by using [Shamir's Secret Sharing Scheme](https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing). It uses Trezors python-shamir-mnemonic to generate mnemonic phrases. To also lower the amount of words per mnemonic phrase it only saves the seed's indexes in the [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md) wordlist and by that lowering the amount of words to ~24 per share.

## Motivation

In the realm of cryptocurrency, security is paramount, and it's often a personal responsibility. Traditional methods of storing seed phrases, even in multiple secure locations, have a critical vulnerability: if one location is breached, the entire wallet is at risk.

I've recently explored the effectiveness of SSSS, particularly for enhancing the security of seedphrases. SSSS is a cryptographic method that allows a secret, such as a seedphrase, to be divided into multiple shares. The brilliance of this approach lies in its flexibility: the original secret can only be reconstructed when a predefined number of these shares are combined. This threshold mechanism ensures that the loss or compromise of a single share doesn’t expose the entire secret, significantly reducing the risk of a single point of failure.

The application of SSSS to seedphrases marks a significant improvement in how we secure our digital assets. It allows for a distributed and resilient form of protection. Additionally, users can employ advanced security measures like steganography to conceal these shares.

## Disclaimer

Important: This tool should only be used in a secure, air-gapped environment, like [TAILS](https://tails.net)

This project is in experimental stage, and contributions from those with cryptography and coding expertise are welcome.

## Features & Roadmap

* [X] Convert monero polyseed seed to small hexstring
* [X] Generate a set of secret shares (multiple groups, master threshold etc.)
* [ ] Ability to generate secret shares from arbitrary data.
* [ ] Codebase enhancements for simplicity and clarity.
* [ ] Direct integration with Trezor's shamir-mnemonic for streamlined processes.

## Prerequisites

- Python 3.9+
- click python module (preinstalled on Tails)
- Trezors [python-shamir-mnemonic](https://github.com/trezor/python-shamir-mnemonic)

## Installation

1. Install click module

   `pip install click`

   For externally managed environment on Arch:

   ```
   sudo pacman -S python-click
   ```
2. Install python-shamir-mnemonic

   `git clone https://github.com/trezor/python-shamir-mnemonic`
3. Start the tool

   `python main.py`

## Credits

- Trezor [python-shamir-mnemonic](https://github.com/trezor/python-shamir-mnemonic)
- [iancoleman](https://github.com/iancoleman/slip39) for inspiration from his https://iancoleman.io/slip39/

## Donations

If you find this project useful, please consider donating to the following Monero address: (Or for other cryptos [here](https://trocador.app/anonpay/?ticker_to=xmr&network_to=Mainnet&address=89ZYSD9nyFxZS1zrZaB9Z4giuv776AeKTMXVRWPMkZDtau7wF2DCgqc1tH9zAVszPTP9XTSnhLT4rYUhW6oP8okeS56Jbdc&donation=True&simple_mode=True&name=Unkn8wn69))

89ZYSD9nyFxZS1zrZaB9Z4giuv776AeKTMXVRWPMkZDtau7wF2DCgqc1tH9zAVszPTP9XTSnhLT4rYUhW6oP8okeS56Jbdc

## License

This project is released under the terms of the GPL 3.0 license. For more information, see the [LICENSE](LICENSE) file included in the repository.
