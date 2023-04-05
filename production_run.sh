#!/bin/bash

set -eoux pipefail

# Serial numbers to generate
serial_numbers="
0001
0002
0003
"
prusa_config="15mm_prusa_petg_config.ini"

for sn in ${serial_numbers}; do
    pipenv run python bottom_coin.py "generate" "${sn}"
    openscad -q -o bottom_coins/bottom_coin_sn${sn}.stl bottom_coins/bottom_coin_sn${sn}.scad
    prusa-slicer \
                 --slice bottom_coins/bottom_coin_sn${sn}.stl \
                 --output bottom_coins/bottom_coin_sn${sn}.gcode \
                 --load ${prusa_config}
    prusa-slicer --duplicate 2 \
                 --slice bottom_coins/bottom_coin_sn${sn}.stl \
                 --output bottom_coins/2xbottom_coin_sn${sn}.gcode \
                 --load ${prusa_config}
done
