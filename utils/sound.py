import os
import platform

if platform.system() == "windows":
	import winsound


class BeepSound:

	@staticmethod
	def beep(duration=1000, freq=440):
		"""
		duration = 1000
		freq = 440
		"""
		os.system(f"beep -f {freq} -l {duration}")

		if platform.system() == "windows":
			winsound.Beep(freq, duration)