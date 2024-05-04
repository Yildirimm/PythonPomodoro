from datetime import datetime

from category import Category
from utils import check_shape, BeepSound, Counter
import schedule


cat_general = []
cat_flag = 0


if __name__ == '__main__':

    the_day = datetime.today().strftime('%Y-%m-%d')

    c1 = Category()

    c1.init_csv_file(file_name="categories.csv")
    _category, the_last_one = c1.read_categories(file_name="categories.csv")

    if len(_category) == 0:
        print("There is no category right now! Redirecting to add category...\n")
        c1.build_category()
        c1.store_categories()

    else:
        a = input("There are categories on table but if you want to add even more [y/n]?: ")

        if a == "y":
            c1.build_category()
            c1.store_categories()

    chosen_one = c1.choose_category()

    loop_number = 0
    pomodoro_time = 0

    while True:
        time_to_run = str(input("Enter the time as MM:SS, "))
        _, mins, secs = check_shape(time_to_run)

        counter_time = (int(mins) * 60) + int(secs)
        Counter.countdown(int(counter_time))
        BeepSound.beep()

        loop_number += 1
        pomodoro_time += counter_time
        breaker = str(input("\nDo you want to break the cycle [y/n]?: "))
        if breaker == "y":
            count_t = pomodoro_time
            break

    chosen_one.time_spent = round(count_t / 60, 3)

    Category.write_to_file(the_day, chosen_one.category_name, count_t)

# schedule.every(2).seconds.do(c1.calculate_by_time())

# TODO: write the chosen ones into pomodoro, and make them to be summed and written into categories.

# TODO: add the hour stamp to the pomodoro_records.csv also
# TODO: add a function to add the studied stuff's hour on the records and it should ask at the beginning of the program

# TODO: add timestamps to pomodoro records, as start-finish then you can get the time-interval from these
# TODO: add a function to see if computer is on or not

# TODO: add functions to categories to draw graphs
