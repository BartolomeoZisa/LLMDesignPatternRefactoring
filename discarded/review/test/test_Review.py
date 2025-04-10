import pytest
from base.Review import Rating 

def test_rating_initialization():
    review = Rating(7)
    assert review.get_description("Customer") == "7", "Rating should be initialized correctly"

def test_adding_merchant_comments():
    review = Rating(8)
    review.add_merchant_comment("Great service!")
    review.add_merchant_comment("Fast delivery!")

    assert review.get_description("Customer") == "8 Great service! Fast delivery!", \
        "Merchant comments should be added and displayed correctly"

def test_adding_commission_comments():
    review = Rating(9)
    review.add_commission_comment("Verified quality.")
    review.add_commission_comment("Trusted seller.")

    assert review.get_description("Customer") == "9", \
        "Commission comments should not be visible to customers"

    assert review.get_description("Commission") == "9 Verified quality. Trusted seller.", \
        "Commission comments should be visible to commission members"

def test_adding_both_types_of_comments():
    review = Rating(10)
    review.add_merchant_comment("Excellent product!")
    review.add_commission_comment("Approved by board.")

    assert review.get_description("Customer") == "10 Excellent product!", \
        "Only merchant comments should be visible to customers"
    
    assert review.get_description("Commission") == "10 Excellent product! Approved by board.", \
        "Both merchant and commission comments should be visible to commission members"

def test_private_attribute_encapsulation():
    review = Rating(8)
    with pytest.raises(AttributeError):
        _ = review.__merchant_comments  # Should raise an error because it's private

    with pytest.raises(AttributeError):
        _ = review.__commission_comments  # Should raise an error because it's private

