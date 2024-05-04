import os
import os.path
import csv
import datetime
import pandas as pd
import numpy as np

from PythonPomodoro.utils import check_shape

HEADERS = ["category_name", "time_required", "req_mins_per_week", "time_spent_per_week", "total_weeks", "daily_sum"]
FILE_DIR = "PythonPomodoro/text_files/"
CUR_PATH = os.path.dirname(__file__)

on_use_categories = []


class Category:

    def __init__(self,
                 category_name=None,
                 time_required=None,
                 req_mins_per_week=None,
                 time_spent_per_week=None,
                 total_weeks=1,
                 daily_sum=None):

        self.category_name = category_name
        self.time_required = time_required
        self.req_mins_per_week = req_mins_per_week  # required minutes to fill for a week
        self.time_spent_per_week = time_spent_per_week  # time_spent will be filled by the function called pomodoro
        self.total_weeks = total_weeks
        self.daily_sum = daily_sum

    @staticmethod
    def init_csv_file(file_name):
        """
        Creates a csv file with regarding headers in a predefined folder
        """
        file_path = "".join(FILE_DIR + file_name)
        new_path = os.path.relpath(file_path, CUR_PATH)

        file_exists = os.path.isfile(new_path)

        with open(new_path, 'a') as f:
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=HEADERS)

            if not file_exists:
                print("creating a file", new_path)
                writer.writeheader()

    @staticmethod
    def read_categories(file_name):
        """
        read stored Categories and its features  from a given CSV file
        """
        file_path = "".join(FILE_DIR + file_name)
        new_path = os.path.relpath(file_path, CUR_PATH)

        with open(new_path, "r") as csv_file:
            lines = csv.reader(csv_file)
            for i, line in enumerate(lines):
                if i == 0:
                    pass
                else:
                    on_use_categories.append(
                        Category(
                            category_name=line[0],
                            time_required=line[1],
                            req_mins_per_week=line[2],
                            time_spent_per_week=line[3],
                            total_weeks=line[4],
                            daily_sum=line[5]
                        ))

        return on_use_categories, lines

    @staticmethod
    def check_categories(name_to_check, line_number=None):
        """
        Checks the new category name with the existing ones while reading from a file
        :returns True or False
        """

        if len(on_use_categories) == 0:  # meaning there is no category added before
            print("[check_categories] The category name is successful")
            return True

        else:
            for index in range(len(on_use_categories)):
                print("name_to_check", name_to_check,
                      "category_name", on_use_categories[index].category_name,
                      "index", index)

                if name_to_check == on_use_categories[index].category_name and line_number - index != 0:
                    # meaning the last entered one is an exception
                    print("this category already exists, please choose another one")

                    return False

            print("You entered a new category")
            return True

    def build_category(self):
        """
        Builds categories and their values via inputs from the user
        :return: list of category objects
        """

        name = str(input("Enter the name of the category: "))

        if Category.check_categories(name_to_check=name) is True:
            print("\n[build_the_category] Enter the details of the category below")

            weeks_required = int(
                input("\nWhat is the total required weeks to handle it, if you don't know, type it as 1...  "))

            time_required = str(input("\nWhat is the total required hours to handle it in a week (hh:mm)... " +
                                      "\nif you don't know in total press 2" +
                                      "\nif you know it, press 3 "))

            if time_required == "2":  # meaning, the category member has no total hours
                time_required = str(input("\nWhat is the required time to handle it for a week (hh:mm)...? "))
                _, h_req, m_req = check_shape(time_required)
                req_minutes = (int(h_req) * 60) + int(m_req)

                on_use_categories.append(
                    Category(category_name=name, time_required=time_required, req_mins_per_week=req_minutes,
                             total_weeks=weeks_required))

            elif time_required == "3":  # meaning, the category member has total hours
                time_required = str(input("\nWhat is the required time to handle it for a week (hh:mm)...? "))
                _, h_req, m_req = check_shape(time_required)
                req_minutes = (int(h_req) * 60) + int(m_req)

                total_minutes_per_week = float(req_minutes / weeks_required)

                req_minutes_per_week = total_minutes_per_week

                on_use_categories.append(
                    Category(category_name=name, time_required=time_required, req_mins_per_week=req_minutes_per_week,
                             total_weeks=weeks_required))

            else:
                print("Some error occurred at Building the Category !!! ")
                print("Please check your entries !!! ")
                return False

        return on_use_categories

    def choose_category(self):
        """
        takes the current Category Class and prints them
        :return: the chosen category
        """

        print("\nChoose the topic you want to study!!")
        print("\nThe categories...")

        for id, cat in enumerate(on_use_categories):
            print(id, cat.category_name)

        _id = int(input("\nput the number of category "))
        print(on_use_categories[_id].category_name, "is selected! ")

        return on_use_categories[_id]

    def store_categories(self):
        """
		Takes the category and stores it into a file and recovers it back when the program starts
		"""
        print("\n entering to the store_categories\n")

        self.init_csv_file(file_name="categories.csv")

        file_path = "".join(FILE_DIR + "categories.csv")
        new_path = os.path.relpath(file_path, CUR_PATH)

        with open(new_path, 'a') as f:

            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=HEADERS)
            len_cat_gen = len(on_use_categories)

            if self.check_categories(on_use_categories[len_cat_gen - 1].category_name,
                                     line_number=len_cat_gen - 1) is True:
                writer.writerow(
                    {HEADERS[0]: on_use_categories[len_cat_gen - 1].category_name,
                     HEADERS[1]: on_use_categories[len_cat_gen - 1].time_required,
                     HEADERS[2]: on_use_categories[len_cat_gen - 1].req_mins_per_week,
                     HEADERS[3]: on_use_categories[len_cat_gen - 1].time_spent_per_week,
                     HEADERS[4]: on_use_categories[len_cat_gen - 1].total_weeks,
                     HEADERS[5]: on_use_categories[len_cat_gen - 1].daily_sum
                     })
                print("\nStoring is successful !!! \n")
            else:
                print("Unexpected error occurred!!\n")
                _name_to_check = str(input("Please enter another name for the category "))
                Category.check_categories(_name_to_check)
        return True

    def read_from_records(self, time_stamp=None):
        """
        Reads the recorded time values and sums them altogether and add it to the "time_spent_per_week" and subtracts
        them from "req_minutes_per_week"
        :parameter:
            time_stamp: time interval of the record, ie, day or week
        """
        # TODO: under development, complete here

        print('timeStamp', time_stamp)
        total = 0
        temp = [[0 for x in range(1)] for y in range(1)]  # Record the values to sum up
        print('temp:', temp)
        pomo_data = pd.read_csv("pomodoro_records.csv")

        unique, indexes, counts = np.unique(pomo_data.work_type, return_counts=True, return_index=True)

        for i, uniq in enumerate(unique):

            if time_stamp is not None:

                for j in range(1, pomo_data.shape[0]):

                    if uniq == pomo_data.work_type[j] and time_stamp == pomo_data.date[j]:
                        total += pomo_data.iloc[j, 2]

                if total != 0:
                    # TODO: add the value to the related column of the related category
                    print('recorded to a file')

                temp.append([uniq, total])
                total = 0

            else:
                for j in range(1, pomo_data.shape[0]):
                    if uniq == pomo_data.work_type[j]:
                        total += pomo_data.iloc[j, 2]

                temp.append([uniq, total])
                total = 0

        print("temp:\n", temp)

        return temp

    def calculate_by_time(self, time_info=None):
        """
		This function only checks for the time and when it is called, it calls the read_from_records(self)
		function sum all the records based on the time interval. If that day/week already calculated it doesn't
		calculate again. it stores the daily sums to update "time_spentPerWeek" weekly.
		And makes the daily sum zero again.

		:returns matrix of consists of tuples of work_type and total time
		"""
        # TODO: complete here
        # TODO: get the day information
        # TODO: get the week information
        # TODO: first run by day to fill the daily_sum, if a week changes then run by week_flag=True

        # Get the current date and parse it by seperating from '-'
        current_date = datetime.date.today()
        current_date_s = str(current_date).split('-')

        # get the numbers of each element, as string
        cur_year_num = current_date_s[0]
        cur_month_num = current_date_s[1]
        cur_day_num = current_date_s[2]
        cur_week_num = datetime.date(int(current_date_s[0]),
                                     int(current_date_s[1]),
                                     int(current_date_s[2])).isocalendar()[1]

        while True:
            next_day_num = cur_day_num

            if cur_day_num == next_day_num:

                self.read_from_records(time_stamp=str(current_date), week_flag=False)
                next_day_num = str(datetime.date.today()).split('-')
                next_day_num = next_day_num[2]

            else:
                raise "Unexpected error at calculate_by_time() "

    @staticmethod
    def write_to_file(date, work, time_spent):
        """
        Save all these pomodoro records to a file
        """

        file_path = "".join(FILE_DIR + "pomodoro_records.csv")
        new_path = os.path.relpath(file_path, CUR_PATH)

        file_exists = os.path.isfile(new_path)

        with open(new_path, 'a') as f:
            headers = ["date", "work_type", "time_spent_in_sec"]
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames=headers)

            if not file_exists:
                writer.writeheader()

            writer.writerow({'date': date, 'work_type': str(work), 'time_spent_in_sec': str(time_spent)})
