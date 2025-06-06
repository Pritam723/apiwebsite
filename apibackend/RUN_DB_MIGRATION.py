from standardInterface.stardardInterfaceTables.PeakHours import PeakHours
from standardInterface.stardardInterfaceTables.LimitedTenders import LimitedTenders
from standardInterface.stardardInterfaceTables.SingleTender import SingleTender
from standardInterface.stardardInterfaceTables.OpenTender import OpenTender
from standardInterface.stardardInterfaceTables.RajbhasaPatrika import RajbhasaPatrika
from standardInterface.stardardInterfaceTables.ShutdownAvailedList import ShutdownAvailedList
from standardInterface.stardardInterfaceTables.YearAheadForecastingError import YearAheadForecastingError
from standardInterface.stardardInterfaceTables.MonthAheadForecastingError import MonthAheadForecastingError
from standardInterface.stardardInterfaceTables.WeekAheadRollingForecast import WeekAheadRollingForecast
from standardInterface.stardardInterfaceTables.WeekAheadForecastingError import WeekAheadForecastingError
from standardInterface.stardardInterfaceTables.IntraDayForecastingError import IntraDayForecastingError
from standardInterface.stardardInterfaceTables.DayAheadForecastingError import DayAheadForecastingError
from standardInterface.stardardInterfaceTables.ATCViolationDaily import ATCViolationDaily
from standardInterface.stardardInterfaceTables.ATCViolationWeekly import ATCViolationWeekly
from standardInterface.stardardInterfaceTables.ATCViolationMonthly import ATCViolationMonthly
from standardInterface.stardardInterfaceTables.FRC import FRC
from standardInterface.stardardInterfaceTables.TransmissionElementAvailability import TransmissionElementAvailability
from standardInterface.stardardInterfaceTables.FinalSchedule import FinalSchedule
from standardInterface.stardardInterfaceTables.Telemetry import Telemetry
from standardInterface.stardardInterfaceTables.ScadavsSEM import ScadavsSEM
from standardInterface.stardardInterfaceTables.GenerationOutage import GenerationOutage
from standardInterface.stardardInterfaceTables.DailyPSPReport import DailyPSPReport
from standardInterface.stardardInterfaceTables.MonthlyReports import MonthlyReports
from standardInterface.stardardInterfaceTables.WeeklyReports import WeeklyReports
from standardInterface.stardardInterfaceTables.AnnualReports import AnnualReports
from standardInterface.stardardInterfaceTables.QuarterlyReports import QuarterlyReports

from standardInterface.stardardInterfaceTables.VDIDaily import VDIDaily
from standardInterface.stardardInterfaceTables.VDIMonthly import VDIMonthly
from standardInterface.stardardInterfaceTables.VDIWeekly import VDIWeekly
from standardInterface.stardardInterfaceTables.MonthlyDeviationReport import MonthlyDeviationReport
from standardInterface.stardardInterfaceTables.AnnualCompendium import AnnualCompendium
from standardInterface.stardardInterfaceTables.GridEventsFlashreport import GridEventsFlashreport
from standardInterface.stardardInterfaceTables.WeatherRelatedEvents import WeatherRelatedEvents
from standardInterface.stardardInterfaceTables.TechnicalReports import TechnicalReports
from standardInterface.stardardInterfaceTables.FTCDocuments import FTCDocuments

from standardInterface.stardardInterfaceTables.ReconciliationCTU import ReconciliationCTU
from standardInterface.stardardInterfaceTables.ReconciliationApplicant import ReconciliationApplicant
from standardInterface.stardardInterfaceTables.Disbursements import Disbursements
from standardInterface.stardardInterfaceTables.Refunds import Refunds
from standardInterface.stardardInterfaceTables.DSMDisbursementLetter import DSMDisbursementLetter
from standardInterface.stardardInterfaceTables.DSMReconcilation import DSMReconcilation
from standardInterface.stardardInterfaceTables.ReactiveReconcilation import ReactiveReconcilation
from standardInterface.stardardInterfaceTables.AGCReconciliation import AGCReconciliation
from standardInterface.stardardInterfaceTables.RRASReconciliation import RRASReconciliation
from standardInterface.stardardInterfaceTables.ReactiveDisbursementLetter import ReactiveDisbursementLetter
from standardInterface.stardardInterfaceTables.SEMData import SEMData
from standardInterface.stardardInterfaceTables.TimeCorrectionManual import TimeCorrectionManual
from standardInterface.stardardInterfaceTables.MeteringSoftware import MeteringSoftware
from standardInterface.stardardInterfaceTables.MeteringError import MeteringError
from standardInterface.stardardInterfaceTables.MeteringManual import MeteringManual
from standardInterface.stardardInterfaceTables.SupplementaryAndPLIBill import SupplementaryAndPLIBill
from standardInterface.stardardInterfaceTables.QuarterlyReconciliationStatement import QuarterlyReconciliationStatement
from standardInterface.stardardInterfaceTables.PSDF import PSDF
from standardInterface.stardardInterfaceTables.CongestionReport import CongestionReport
from models.models import User, UserRoles,PagePermissions,Albums,HRDocuments,Tenders

def runMigration(app, db):
    with app.app_context():
        db.create_all()