all: black top_coin.scad top_coin.stl bottom_coin.scad bottom_coin.stl

quick_build: black top_coin.scad bottom_coin.scad

black:
	pipenv run black *.py

top_coin.scad: top_coin.py coin_lib.py
	pipenv run python top_coin.py
top_coin.stl: top_coin.scad
	openscad -o top_coin.stl top_coin.scad
	prusa-slicer --slice top_coin.stl --output top_coin.gcode --load 15mm_prusa_petg_config.ini
	prusa-slicer --duplicate 6 --slice top_coin.stl --output 6xtop_coin.gcode --load 15mm_prusa_petg_config.ini

bottom_coin.scad: bottom_coin.py coin_lib.py
	rm -f coin_data/bottom_coin_sn0000.json
	pipenv run python bottom_coin.py "NATION CAT SENIOR UTILITY ENLIST NEXT HOST SYRUP WOMAN DIAGRAM SOCIAL ARRANGE" "0000"
bottom_coin.stl: bottom_coin.scad
	openscad -o bottom_coins/bottom_coin_sn0000.stl bottom_coins/bottom_coin_sn0000.scad
	prusa-slicer --slice bottom_coins/bottom_coin_sn0000.stl --output bottom_coins/bottom_coin_sn0000.gcode --load 15mm_prusa_petg_config.ini
	prusa-slicer --duplicate 2 --slice bottom_coins/bottom_coin_sn0000.stl --output bottom_coins/2xbottom_coin_sn0000.gcode --load 15mm_prusa_petg_config.ini
