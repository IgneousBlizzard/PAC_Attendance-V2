import json
from datetime import datetime, timedelta
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
								user_in = input("Username: ")
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
	
def run_remove_user_loop():
	while True:
		user_input = input("User to remove, or 'e' to exit: ")
		if user_input in staff.staff_list:
			if input("Are you sure you want to remove", user_input, "from data.json?") == "y":
				staff.staff_list.pop(user_input)
		elif user_input == "e":
			break

def run_add_user_loop():
	user_input = input("User to add (Full username): ")
	if user_input in staff.staff_list:
		print("User already present.")
	else:
		if input("Are you sure you want to add", user_input, "to the staff list?") == "y":
			role = input("Are they a pilot? (y/n) ")
			if role == "y":
				staff.add_user(user_input, True)
			elif role == "n":
				staff.add_user(user_input, False)
			else:
				print("Invalid entry.")

# !! BEWARE !!! EVIL ASS FUNCTION !!! DO NOT TOUCH !!! YOU WILL REGRET IT !!!
def run_leaderboard_loop():
	while True:
		clear_term()
		print("|| PAC ACTIVITY LEADERBOARD V2 ||\n\n1. Days since last attendance\n2. 30 day activity\n3. TOTAL recorded activity\n'e'. exit")
		user_input = input(">> ")

		if user_input == "1":
			sorted_staff = sorted(
				staff.staff_list.values(),
				key= lambda s: max(s.attendance) if s.attendance else datetime.min,
				reverse= False
			)

			clear_term()
			print("|| Last Active ||\n")


			for i in sorted_staff:
				try: 
					most_recent_attendance = max(i.attendance).date()
					days_to_today = (datetime.today().date() - most_recent_attendance).days
				except:
					days_to_today = -1
				if days_to_today != -1:
					print(i.username + ":", days_to_today)

			input("\nEnter to continue. ")

		elif user_input == "2":
			today = datetime.today().date()
			thirty_days_ago = today - timedelta(days=30)

			clear_term()
			print("|| 30 Day Activity ||\n")

			thirty_day_activity = {}

			for member in staff.staff_list.values():
				count = sum(1 for datetime in member.attendance if datetime.date() >= thirty_days_ago)
				thirty_day_activity[member] = count
			
			thirty_day_activity = sorted(thirty_day_activity.items(), key= lambda x: x[1], reverse= True)

			for user_object, days in thirty_day_activity:
				print(user_object.username, days)

			
			input("\nEnter to continue. ")
		elif user_input == "3":
			pass
		elif user_input == "e":
			break

while True:
	clear_term()
	print("|| PAC ATTENDANCE TRACKER V2 ||\n\n1. Add new event.\n2. Export to leaderboard\n3. Add new user\n4. Remove user")

	user_input = input(">> ")
	if user_input == "1":
		run_event_loop()
		clear_term()

	elif user_input == "2":
		run_leaderboard_loop()
		clear_term()

	elif user_input == "3":
		run_add_user_loop()
		clear_term()

	elif user_input == "4":
		run_remove_user_loop()
		clear_term()