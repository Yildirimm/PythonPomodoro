import time

class Counter:

	@staticmethod
	def countdown(t):
		while t:
			min_in, sec_in = divmod(t, 60)
			timer = '{:02d}:{:02d}'.format(min_in, sec_in)
			print(timer, end="\r")  # carriage return
			time.sleep(1)
			t -= 1
