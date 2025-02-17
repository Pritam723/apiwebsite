from standardInterface.stardardInterfaceTables.PeakHours import PeakHours
from standardInterface.stardardInterfaceTables.LimitedTenders import LimitedTenders
from models.models import User, UserRoles,PagePermissions

def runMigration(app, db):
    with app.app_context():
        db.create_all()