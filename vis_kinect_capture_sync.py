import csv


class Capture(object):
	def __init__(self, csv_row):
		self.device_idx   = csv_row[0]
		self.device_sn    = csv_row[1]
		self.capture_time = int(csv_row[2])
		self.is_master    = csv_row[3]

captures = []

with open('data/mock_kinect_server_debug_file.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        captures.append(Capture(row))

earliest_capture = 9999999999999999999999999999
latest_capture   = 0

for c in captures:
	earliest_capture = min(earliest_capture, c.capture_time)
	latest_capture = max(latest_capture, c.capture_time)


print('earliest capture ' + str(earliest_capture))
print('latest capture ' + str(latest_capture))



