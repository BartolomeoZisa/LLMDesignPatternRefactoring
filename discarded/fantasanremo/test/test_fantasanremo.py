import pytest
from alternative.fantasanremo import Artist  # Assuming the Artist class is in a file named artista.py


def test_calculate_score_BM_starter():
    artist = Artist("Mario", "starter")
    assert artist.calculate_score_BM(10) == 10

def test_calculate_score_BM_captain():
    artist = Artist("Luca", "captain")
    assert artist.calculate_score_BM(10) == 10

def test_calculate_score_BM_reserve():
    artist = Artist("Giovanni", "reserve")
    assert artist.calculate_score_BM(10) == 0

def test_calculate_score_BM_default():
    artist = Artist("Paolo", "unknown")
    assert artist.calculate_score_BM(10) == 0

def test_calculate_position_score_starter():
    artist = Artist("Mario", "starter")
    assert artist.calculate_position_score(10) == 10

def test_calculate_position_score_captain():
    artist = Artist("Luca", "captain")
    assert artist.calculate_position_score(10) == 20

def test_calculate_position_score_reserve():
    artist = Artist("Giovanni", "reserve")
    assert artist.calculate_position_score(10) == 0

def test_calculate_position_score_default():
    artist = Artist("Paolo", "unknown")
    assert artist.calculate_position_score(10) == 0
