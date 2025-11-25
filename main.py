import json
from datetime import datetime

class staff:
    staff_list = {}
    def __init__(self, username, attendance=None, role=False): # Attendance = List of all recorded events attended | role = True (Pilot) / False (Crew Chief)
        self.username = username
        self.attendance = attendance if attendance is not None else []
        self.role = role
        staff.staff_list[username] = self

    def format_json(self):
        return {
            "attendance": [date.isoformat() for date in self.attendance],
            "role": self.role
        }

    @classmethod
    def save_to_json(cls, filename):
        with open(filename, "w") as f:
            data = {username: member.format_json() for username, member in cls.staff_list.items()}
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        cls.staff_list.clear()
        for username, member_data in data.items():
            attendance_dates = [datetime.fromisoformat(d) for d in member_data.get("attendance", [])]
            staff(
                username,
                attendance=attendance_dates, role=member_data.get("role", False)
            )

    @classmethod
    def get(cls, username):
        return cls.staff_list.get(username)
    

staff("IgneousKaiser", [datetime(2025,1,1), datetime(2025,2,10)], False)
staff("fishpint", [datetime(2025,2,6), datetime(2025,4,12)], True)

staff.save_to_json("data.json")