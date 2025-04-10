from abc import ABC, abstractmethod

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

# Creator Class
class Creator:
    def generate_report(self, type):
        if type == "Administrator":
            return AdministratorReport()
        elif type == "Citizen":
            return CitizenReport()
        elif type == "Manager":
            return ManagerReport()
        else:
            raise ValueError(f"Invalid report type: {type}")

    def get_pdf_report(self, type):
        report = self.generate_report(type)
        return f"Generating PDF for {report.generate()}"




