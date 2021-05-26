import csv
import sys
import cv2 as cv
import numpy as np


# classes ---------------------------------------------      

class Capture(object):
	def __init__(self, csv_row):
		self.frame        = int(csv_row[0])
		self.device_idx   = int(csv_row[1])
		self.device_sn    = csv_row[2]
		self.capture_time = int(csv_row[3])
		self.is_master    = int(csv_row[4])
		# self.group        = int(csv_row[4])

# constants ---------------------------------------------      

debug_filename = sys.argv[1]

WIDTH=1920*6
HEIGHT=200*2

circle_r=5
circle_col=(0,0,255)

rect_cols=[(0,0,255), (0,255,0), (255,125,125)]
rect_half_size=5

# map_device_idx_to_row=[1,2,0,3] # for 4 cameras 
map_device_idx_to_row=[0,1,4,2,5,6,3,7] # for 4 cameras 

captures_to_use=3000

# globals ---------------------------------------------      


captures = []
earliest_capture = 9999999999999999999999999999
latest_capture   = 0
capture_range    = 0

img = np.zeros((HEIGHT,WIDTH,3), np.uint8)

# logic  ---------------------------------------------      




print('loading debug file ' + debug_filename)

with open(debug_filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        captures.append(Capture(row))

print('Found ' + str(len(captures)) + ' captures')
print('ONLY USING THE LAST ' + str(captures_to_use) + ' CAPTURES!!!')

captures=captures[len(captures)-captures_to_use:]

for c in captures:
	earliest_capture = min(earliest_capture, c.capture_time)
	latest_capture = max(latest_capture, c.capture_time)

print('earliest capture ' + str(earliest_capture))
print('latest capture ' + str(latest_capture))

#create margin at ends of timeline
earliest_capture -= 100000
latest_capture   += 100000

capture_range = latest_capture - earliest_capture

last_centre = (0,0)
last_master_centre = (0,0)

for c_idx in range(len(captures)):

	c = captures[c_idx]

	normed_capture_time = (c.capture_time - earliest_capture) / capture_range
	
	#draw capture as circle
	# cv.circle(img,(int(WIDTH*normed_capture_time),100), circle_r, circle_col, -1)
	
	rect_centre_x = int(WIDTH*normed_capture_time)
	rect_centre_y = 20 + map_device_idx_to_row[c.device_idx] * 20;

	# link rectangle to previous capture if they belong to the same frame
	if (c_idx > 0):
		if c.frame == captures[c_idx-1].frame:
			cv.line(img,last_centre,(rect_centre_x,rect_centre_y),(255,255,255),1)


	if c.is_master:
		print('master_time: ' + str(c.capture_time))

		#link masters with line to check group order is not corrupted
		cv.line(img,last_master_centre,(rect_centre_x,rect_centre_y),(255,255,255),1)
		last_master_centre = (rect_centre_x,rect_centre_y)


	#draw capture as rect
	cv.rectangle(img,(rect_centre_x-rect_half_size, rect_centre_y-rect_half_size),(rect_centre_x+rect_half_size,rect_centre_y+rect_half_size),rect_cols[c.frame%3],-1)

	last_centre = (rect_centre_x,rect_centre_y)






cv.imwrite("kinect_capture_vis.png", img);