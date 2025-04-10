from abc import ABC, abstractmethod

#simple Factory Pattern to keep retrocompatibility with the old code
class Creator:

    def generate_report(self, type):
        if type == "Administrator":
            reportCreator = AdministratorReportCreator()
            return reportCreator.generate_report()
        elif type == "Citizen":
            reportCreator = CitizenReportCreator()
            return reportCreator.generate_report()
        elif type == "Manager":
            reportCreator = ManagerReportCreator()
            return reportCreator.generate_report()
        else:
            raise ValueError(f"Invalid report type: {type}")

    def get_pdf_report(self, type):
        report = self.generate_report(type)
        if report:
            return f"Generating PDF for {report.generate()}"
        return "Invalid report type"
            



# Abstract Creator
class ReportCreator(ABC):
    @abstractmethod
    def generate_report(self):
        pass  

    def get_pdf_report(self):
        report = self.generate_report()
        return f"Generating PDF for {report.generate()}"

# Concrete Creators
class AdministratorReportCreator(ReportCreator):
    def generate_report(self):
        return AdministratorReport()

class CitizenReportCreator(ReportCreator):
    def generate_report(self):
        return CitizenReport()

class ManagerReportCreator(ReportCreator):
    def generate_report(self):
        return ManagerReport()

# Abstract Report Class
class Report(ABC):
    @abstractmethod
    def generate(self):
        pass  

# Concrete Report Classes
class AdministratorReport(Report):
    def generate(self):
        return "Administrator Report"

class CitizenReport(Report):
    def generate(self):
        return "Citizen Report"

class ManagerReport(Report):
    def generate(self):
        return "Manager Report"
