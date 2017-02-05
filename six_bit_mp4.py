# -*- coding: utf-8 -*-

import os
import re
import sys
import shutil
import string
import subprocess

# FAQ

# how to use it:
#   echo "Pick a lane and drive like hell." | python3 six_bit_mp4.py
#   a file called hexbit.mp4 should appear in the directory when it's done

# what it does:
#   takes a string from the command line and converts it to video and audio
#   the video is a series of varying patterns but the audio tends towards headache inducing frequencies
#	there's a 1000Hz low pass filter but if you want high tones that your dog will hate you can comment it out

# how:
#   converts characters from strings into 6 bits: 'a' to '100100' and squishes them together
#   then it puts the big bunch of bits together repeatedly until there's enough to make a 360x360 jpg
#   the first iteration will contain only the first letter of the string: PPPPPPPPP..
#   the second iteration: PiPiPiPiPi...
#   and so on until all the characters are exhausted

# which characters does it accept?
#   [0-9], [A-Z], [a-z], [_], [.]
#   '0' = '000000', '.' = '111111'

# the image on my media player doesn't change but the audio works:
#   yeah this happened to me with VLC. I think the 2 fps rate is unusual and scrambles the media player's brain.

# what if I want a different frame-per-second rate?
#   it's possible but you'll have to figure out how make the audio accept the increased or decreased video information rate

# will it work on Windows?
#   probably but you'll have to install ffmpeg which is free and available here: http://www.ffmpeg.org/download.html#build-windows
#   then alter the subprocess.call command:
#     - change ffmpeg to [ffmpeg directory]\ffmpeg.exe
#     - delete ', shell=True' from the end of the subprocess.call command

# can I use this code for my own projects?
#   yeah sure totally go for it and you don't even have to credit me. It's a public domain license.
#   If you build a twitter bot please let me know so I can make videos.

# why is this Python 3 only?
#   it uses int.to_bytes which isn't available in Python 2. Sorry!
if sys.version_info[0] != 3 or sys.version_info[1] < 2:
	print('This version works with Python version 3.2 and above but not Python 2, sorry!')
	sys.exit()


images_dir = 'images/'
raw_file   = 'data.raw'
out_mp4    = 'hexbit.mp4'

if os.path.exists(images_dir):
	shutil.rmtree(images_dir)

os.mkdir(images_dir)

if os.path.exists(raw_file):
	os.remove(raw_file)


# Functions

def dict_prep():

	hexbit_dict = {}

	# [0-9], [A-Z], [a-z], [_], [.]
	char_string = string.digits + string.ascii_uppercase + string.ascii_lowercase + '_' + '.'

	# to make each video unique uncomment commands below
	#import random
	#char_string = ''.join(random.sample(char_string,len(char_string)))

	# each character will equal a 6 bit string six_dict['0']: '000000'
	i = 0
	for c in char_string:
		hexbit_dict[c] = '{:06b}'.format(int(bin(i),2))
		i += 1

	return(hexbit_dict)


def string_prep(total_loops):

	# multiplies by 8 to get total bits, divide by 6 for hexbits and then +1 for ceil
	hexbit_len = int( ((total_loops * 8) / 6) + 1)

	# read in lines from pipe. buffer limited to length of hexbit_len for safety from buffer overflow bugs
	s = ""
	for line in sys.stdin.readline(hexbit_len):
		s += line

	if len(s) < 1:
		print("Error: string must be at least 1 character long.")
		sys.exit()

	# everything that isn't alphanumeric becomes '_'
	s = re.sub('[^0-9a-zA-Z.]+', '_', s)

	# get rid of this loop and change to return(s) if you want to vary the length of videos
	# according to the length of input text

	ns = ''
	while len(ns) < hexbit_len:
		ns += s

	return(ns)


def build_raw_string(s):

	# converts 'j' to '101101'
	bit_string = ''
	for c in s:
		bit_string += six_dict[c]

	# repeats the bit_string until it's long enough for a full frame
	build_bit = ''
	while len(build_bit) < image_size_bits: build_bit += bit_string

	# slices off the extra
	finished_bit = build_bit[:image_size_bits]

	return(finished_bit)


def bitstring_to_bytes(s):

	# '10001000' to b'\x88\x88'
	return int(s, 2).to_bytes(len(s) // 8, byteorder='big') # big, little, sys.byteorder


def make_video(raw_file):

	# uses the bytes to create both video and audio and combines them into an mp4
	subprocess.call('ffmpeg -loglevel error -y ' +
					' -f rawvideo -pix_fmt rgb24 -r 2 -s 360x360 -i ' + raw_file +
					# because audio usually requires less information than video
					# these bit sizes are abnormally high to use all bytes in the raw_file
					' -f f64be -acodec pcm_s64be -ac 2 -ar 48600 -i ' + raw_file +
					# has a tendency to create annoying frequencies so we lowpass filter them out
					' -af "lowpass=f=1000" ' +
					# settings for twitter. if it rejects a video try dropping -b:v to 256k
					' -vcodec libx264 -acodec aac -ar 44100 -b:a 64k -b:v 512k -pix_fmt yuv420p ' +
					out_mp4, shell=True)


# Variables
jump_gap = 1 # in case you want to iterate more than 1 char per image
# one loop per character in a tweet
total_loops = 140
# jpg most commonly uses rgb24 which is 24 bits per pixel or 3 bytes
bytes_per_pixel = 3
pixels = int(360 * 360)
image_size_bytes  = int(pixels * bytes_per_pixel)
image_size_bits   = int(image_size_bytes * 8)


# Main
six_dict = dict_prep()
s = string_prep(total_loops)
i = itt = jump_gap
old_s = ''
while i <= total_loops * itt:

	new_s = s[:i]
	# checks if the previous frame was identical, quits if it is
	if old_s == new_s: break
	old_s = new_s

	# repeats the string until it's long enough for a full frame
	big_bit = build_raw_string(new_s)
	# '10001000' to b'\x88'
	big_byte = bitstring_to_bytes(big_bit)

	# appends bytes to a file
	with open(raw_file,'ab') as raw:
		raw.write(big_byte)

	i += itt

# And done
make_video(raw_file)

# clean up
shutil.rmtree(images_dir)
os.remove(raw_file)
