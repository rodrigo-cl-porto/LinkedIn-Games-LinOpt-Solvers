from linkedin_games import Zip
import pytest

def test_zip_must_not_accept_size_zero():
    with pytest.raises(ValueError) as exc_info:
        Zip(
            size=0,
            numbered_squares=[(1,3), (1,4), (6,4), (3,5), (4,4), (4,2), (5,2), (6,3), (3,3), (2,5)]
        )
    assert str(exc_info.value) == "Game's size must be a positive integer. Got 0 instead."

def test_zip_must_not_accept_negative_size():
    with pytest.raises(ValueError) as exc_info:
        Zip(
            size=-100,
            numbered_squares=[(1,3), (1,4), (6,4), (3,5), (4,4), (4,2), (5,2), (6,3), (3,3), (2,5)]
        )
    assert str(exc_info.value) == "Game's size must be a positive integer. Got -100 instead."

def test_zip_should_raise_error_when_numbered_squares_has_duplicates():
    with pytest.raises(ValueError) as exc_info:
        Zip(
            size=6,
            numbered_squares=[(1,3), (1,3), (1,4), (6,4), (3,5), (4,4), (4,2), (5,2), (6,3), (3,3), (2,5)]
        )
    assert str(exc_info.value) == "The numbered squares list has duplicated squares."

def test_zip_must_not_accept_empty_numbered_squares():
    with pytest.raises(ValueError) as exc_info:
        Zip(size=6, numbered_squares=[])
    assert str(exc_info.value) == "The quantity of numbered squares is too small for the game. Got a total of 0 numbered squares."
