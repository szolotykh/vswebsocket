import threading

# Thread class with stop method
class VSThread(threading.Thread):
	def __init__(self):
		super(VSThread, self).__init__()
		self._stop = threading.Event()

	def stop(self, timeout=None):
		self._stop.set()
		self.join(timeout)

	def stopped(self):
		return self._stop.isSet()