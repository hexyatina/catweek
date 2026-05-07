from datetime import time

import pytest

from app.utils.time import parse_time_slot


def test_valid_parses_correctly():
    start, end = parse_time_slot("08:30-10:05")
    assert start == time(8, 30)
    assert end == time(10, 5)


def test_midnight_boundary():
    start, end = parse_time_slot("00:00-00:00")
    assert start == time(0, 0)
    assert end == time(0, 0)


def test_end_of_day():
    start, end = parse_time_slot("23:59-23:59")
    assert start == time(23, 59)


def test_missing_dash_raises():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time_slot("0830-1005")


def test_wrong_separator_raises():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time_slot("08:30/10:05")


def test_empty_string_raises():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time_slot("")


def test_none_raises():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time_slot(None)


def test_out_of_range_hour_raises():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time_slot("25:00-26:00")


def test_extra_parts_raises():
    with pytest.raises(ValueError, match="Invalid time format"):
        parse_time_slot("08:30-10:05-12:00")
