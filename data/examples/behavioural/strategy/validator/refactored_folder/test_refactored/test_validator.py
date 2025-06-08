import pytest
from refactored.validator import ValidationContext, NumericValidator, AlphanumericValidator, TelNumberValidator


@pytest.fixture
def context():
    return ValidationContext()


def test_numeric_validator_valid(context):
    context.set_strategy(NumericValidator())
    assert context.validate("12345") is True
    assert context.validate("0000") is True


def test_numeric_validator_invalid(context):
    context.set_strategy(NumericValidator())
    assert context.validate("123a") is False
    assert context.validate("") is False


def test_alphanumeric_validator_valid(context):
    context.set_strategy(AlphanumericValidator())
    assert context.validate("abc123") is True
    assert context.validate("XYZ") is True


def test_alphanumeric_validator_invalid(context):
    context.set_strategy(AlphanumericValidator())
    assert context.validate("abc123!") is False
    assert context.validate(" ") is False


def test_telnumber_validator_valid(context):
    context.set_strategy(TelNumberValidator())
    assert context.validate("+1 (234) 567-8900") is True
    assert context.validate("1234567890") is True
    assert context.validate("(555) 555-5555") is True


def test_telnumber_validator_invalid(context):
    context.set_strategy(TelNumberValidator())
    assert context.validate("abc123") is False
    assert context.validate("123-456-7890x123") is False  # contains invalid character 'x'
    assert context.validate("") is False


def test_no_strategy_set_raises(context):
    with pytest.raises(RuntimeError):
        context.validate("anything")


def test_set_strategy_invalid_type_raises(context):
    with pytest.raises(TypeError):
        context.set_strategy(str)  # str is not a Validator subclass
