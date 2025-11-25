import json
from datetime import datetime
import os

class staff:
    staff_list = {}
    def __init__(self, username, attendance=None, role=False): # Attendance = List of all recorded events attended | role = True (Pilot) / False (Crew Chief)
        self.username = username
        self.attendance = attendance if attendance is not None else []
        self.role = role if role is not None else False
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
    def add_user(cls, username, role):
        staff.staff_list[username] = staff(username, role=role)

    @classmethod
    def remove_user(cls, username):
        staff.staff_list.pop(username)

    @classmethod
    def add_event(cls, user_object, event):
        staff.staff_list[user_object.username].attendance.append(event)
        print(user_object.username, user_object.attendance)

staff.load_from_json("data.json")

def clear_term():
    os.system("cls")

def run_event_loop():

    print("'e' to exit any of the following.")
    year = None
    month = None
    day = None
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
                                user_in = input(f"Username: ")
                                if user_in == "e":
                                    user_in = None
                                    break
                                else:
                                    matches = staff.find_from_partial(user_in)
                                    if len(matches) > 1:
                                        print("Multiple users found.\n", ", ".join(i.username for i in matches), "\n")
                                        continue
                                    elif len(matches) == 1:
                                        staff.add_event(matches[0], datetime.strptime(f"{month}{day}{year}", "%m%d%y"))
                                    else:
                                        print("No matches found.")
        
        if input("Save work? (y/n) ") == "y":
            staff.save_to_json("data.json")
            break
        else:
            break
    
def run_remove_user_loop():
    pass

while True:
    print("|| PAC ATTENDANCE TRACKER ||\n\n1. Add new event.\n2. Export to leaderboard\n3. Add new user\n4. Remove user")

    user_input = input(">> ")
    if user_input == "1":
        run_event_loop()
        clear_term()

    elif user_input == "2":
        pass

    elif user_input == "3":
        pass