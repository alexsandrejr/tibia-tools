import os
import sys
import cv2
import pyautogui
import time
import numpy as np
import pygetwindow as gw



def get_tibia_active(CHAR_NAME):
	'''
	Get Tibia tab
		@params
		null

		@return
		void
	'''
	try:
		tibia = gw.getWindowsWithTitle('Tibia - '+str(CHAR_NAME))[0]
		tibia.activate()
	except IndexError:
		print(' ~~ TIBIA NOT FOUND! ~~')
		sys.exit(0)

def get_latest_image(SS_DIRPATH, valid_extensions=('jpg','jpeg','png')):
	'''
	Get the latest image file in the given directory
		@params
		SS_DIRPATH: Tibia screenshots path folder

		@return
		last added image file
	'''
	# get filepaths of all files and dirs in the given dir
	valid_files = [os.path.join(SS_DIRPATH, filename) for filename in os.listdir(SS_DIRPATH)]
	# filter out directories, no-extension, and wrong extension files
	valid_files = [f for f in valid_files if '.' in f and \
		f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

	if not valid_files:
		raise ValueError("No valid images in %s" % SS_DIRPATH)

	return max(valid_files, key=os.path.getmtime) 


def take_screenshot(SS_HOTKEY):
	'''
	Take screenshot
		@params
		SS_HOTKEY: screenshot hotkey

		@return
		number + 1
	'''
	pyautogui.press(SS_HOTKEY)

def del_screenshot(pic_path):
	'''
	Delete screenshot
		@params
		number: screenshot path

		@return
		void
	'''
	os.remove(pic_path)

def idle(number):
	'''
	Sleep 
		@params
		number: seconds

		@return
		void
	'''
	time.sleep(number)

def increment(number):
	'''
	Increment 1 to a number
		@params
		number: any int

		@return
		number + 1
	'''
	return number+1

def is_visible(template, pic_path, keep_diff=False):
	'''
	Check if the image file is on the screen.
	After check, remove the png file.
		@params
		template: image file to be matched (e.g, .png)
		SS_DIRPATH: Tibia screenshots path folder
		SS_HOTKEY: screenshot hotkey
		keep_diff: if True, save diff file

		@return
		tuple(coordinates found)
	'''
	# Read the snapshot
	img_rgb = cv2.imread(pic_path)
	# Changing: rgb -> grayscale
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	# Looking for the template
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)

	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	threshold = 0.8
	loc = np.where( res >= threshold)

	if keep_diff == True:
		w, h = template.shape[::-1]
		for pt in zip(*loc[::-1]):
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
		print(cv2.rectangle)
		cv2.imwrite('diff.png',img_rgb)

	return loc