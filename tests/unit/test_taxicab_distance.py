from linkedin_games.domain.utils.taxicab_distance import TaxicabDistance


def test_taxicab_distance():
    assert TaxicabDistance.calculate((1,1), (1,1)) == 0
    assert TaxicabDistance.calculate((1,1), (1,2)) == 1
    assert TaxicabDistance.calculate((1,1), (2,2)) == 2
