import pytest
from refactored.Report import Creator, AdministratorReport, CitizenReport, ManagerReport

# Test that generate_report returns the correct report instances
@pytest.mark.parametrize("report_type,expected_class,expected_message", [
    ("Administrator", AdministratorReport, "Administrator Report"),
    ("Citizen", CitizenReport, "Citizen Report"),
    ("Manager", ManagerReport, "Manager Report"),
])
def test_generate_report_valid(report_type, expected_class, expected_message):
    creator = Creator()
    report = creator.generate_report(report_type)
    # Check that the returned report is an instance of the expected class
    assert isinstance(report, expected_class)
    # Verify the output of the generate method
    assert report.generate() == expected_message

# Test that get_pdf_report returns the correct PDF string
@pytest.mark.parametrize("report_type,expected_pdf", [
    ("Administrator", "Generating PDF for Administrator Report"),
    ("Citizen", "Generating PDF for Citizen Report"),
    ("Manager", "Generating PDF for Manager Report"),
])
def test_get_pdf_report_valid(report_type, expected_pdf):
    creator = Creator()
    pdf_output = creator.get_pdf_report(report_type)
    assert pdf_output == expected_pdf

# Test that an invalid report type raises a ValueError
def test_generate_report_invalid():
    creator = Creator()
    with pytest.raises(ValueError) as exc_info:
        creator.generate_report("InvalidType")
    # Optionally check that the error message contains the expected substring
    assert "Invalid report type" in str(exc_info.value)
