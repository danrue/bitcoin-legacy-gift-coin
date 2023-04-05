import pytest
from unittest.mock import MagicMock
from coin_lib import BaseCoin
import coin_lib

# Mock the solid2 library functions
solid2_mock = MagicMock()
coin_lib.solid2 = solid2_mock


@pytest.fixture
def base_coin():
    return BaseCoin()


class TestBaseCoin:
    def test_init(self, base_coin):
        assert base_coin.coin_diameter == 76.2
        assert base_coin.coin_thickness == 5.0
        assert base_coin.screw_hole_diameter == 2.5
        assert base_coin.nut_width == 4.0
        assert base_coin.fn == 512

    def test_hole_locations(self, base_coin):
        hole_locs = base_coin.hole_locations()
        assert len(hole_locs) == 4

        for loc in hole_locs:
            assert len(loc) == 3
            assert isinstance(loc[0], float)
            assert isinstance(loc[1], float)
            assert loc[2] == 0

    def test_common_coin(self, base_coin):
        common_coin = base_coin.common_coin()

        # Verify calls to solid2 functions
        solid2_mock.cylinder.assert_called()

        # Verify the created coin object
        assert common_coin is not None

    def test_common_coin_bottom(self, base_coin):
        common_coin_bottom = base_coin.common_coin(bottom=True)

        # Verify calls to solid2 functions
        solid2_mock.cylinder.assert_called()

        # Verify the created coin object
        assert common_coin_bottom is not None
