import pytest
from coin_lib import ArchimedeanSpiralString
import math
from unittest.mock import MagicMock, patch
import solid2


# Test data
test_data = {
    "string": "Hello",
    "letter_size": 10,
    "dot_dist": 1,
    "init_degrees": 0,
    "spiral_separation": 5,
}


@pytest.fixture
def spiral_string():
    return ArchimedeanSpiralString(**test_data)


class TestArchimedeanSpiralString:
    def test_init(self, spiral_string):
        assert spiral_string.string == test_data["string"]
        assert spiral_string.letter_size == test_data["letter_size"]
        assert spiral_string.dot_dist == test_data["dot_dist"]
        assert spiral_string.init_degrees == test_data["init_degrees"]
        assert spiral_string.spiral_separation == test_data["spiral_separation"]

    def test_calculate_radius(self, spiral_string):
        degrees = 10
        radius = spiral_string.calculate_radius(degrees)
        expected_radius = (
            math.radians(spiral_string.spiral_separation) * math.radians(degrees) + 1e-8
        )
        assert radius == expected_radius

    def test_calculate_degree_step(self, spiral_string):
        degrees = 10
        degree_step = spiral_string.calculate_degree_step(degrees)
        radius = spiral_string.calculate_radius(degrees)
        acos_input = (2 * radius**2 - spiral_string.dot_dist**2) / (2 * radius**2)
        acos_input = max(min(acos_input, 1), -1)
        radian_step = math.acos(acos_input)
        expected_degree_step = math.degrees(radian_step)
        assert degree_step == expected_degree_step

    def test_find_degrees(self, spiral_string):
        degree_list = spiral_string.find_degrees()
        assert len(degree_list) == len(test_data["string"])
        assert degree_list[0] == test_data["init_degrees"]

        for i in range(1, len(degree_list)):
            assert degree_list[i] == degree_list[
                i - 1
            ] + spiral_string.calculate_degree_step(degree_list[i - 1])

    @patch("coin_lib.solid2.text", return_value=MagicMock())
    def test_generate_letters(self, mock_text, spiral_string):
        letters = spiral_string.generate_letters()
        assert len(letters) == len(test_data["string"])
        assert mock_text.call_count == len(test_data["string"])
