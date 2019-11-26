from appbase import global_db as gdb


class Settings(gdb.Model):
    __tablename__ = 'settings'
    settings_id = gdb.Column(gdb.Integer, primary_key=True)
    settings_key = gdb.Column(gdb.String(50))
    settings_value = gdb.Column(gdb.String(1000))

    def __init__(self, settings_key, settings_value):
        self.settings_key = settings_key
        self.settings_value = settings_value

    def todict(self):
        return {"settings_id": self.settings_id,
                "settings_key": self.settings_key,
                "settings_value": self.settings_value}
