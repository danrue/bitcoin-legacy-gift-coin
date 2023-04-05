import math
from solid2 import *
from datetime import datetime
import coin_lib

coin_diameter = coin_lib.coin_diameter
coin_thickness = coin_lib.coin_thickness
fn = coin_lib.fn

# Retrieve basic coin shape
coin = coin_lib.common_coin()

# Write out "bitcoin" on the back side in negative space
coin -= (
    text(
        "bitcoin",
        size=10,
        halign="center",
        valign="center",
        font="Liberation Sans:style=Bold Italic",
    )
    .linear_extrude(height=1)
    .mirror([1, 0, 0])
    .rotate([180, 180, 0])
)

# Import BitcoinSign.svg onto face of coin
coin += (
    import_(file="BitcoinSign.svg")
    .linear_extrude(height=coin_thickness - 3)
    .scale([0.52, 0.52, 1])
    .translate([-18, -24, 3])
)

# Write "LIBERTY" across the top
for letter in coin_lib.ArchimedeanSpiralString(
    string="LIBERTY",
    letter_size=5,
    dot_dist=15,
    init_degrees=360 * 6,
    spiral_separation=360 / 8,
).generate_letters():
    coin += letter.linear_extrude(height=0.6).up(3).rotate([0, 0, 5])

# Add year
for letter in coin_lib.ArchimedeanSpiralString(
    string=str(datetime.now().year)[::-1],
    letter_size=5,
    dot_dist=5,
    init_degrees=360 * 6,
    spiral_separation=360 / 8,
).generate_letters(outward_facing=True):
    coin += letter.linear_extrude(height=0.6).up(3).rotate([0, 0, -103])

coin.save_as_scad()
