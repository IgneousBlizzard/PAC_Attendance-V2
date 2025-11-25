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
    
    @classmethod
    def find_from_partial(cls, partial):
        matches = []
        for username, member in cls.staff_list.items():
            if partial.lower() in username.lower():
                matches.append(member)
        return matches
    
    @classmethod
    def add_user(cls, username):
        pass

    @classmethod
    def remove_user(cls, username):
        pass

    @classmethod
    def add_event(cls, username, event):
        pass


staff.load_from_json("data.json")

print("'e' to exit any of the following.")

year = None
month = None
day = None
role = False # Default to CC
while True:
    year = input("Year: ")
    if year == "e":
        year = None
        break
    else:
        while True:
            month = input("Month: ")
            if month == "e":
                month = None
                break
            else:
                while True:
                    day = input("Day: ")
                    if day == "e":
                        day = None
                        break
                    else:
                        while True:
                            user_in = input(f"Username ({role}): ")
                            if user_in == "e":
                                user_in = None
                                break
                            else:
                                matches = staff.find_from_partial
                                if len(matches) > 1:
                                    pass
                                elif len(matches) == 1:
                                    pass
                                else:
                                    print("No matches found.")
                                    continue