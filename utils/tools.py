import csv
import os


def write_to_file(date, work, time_spent):
	# headers = ["date", "work_type", "time_spent(in s)"]
	# to_write = str(work)+","+str(time_spent)+" secs"+"\n"
	# to_write = [[111], str(work), str(time_spent)]

	file_exists = os.path.isfile("pomodoro_records.csv")

	with open("pomodoro_records.csv", 'a') as f:
		headers = ["date", "work_type", "time_spentInS"]
		writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)

		if not file_exists:
			writer.writeheader()  # file doesn't exist yet, write a header

		writer.writerow({'date': date, 'work_type': str(work), 'time_spentInS': str(time_spent)})


def check_shape(input_time):
	# print("input",input_time)
	# digit_len = int(len(input_time))
	# print("digit_len", digit_len)
	global split_point, min, sec

	for i, c in enumerate(input_time):
		# print(i,c)
		if c == (":" or ","):
			min = input_time[:i]
			sec = input_time[i + 1:]
			# print("min sec ", min, sec)
			split_point = input_time[i]
			return split_point, min, sec

