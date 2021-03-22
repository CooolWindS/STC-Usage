#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:57:11 2021

@author: coolwind
"""

import minor_lib as mlib
import sys
import os
import platform
import struct
import hashlib
import numpy as np
from scipy import signal
from ctypes import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import global_var as gvar
import ctypes
import ctypes.util

def decrypt(cipher_text, password):
	
	salt = cipher_text[:AES.block_size]
	iv = cipher_text[AES.block_size:AES.block_size*2]
	cipher_text = cipher_text[AES.block_size*2:]

	# Fix padding
	mxlen = len(cipher_text)-(len(cipher_text)%AES.block_size)
	cipher_text = cipher_text[:mxlen]

	private_key = hashlib.scrypt(
		password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

	cipher = AES.new(private_key, AES.MODE_CBC, iv=iv)
	decrypted = cipher.decrypt(cipher_text)
	#decrypted = unpad(decrypted, AES.block_size)

	return decrypted
# }}}

# Cover Synthesis port may be here
def extract(stego_image, message_file, channel):
	
	me = os.path.abspath(os.path.dirname(__file__))
	if platform.system() == 'Windows':
		lib = cdll.LoadLibrary(os.path.join(me, "lib", "stc.dll"))
	elif platform.system() == 'Linux':
		lib = cdll.LoadLibrary(os.path.join(me, "lib", "stc.so"))
	else:
		print('Unsupported system: ' + str(platform.system()))
		sys.exit()
	
	image_split = mlib.read_img(stego_image)
	
	if channel == 'RGB':
		img = image_split["R"]
	else:
		img = image_split[channel]
    
	width, height = img.size
	
	I = img.load()
	stego = (c_int*(width*height))()
	idx=0
	for j in range(height):
		for i in range(width):
			stego[idx] = I[i, j]
			idx += 1

	# Extract the message
	n = width*height
	m = int(n * gvar.payload)
	extracted_message = (c_ubyte*m)()
	s = lib.stc_unhide(n, stego, m, extracted_message)

	# Save the message
	enc = bytearray()
	idx=0
	bitidx=0
	bitval=0
	for b in extracted_message:
		if bitidx==8:
			enc.append(bitval)
			bitidx=0
			bitval=0
		bitval |= b<<bitidx
		bitidx+=1
	if bitidx==8:
		enc.append(bitval)

	# decrypt
	cleartext = decrypt(enc, gvar.password)
 
	# Extract the header and the message
	content_ver=struct.unpack_from("B", cleartext, 0)
	content_len=struct.unpack_from("!I", cleartext, 1)
	content=cleartext[5:content_len[0]+5]

	s = content.decode(errors='ignore')
	
	f = open(message_file, 'w', encoding="utf-8")
	f.write(s)
	f.close()
	

if __name__ == "__main__":
	stego_image = 'files/stego_R.bmp'
	message_file = 'files/message_extract.txt'
	channel = 'R'
	
	extract(stego_image, message_file, channel)