from abc import ABC, abstractmethod

# Abstract Report Class
class Report(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

# Concrete Report Classes
class AdministratorReport(Report):
    def generate(self) -> str:
        return "Administrator Report"

class CitizenReport(Report):
    def generate(self) -> str:
        return "Citizen Report"

class ManagerReport(Report):
    def generate(self) -> str:
        return "Manager Report"

# Report Factory
class ReportFactory:
    _report_types = {
        "Administrator": AdministratorReport,
        "Citizen": CitizenReport,
        "Manager": ManagerReport
    }

    @staticmethod
    def create_report(report_type: str) -> Report:
        if report_type in ReportFactory._report_types:
            return ReportFactory._report_types[report_type]()
        raise ValueError(f"Invalid report type: {report_type}")

# Creator Class
class Creator:
    def generate_report(self, type: str) -> Report:
        return ReportFactory.create_report(type)
    
    def get_pdf_report(self, type: str) -> str:
        report = self.generate_report(type)
        return f"Generating PDF for {report.generate()}"




