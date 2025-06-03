import pytest
from refactored.cafecito import (
    Espresso, HouseBlend, DarkRoast, Decaf,
    Milk, Mocha, Soy, Whip
)

# --------------------------
# 1. Base Beverages Only
# --------------------------
def test_espresso_base():
    drink = Espresso()
    assert drink.get_description() == "Espresso"
    assert drink.cost() == pytest.approx(1.99)

def test_house_blend_base():
    drink = HouseBlend()
    assert drink.get_description() == "House Blend Coffee"
    assert drink.cost() == pytest.approx(0.89)

def test_dark_roast_base():
    drink = DarkRoast()
    assert drink.get_description() == "Dark Roast Coffee"
    assert drink.cost() == pytest.approx(0.99)

def test_decaf_base():
    drink = Decaf()
    assert drink.get_description() == "Decaf Coffee"
    assert drink.cost() == pytest.approx(1.05)

# --------------------------
# 2. Each Decorator Once
# --------------------------
def test_milk_once():
    drink = Milk(Espresso())
    assert drink.get_description() == "Espresso, Milk"
    assert drink.cost() == pytest.approx(1.99 + 0.10)

def test_mocha_once():
    drink = Mocha(Espresso())
    assert drink.get_description() == "Espresso, Mocha"
    assert drink.cost() == pytest.approx(1.99 + 0.20)

def test_soy_once():
    drink = Soy(Espresso())
    assert drink.get_description() == "Espresso, Soy"
    assert drink.cost() == pytest.approx(1.99 + 0.15)

def test_whip_once():
    drink = Whip(Espresso())
    assert drink.get_description() == "Espresso, Whip"
    assert drink.cost() == pytest.approx(1.99 + 0.10)

# --------------------------
# 3. Same Decorator Twice
# --------------------------
def test_double_mocha():
    drink = Mocha(Mocha(Espresso()))
    assert drink.get_description() == "Espresso, Mocha, Mocha"
    assert drink.cost() == pytest.approx(1.99 + 0.20 + 0.20)

def test_double_whip():
    drink = Whip(Whip(HouseBlend()))
    assert drink.get_description() == "House Blend Coffee, Whip, Whip"
    assert drink.cost() == pytest.approx(0.89 + 0.10 + 0.10)

# --------------------------
# 4. Mixed Decorators
# --------------------------
def test_soy_milk_whip():
    drink = Soy(Milk(Whip(Espresso())))
    assert drink.get_description() == "Espresso, Whip, Milk, Soy"
    assert drink.cost() == pytest.approx(1.99 + 0.10 + 0.10 + 0.15)

def test_mocha_soy():
    drink = Soy(Mocha(DarkRoast()))
    assert drink.get_description() == "Dark Roast Coffee, Mocha, Soy"
    assert drink.cost() == pytest.approx(0.99 + 0.20 + 0.15)

def test_milk_mocha_whip():
    drink = Whip(Mocha(Milk(Decaf())))
    assert drink.get_description() == "Decaf Coffee, Milk, Mocha, Whip"
    assert drink.cost() == pytest.approx(1.05 + 0.10 + 0.20 + 0.10)

