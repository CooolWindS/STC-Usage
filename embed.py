#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 16:14:36 2021

@author: coolwind
"""

import sys
import os
import platform
import struct
import hashlib
import cv2
import numpy as np
import string
import random
import warnings
from scipy import signal
from ctypes import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import ctypes
import ctypes.util
import global_var as gvar
import minor_lib as mlib
from PIL import Image
from multiprocessing import  Process



# {{{ encrypt()
def encrypt(plain_text, password):

	salt = get_random_bytes(AES.block_size)

	# use the Scrypt KDF to get a private key from the password
	private_key = hashlib.scrypt(
		password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

	cipher = AES.new(private_key, AES.MODE_CBC)
	cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))
	enc = salt+cipher.iv+cipher_text

	return enc
# }}}

def prepare_message(message_file, msg_len, error_code):
	
	msg_bits = int(msg_len * gvar.payload * 0.99 / 8)

	if error_code == 0:

		array=[]
		content_ver=struct.pack("B", 1) # version 1
		
		data=''.join(random.choices(string.ascii_letters, k = msg_bits))
		
		content_data = data.encode('utf-8')
		content_len=struct.pack("!I", len(content_data))
		content=content_ver+content_len+content_data
		
		# encrypt
		enc = encrypt(content, gvar.password)
		
		for b in enc:
			for i in range(8):
				array.append((b >> i) & 1)
		
		f = open(message_file, 'w', encoding="utf-8")
		f.write(data)
		f.close()

	elif error_code == 1:
		array=[]
		
		for i in range(msg_bits * 8):
				array.append(1)

		f = open(message_file, 'w', encoding="utf-8")
		f.write(str(array))
		f.close()

	elif error_code == 2:
		array=[]
		
		for i in range(msg_bits * 8):
				array.append(0)

		f = open(message_file, 'w', encoding="utf-8")
		f.write(str(array))
		f.close()


	return array


def HILL(I):
	H = np.array(
	   [[-1,  2, -1],
		[ 2, -4,  2],
		[-1,  2, -1]])
	L1 = np.ones((3, 3)).astype('float32')/(3**2)
	L2 = np.ones((15, 15)).astype('float32')/(15**2)
	
	# Mod imageio.imread to cv2.imread ????????????
	#I = imageio.imread(input_image)
	
	# Maybe need split RGB channel instead of convert to grayscale
	#I = cv2.imread(input_image,0)
	
	costs = signal.convolve2d(I, H, mode='same')  
	costs = abs(costs)
	costs = signal.convolve2d(costs, L1, mode='same')  
	costs = 1/costs
	costs = signal.convolve2d(costs, L2, mode='same')  
	costs[costs == np.inf] = 1
	
	return costs

# Cover Synthesis port may be here (1/2)
def embed_stc(cost_matrix, cover_image, msg_bits):

	# Lib load
	me = os.path.abspath(os.path.dirname(__file__))
	if platform.system() == 'Windows':
		lib = cdll.LoadLibrary(os.path.join(me, "lib", "stc.dll"))
	elif platform.system() == 'Linux':
		lib = cdll.LoadLibrary(os.path.join(me, "lib", "stc.so"))
	else:
		print('Unsupported system: ' + str(platform.system()))
		sys.exit()


	width, height = cover_image.size

	I = cover_image.load()
	cover = (c_int*(width*height))()
	idx=0
	for j in range(height):
		for i in range(width):
			cover[idx] = I[i, j]
			idx += 1


	# Prepare costs
	INF = 2**31-1
	costs = (c_float*(width*height*3))()
	idx=0
	for j in range(height):
		for i in range(width):
			if cover[idx]==0:
				costs[3*idx+0] = INF
				costs[3*idx+1] = 0
				costs[3*idx+2] = cost_matrix[i, j]
			elif cover[idx]==255:
				costs[3*idx+0] = cost_matrix[i, j]
				costs[3*idx+1] = 0 
				costs[3*idx+2] = INF
			else:
				costs[3*idx+0] = cost_matrix[i, j]
				costs[3*idx+1] = 0
				costs[3*idx+2] = cost_matrix[i, j]
			idx += 1


	m = int(width*height*gvar.payload)
	message = (c_ubyte*m)()
	for i in range(m):
		if i<len(msg_bits):
			message[i] = msg_bits[i]
		else:
			message[i] = 0

	# Hide message
	stego = (c_int*(width*height))()
	a = lib.stc_hide(width*height, cover, costs, m, message, stego)

    # Save output message
	idx=0
	for j in range(height):
		for i in range(width):
			cover_image.putpixel((i, j), stego[idx])
			idx += 1


	return cover_image


# Cover Synthesis port may be here (2/2)
def embed(cover_image_path, stego_image_path, channel, message_file, error_code):

	#####
	warnings.filterwarnings('ignore')
	#####

	# img for embed
	image_split = mlib.read_img(cover_image_path)
	
	##
	width, height = image_split["R"].size
	
	## msg generate
	msg_bits = prepare_message(message_file, width*height, error_code)
	
	#
	if channel == 'R' or channel == 'RGB':
		cost_matrix = HILL(image_split["R"])
		stego_image_R = embed_stc(cost_matrix, image_split["R"], msg_bits)
		out = Image.merge("RGB", (stego_image_R, image_split["G"], image_split["B"]))
	if channel == 'G' or channel == 'RGB':
		cost_matrix = HILL(image_split["G"])
		stego_image_G = embed_stc(cost_matrix, image_split["G"], msg_bits)
		out = Image.merge("RGB", (image_split["R"], stego_image_G, image_split["B"]))
	if channel == 'B' or channel == 'RGB':
		cost_matrix = HILL(image_split["B"])
		stego_image_B = embed_stc(cost_matrix, image_split["B"], msg_bits)
		out = Image.merge("RGB", (image_split["R"], image_split["G"], stego_image_B))
		
	## Mode handle
	if channel != 'R' and channel != 'G' and channel != 'B' and channel != 'RGB':
		print("\n\nPicture Mode not suuported.")
		sys.exit()
	
	if channel == 'RGB':
		out = Image.merge("RGB", (stego_image_R, stego_image_G, stego_image_B))
		
	# Stego img save
	out.save(stego_image_path)
	
	## Log Record
	log = open('files/log_embed.log', 'a+')
	log.write('Img: ' + str(cover_image_path) + '\n')
	log.write('Embed in ' + str(channel) + ' channel.\n')
	log.write('Img: ' + str(width) + ' x ' + str(height) + ' \n')
	log.write('Message bits: ' + str(len(msg_bits)) + ' (per channel)\n')
	if(error_code == 1):
		log.write('Message bits: ' + 'ALL 1 ' + '\n')
	elif(error_code == 2):
		log.write('Message bits: ' + 'ALL 0 ' + '\n')
	log.write('msg_bit / MAX_bits: ' + str(len(msg_bits)) + ' / ' + str(width*height) + ' : ' + str(format(len(msg_bits) / (width*height), '.3f')) + ' bpp (per channel)\n')
	log.write('Stego: ' + str(stego_image_path) + '\n\n')
	log.close()
	##


if __name__ == "__main__":

	cover_image_path = 'files/cover/01-source-00110.bmp'
	stego_image_path ='files/stego_R.bmp'
	message_file = 'files/message.txt'
	channel = 'R'
	error_code = 0
	
	p = Process(target=embed, args=(cover_image_path, stego_image_path, channel, message_file, error_code))
	p.start()
	p.join()
	
	if not(os.path.isfile(stego_image_path)):
		print('Img embed failed in ' + str(channel) + ', try to embed again 1st.')
		
		error_code = error_code + 1
		p = Process(target=embed, args=(cover_image_path, stego_image_path, channel, message_file, error_code))
		p.start()
		p.join()

		if (os.path.isfile(stego_image_path)):
			print('Img embed succeed in ' + str(channel) + '\n\n')

	if not(os.path.isfile(stego_image_path)):
		print('Img embed failed in ' + str(channel) + ', try to embed again 2nd.')

		error_code = error_code + 1
		p = Process(target=embed, args=(cover_image_path, stego_image_path, channel, message_file, error_code))
		p.start()
		p.join()

		if (os.path.isfile(stego_image_path)):
			print('Img embed succeed in ' + str(channel) + '\n\n')

	if not(os.path.isfile(stego_image_path)):
		print('Img embed failed in ' + str(channel) + ', skip.\n\n')
		print("If there is no output or the program crashes, it means that the embedding failed.")
		print("(Maybe the crash point will be lib/lib_c++/stc_ml_c.cpp line 317.)")

		if (os.path.isfile(message_file)):
			os.remove(message_file)