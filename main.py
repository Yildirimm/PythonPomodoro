import csv
import time
import winsound
import os.path
from datetime import datetime
import Category_handler as ch
import Counter as Counter

import schedule

cat_general = []
cat_flag = 0

if __name__ == '__main__':

	the_day = datetime.today().strftime('%Y-%m-%d')

	# make a category object
	c1 = ch.Category()

	# print(c1.category_name)

	###### 1- print the existing categories
	# and if they are empty, redirect him to add categories
	cat, the_last_one = c1.read_the_categories()
	#print("cat", len(cat), "|| and the last line ", the_last_one)

	###### 1.1 choose the categories
	if len(cat) == 0:
		print("there is no category right now! Want to add some category ?")
		print("[main]c1.category_name: ", c1.category_name)
		# Category.build_the_category(c1)

		c1.build_the_category()
		c1.store_categories(cat_flag)

	###### 2- If he wants to add category, redirect him to add categories
	else:
		a = input("[main]There are categories on table but if you want to add even more [y/n]?: ")

		if a == "y":
			c1.build_the_category()
			c1.store_categories(cat_flag)

	###### 3- Choose one of the existing categories
	chosen_one = c1.choose_category()

	###### 4- Start the Pomodoro Timer

	# input time in seconds
	# Kategori seçildi ve zamanı giriliyor
	rows, cols = (4,2)
	cycle = [[0 for i in range(cols)] for j in range(rows)]
	loop_number = 0
	pomodoro_time = 0
	while True:
		t = str(input("Enter the time as MM:SS, "))
		_, mins, secs = Counter.check_shape(t)
		# min, sec = t.split(":")
		# print("mins secs ", mins,":", secs)
		# print(type(clean_t),type(mins),type(secs))
		count_t = (int(mins) * 60) + int(secs)
		Counter.countdown(int(count_t))
		Counter.beep()

		loop_number += 1
		pomodoro_time += count_t
		cycle[loop_number].append(count_t)
		print("loop_number, count_t, pomodoro_total_time : ",loop_number, count_t, pomodoro_time)
		breaker = str(input("\nDo you want to break the cycle [y/n]?: "))
		if breaker == "y":
			count_t = pomodoro_time
			break
	print("\n, cycle here", cycle)

	###### 5- Store the time and category into a file
	chosen_one.time_spent = round(count_t / 60, 3)

	print("\nchosen one: ", chosen_one.category_name, " ,time spent: ", chosen_one.time_spent)
	# ch.Category.store_categories(chosen_one.time_spent)  # stores in seconds

	Counter.write_to_file(the_day, chosen_one.category_name, count_t)

	schedule.every(2).seconds.do(c1.calculate_by_time())

	###### 6- Read from the pomodoro_records.csv and store to the categories.csv
	# TODO: write the chosen ones into pomodoro, and make them to be summed and written into categories.

	# TODO: add the hour stamp to the pomodoro_records.csv also
    # TODO: add a function to add the studied stuff's hour on the records and it should ask at the beginning of the program

	# TODO: add timestamps to pomodoro records, as start-finish then you can get the time-interval from these
	# TODO: add a function to see if computer is on or not

	# TODO: add functions to categories to draw graphs
