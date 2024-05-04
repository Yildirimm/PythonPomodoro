global split_point, min, sec


def check_shape(input_time):

	for i, c in enumerate(input_time):
		if c == (":" or ","):
			min = input_time[:i]
			sec = input_time[i + 1:]
			split_point = input_time[i]

			return split_point, min, sec

