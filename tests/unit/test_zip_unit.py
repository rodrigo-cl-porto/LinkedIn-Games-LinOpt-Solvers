from linkedin_games import Zip
import pytest


def test_zip_should_raise_error_when_numbered_squares_has_duplicates():
    with pytest.raises(ValueError) as exc_info:
        Zip(
            size=6,
            numbered_squares=[(1,3), (1,3), (1,4), (6,4), (3,5), (4,4), (4,2), (5,2), (6,3), (3,3), (2,5)]
        )
    assert str(exc_info.value) == "The numbered squares list has duplicated squares."
