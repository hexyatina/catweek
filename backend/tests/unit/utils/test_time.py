import pytest
from datetime import time
from src.app.utils.time import parse_time_slot

@pytest.mark.parametrize("input_str, expected_start, expected_end", [
    ("12:00-13:30", time(12, 0), time(13, 30)),
    ("00:00-23:59", time(0, 0), time(23, 59)),
    ("9:05-10:10", time(9, 5), time(10, 10)),  # Single digits
])
def test_parse_time_slot_valid(input_str, expected_start, expected_end):
    """Test correctly formatted time ranges."""
    start, end = parse_time_slot(input_str)
    assert start == expected_start
    assert end == expected_end

@pytest.mark.parametrize("invalid_input", [
    "12:10",            # Missing hyphen
    "12:00-25:00",      # Invalid hour
    "12:60-13:00",      # Invalid minute
    "abc-def",          # Not numbers
    "12:00:00-13:00",   # Wrong format
    None,               # Not a string
    1210,               # Integer input
    "",                 # Empty string
])
def test_parse_time_slot_invalid(invalid_input):
    """Test that invalid inputs raise a descriptive ValueError."""
    with pytest.raises(ValueError) as exc_info:
        parse_time_slot(invalid_input)
    assert "Invalid time format" in str(exc_info.value)
