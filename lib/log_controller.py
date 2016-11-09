import datetime


class LogController(object):
	def __init__(self, configs):
		self.path = configs["log_destination"]

	def log(self, server, group_id, group_name):
		with open(self.path, 'a') as f:
			log_msg = "%s - INFO %s moved to group %s \n" % (datetime.datetime.utcnow(),
															 server["server_label"],
															 group_name)
			f.write(log_msg)

	def log_error(self, e):
		with open(self.path, 'a') as f:
			error_msg = "%s - Error - Error Experienced. %s:%s \n" % (datetime.datetime.utcnow(),
																	  type(e).__name__,
																	  e)
			f.write(error_msg)