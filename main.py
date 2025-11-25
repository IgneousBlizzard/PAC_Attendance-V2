import json
import datetime

class staff:
    staff_list = {}
    def __init__(self, username, attendance=None, role=False): # Attendance = List of all recorded events attended | role = True (Pilot) / False (Crew Chief)
        self.username = username
        self.attendance = attendance if attendance is not None else []
        self.role = role

    def format_json():
        return {
            "attendance": self.attendance,
            "role": self.role
        }

    @classmethod
    def save_to_json(cls, filename):
        pass