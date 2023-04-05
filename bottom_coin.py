import sys
import os
import json
import math
from solid2 import *
import coin_lib


class BottomCoin:
    def __init__(
        self,
        seed_phrase,
        serial_number,
        denomination_amount="1,000,000",
        denomination_unit="Satoshis",
    ):
        self.seed_phrase = seed_phrase
        self.serial_number = serial_number
        self.denomination_amount = denomination_amount
        self.denomination_unit = denomination_unit
        self.wallet = self.initialize_wallet()
        self.coin = self.create_coin()

    def initialize_wallet(self):
        if self.seed_phrase == "generate":
            return coin_lib.BitcoinWallet()
        else:
            return coin_lib.BitcoinWallet(seed_phrase=self.seed_phrase.lower())

    def create_coin(self):
        coin = coin_lib.common_coin(bottom=True)
        coin = self.add_denomination_text(coin)
        coin = self.add_serial_number_text(coin)
        coin = self.add_bitcoin_sign(coin)
        coin = self.add_seed_phrase_spiral(coin)
        return coin

    def add_denomination_text(self, coin):
        coin += (
            text(
                self.denomination_amount,
                size=10,
                halign="center",
                valign="center",
                font="Liberation Sans:style=Bold Italic",
            )
            .linear_extrude(coin_lib.coin_thickness - 3)
            .translate([0, 8, 3])
        )
        coin += (
            text(
                self.denomination_unit,
                size=10,
                halign="center",
                valign="center",
                font="Liberation Sans:style=Bold Italic",
            )
            .linear_extrude(coin_lib.coin_thickness - 3)
            .translate([0, -8, 3])
        )
        return coin

    def add_serial_number_text(self, coin):
        coin += (
            text(
                f"sn{self.serial_number}",
                size=5,
                halign="center",
                valign="center",
                font="Liberation Mono:style=Bold",
            )
            .linear_extrude(0.6)
            .translate([0, -22, 3])
        )
        return coin

    def add_bitcoin_sign(self, coin):
        coin -= (
            import_(file="BitcoinSign.svg")
            .linear_extrude(height=1)
            .scale([0.20, 0.20, 1])
            .translate([-7, -9.75, 0])  # XXX center the image; hard coded
            .mirror([1, 0, 0])
            .rotate([180, 180, 0])
        )
        return coin

    def add_seed_phrase_spiral(self, coin):
        seed_phrase = self.wallet.seed_phrase.upper()

        for letter in coin_lib.ArchimedeanSpiralString(
            string=seed_phrase,
            letter_size=5,
            dot_dist=4.5,
            init_degrees=360 * 2.5,
            spiral_separation=360 / 8,
        ).generate_letters():
            coin -= letter.linear_extrude(height=1).mirror([1, 0.0])
        return coin


def main(seed_phrase, serial_number, denomination_amount, denomination_unit):
    bottom_coin = BottomCoin(
        seed_phrase,
        serial_number,
        denomination_amount=denomination_amount,
        denomination_unit=denomination_unit,
    )

    output_path = "bottom_coins"
    os.makedirs(output_path, exist_ok=True)

    json_path = "coin_data"
    os.makedirs(json_path, exist_ok=True)
    json_file_path = os.path.join(json_path, f"bottom_coin_sn{serial_number}.json")

    if os.path.exists(json_file_path):
        print(f"Error: json file already exists for serial number {serial_number}")
        sys.exit(1)

    os.system(f"cp BitcoinSign.svg {output_path}")
    bottom_coin.coin.save_as_scad(
        os.path.join(output_path, f"bottom_coin_sn{serial_number}.scad")
    )

    json_data = {
        "serial_number": serial_number,
        "public_address": bottom_coin.wallet.address,
        "denomination_amount": denomination_amount,
        "denomination_unit": denomination_unit,
    }

    with open(json_file_path, "w") as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bottom_coin.py <seed phrase> <serial number>")
        sys.exit(1)

    seed_phrase_arg = sys.argv[1]
    serial_number_arg = sys.argv[2]
    main(seed_phrase_arg, serial_number_arg, "1,000,000", "Satoshis")
