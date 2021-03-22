#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 14:56:58 2021

@author: coolwind
"""

import os
import sys
import global_var as gvar
import minor_lib as mlib
from tqdm import tqdm
from embed import embed
from multiprocessing import  Process

def embed_interface():

	# ex. /home/.../pySTC/files/cover/
	cover_image_dir = gvar.directory['cover']
	mlib.check_dir(cover_image_dir)


	mode = gvar.mode
	channel_list = mlib.channel_choose(int(mode))

	# ex. /home/.../pySTC/files/stego/
	stego_image_dir = gvar.directory['stego']

	# ex. /home/.../pySTC/files/stego/R
	stego_image_dir_channel = {}
	for i in channel_list:

		stego_image_dir_channel[i] = os.path.join(stego_image_dir, i)
		mlib.check_dir(stego_image_dir_channel[i])

	# ex. /home/.../pySTC/files/message_embed/R
	message_dir = gvar.directory['message_embed']
	message_dir_channel ={}
	for i in channel_list:

		message_dir_channel[i] = os.path.join(message_dir, i)
		mlib.check_dir(message_dir_channel[i])

	# All cover image in cover_image_dir
	# ex. ['color_001.bmp', 'color_002.bmp', ...]
	cover_image_filelist = os.listdir(cover_image_dir)
	cover_image_filelist.sort()

	data_size = len(cover_image_filelist)
	#data_size = 20

	# prepare message for embed
	#mlib.prepare_message_embed(cover_image_filelist, message_dir_channel)

	print('In ' + str(cover_image_dir))
	print(str(data_size) + ' images need embeded.')
	print('Channel list: ' + str(channel_list))
	print('Embed start...\n')


	for i in tqdm(range(data_size),  file=sys.stdout, position=0, leave=True):

		# Cover image
		# ex. color_001.bmp
		cover_image = cover_image_filelist[i]

		# Cover image path
		# ex. /home/.../pySTC/files/cover/color_001.bmp
		cover_image_path = os.path.join(cover_image_dir, cover_image)

		# Cover image name and datatype
		# color_001 and .bmp
		cover_image_name = os.path.splitext(cover_image)[0]
		#cover_image_datatype = os.path.splitext(cover_image)[1]

		for channel in channel_list:

			error_code = 0

			s = "_stego_" + channel + "."
			stego_image_name = (cover_image.replace(".", s))
			stego_image_path = os.path.join(stego_image_dir_channel[channel], stego_image_name)

			input_message_file = cover_image_name + '_' + str(channel) + '.txt'
			message_file = os.path.join(message_dir_channel[channel], input_message_file)

			if (os.path.isfile(stego_image_path)):
				tqdm.write('Img: ' + str(cover_image_name) + ' embed in ' + str(channel) + ' already exist, please check ur file is new or not.\n\n')
				sys.exit()

			p = Process(target=embed, args=(cover_image_path, stego_image_path, channel, message_file, error_code))
			p.start()
			p.join()

			if not(os.path.isfile(stego_image_path)):
				tqdm.write('Img: ' + str(cover_image_name) + ' embed failed in ' + str(channel) + ', try to embed again 1st.')
				
				## Log Record
				log_try = open('files/log_embed_try.log', 'a+')
				log_try.write('Img: ' + str(cover_image_name) + ' embed failed in ' + str(channel) + ', try to embed again 1st.\n')
				log_try.close()

				error_code = error_code + 1
				p = Process(target=embed, args=(cover_image_path, stego_image_path, channel, message_file, error_code))
				p.start()
				p.join()

				if (os.path.isfile(stego_image_path)):
					tqdm.write('Img: ' + str(cover_image_name) + ' embed succeed in ' + str(channel) + '\n\n')
					## Log Record
					log_try = open('files/log_embed_try.log', 'a+')
					log_try.write('Img: ' + str(cover_image_name) + ' embed succeed in ' + str(channel) + '\n\n')
					log_try.close()

			if not(os.path.isfile(stego_image_path)):
				tqdm.write('Img: ' + str(cover_image_name) + ' embed failed in ' + str(channel) + ', try to embed again 2nd.')
				
				## Log Record
				log_try = open('files/log_embed_try.log', 'a+')
				log_try.write('Img: ' + str(cover_image_name) + ' embed failed in ' + str(channel) + ', try to embed again 2nd.\n')
				log_try.close()

				error_code = error_code + 1
				p = Process(target=embed, args=(cover_image_path, stego_image_path, channel, message_file, error_code))
				p.start()
				p.join()

				if (os.path.isfile(stego_image_path)):
					tqdm.write('Img: ' + str(cover_image_name) + ' embed succeed in ' + str(channel) + '\n\n')
					## Log Record
					log_try = open('files/log_embed_try.log', 'a+')
					log_try.write('Img: ' + str(cover_image_name) + ' embed succeed in ' + str(channel) + '\n\n')
					log_try.close()

			if not(os.path.isfile(stego_image_path)):
				tqdm.write('Img: ' + str(cover_image_name) + ' embed failed in ' + str(channel) + ', skip.\n\n')
				
				## Log Record
				log = open('files/log_embed_failedy.log', 'a+')
				log.write(cover_image_name + ' in ' + str(channel) + '\n')
				log.close()
				## Log Record
				log_try = open('files/log_embed_try.log', 'a+')
				log_try.write('Img: ' + str(cover_image_name) + ' embed failed in ' + str(channel) + ', skip.\n\n')
				log_try.close()

				if (os.path.isfile(message_file)):
					os.remove(message_file)
					
	print('Done.\n\n')
	print("If there are no output in some cases, it means that the embedding failed.")
	print("(Maybe the crash point will be lib/lib_c++/stc_ml_c.cpp line 317.)\n\n")




if __name__ == "__main__":
	embed_interface()