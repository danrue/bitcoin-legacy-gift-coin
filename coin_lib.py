import solid2
import math
import secrets
from bitcoinlib.keys import HDKey
from bitcoinlib.mnemonic import Mnemonic


class BaseCoin:
    def __init__(
        self,
        coin_diameter=76.2,
        coin_thickness=5.0,
        screw_hole_diameter=2.5,
        nut_width=4.0,
        fn=512,
    ):
        self.coin_diameter = coin_diameter
        self.coin_thickness = coin_thickness
        self.screw_hole_diameter = screw_hole_diameter
        self.nut_width = nut_width
        self.fn = fn

    def hole_locations(self):
        radius = (self.coin_diameter / 2) - 5
        angles = [45, 135, 225, 315]

        return [
            [
                radius * math.cos(math.radians(angle)),
                radius * math.sin(math.radians(angle)),
                0,
            ]
            for angle in angles
        ]

    def common_coin(self, bottom=False):
        # basic coin shape
        coin = solid2.cylinder(d=self.coin_diameter, h=self.coin_thickness, _fn=self.fn)

        # cut out the center
        # 2mm deep, 2.5mm rim (5mm/2)
        coin -= solid2.cylinder(h=2, d=self.coin_diameter - 5, _fn=self.fn).up(3)

        if bottom:
            # If bottom, create nut holder
            # The nut holder consists of a circular support area and a
            # hexagon shaped hole for the nut.
            for location in self.hole_locations():
                coin += solid2.cylinder(
                    h=self.coin_thickness, d=self.screw_hole_diameter * 3, _fn=self.fn
                ).translate(location)
                coin -= (
                    solid2.cylinder(h=2, d=self.nut_width, _fn=6)
                    .translate(location)
                    .up(3)
                )  # fn=6 cleverly makes it a hexagon

        # create 4 screw holes
        for location in self.hole_locations():
            coin -= solid2.cylinder(
                h=self.coin_thickness, d=self.screw_hole_diameter, _fn=self.fn
            ).translate(location)

        return coin


class ArchimedeanSpiralString:
    """
    A class to represent a string of characters arranged in an Archimedean spiral.

    The Archimedean spiral is a spiral with a constant separation between its turns,
    making it suitable for arranging a sequence of characters with a constant distance
    between them. The class takes a string and generates the characters as 3D text
    objects, positioned along the spiral. The characters can be either outward facing
    or inward facing.

    Attributes:
        string (str): The string of characters to be arranged in a spiral.
        letter_size (float mm): The size of each character in the spiral.
        dot_dist (float degrees): The distance between the characters along the spiral.
        init_degrees (float degrees): The initial angle (in degrees) for positioning the first character.
        spiral_separation (float degrees): The constant separation between the turns of the spiral.

    Methods:
        generate_letters(outward_facing=True): Generates a list of 3D text objects representing
            the characters in the spiral, with the specified orientation.
        calculate_radius(degrees): Calculates the radius of the spiral at a given angle (in degrees).
        calculate_degree_step(degrees): Calculates the angular step (in degrees) between characters
            based on their position along the spiral.
        find_degrees(): Calculates the list of angles (in degrees) for positioning each character along the spiral.
    """

    def __init__(
        self,
        string,
        letter_size,
        dot_dist,
        init_degrees,
        spiral_separation,
    ):
        self.string = string
        self.letter_size = letter_size
        self.dot_dist = dot_dist
        self.init_degrees = init_degrees
        self.spiral_separation = spiral_separation

    def generate_letters(self, outward_facing=False):
        degree_list = self.find_degrees()
        degree_list.reverse()
        letters = []
        letter_orientation = -90
        if outward_facing:
            letter_orientation = -270
        for i, theta in enumerate(degree_list):
            letters.append(
                solid2.text(
                    font="Liberation Mono:style=Bold",
                    halign="center",
                    size=self.letter_size,
                    text=self.string[i],
                    valign="center",
                )
                .rotate([0, 0, letter_orientation])
                .translate(
                    [math.radians(self.spiral_separation) * math.radians(theta), 0, 0]
                )
                .rotate([0, 0, theta])
            )
        return letters

    def calculate_radius(self, degrees):
        return (
            math.radians(self.spiral_separation) * math.radians(degrees) + 1e-8
        )  # avoid division by zero

    def calculate_degree_step(self, degrees):
        radius = self.calculate_radius(degrees)
        acos_input = (2 * radius**2 - self.dot_dist**2) / (2 * radius**2)
        acos_input = max(
            min(acos_input, 1), -1
        )  # Clip the input value to the valid range [-1, 1]
        radian_step = math.acos(acos_input)
        return math.degrees(radian_step)

    def find_degrees(self):
        degrees = [self.init_degrees]
        for count in range(1, len(self.string)):
            degrees.append(degrees[-1] + self.calculate_degree_step(degrees[-1]))
        return degrees


class BitcoinWallet:
    def __init__(self, seed_phrase=None):
        if seed_phrase:
            self.seed_phrase = seed_phrase
        else:
            self.seed_phrase = self.generate_seed_phrase()
        self.wallet = self.create_wallet(self.seed_phrase)
        self.address = self.get_address(self.wallet)

    @staticmethod
    def generate_seed_phrase():
        strength = 128  # 128 bits for a 12-word seed phrase
        entropy = secrets.token_bytes(strength // 8)
        mnemo = Mnemonic("english")
        seed_phrase = mnemo.to_mnemonic(entropy)
        return seed_phrase

    @staticmethod
    def create_wallet(seed_phrase):
        seed = Mnemonic("english").to_seed(seed_phrase)
        wallet = HDKey.from_seed(seed, network="bitcoin")
        return wallet

    @staticmethod
    def get_address(wallet):
        # https://github.com/bitcoin/bips/blob/master/bip-0084.mediawiki
        # 84 corresponds to bip84 and provides native segwit address space
        derivation_path = f"m/84'/0'/0'/0/0"
        child_key = wallet.subkey_for_path(derivation_path)
        # see https://unchained.com/blog/bitcoin-address-types-compared/
        return child_key.address(encoding="bech32", script_type="p2wpkh")
