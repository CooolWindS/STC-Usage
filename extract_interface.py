# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:00:06 2021

@author: CoolWind
"""

import os
import sys
import global_var as gvar
from extract import extract
import minor_lib as mlib
from tqdm import tqdm

def extract_interface():
	
	# ex. files/stego/
	stego_image_dir = gvar.directory['stego']
	mlib.check_dir(stego_image_dir)
	
	stego_image_folders = os.listdir(stego_image_dir)
	
	# ex. /home/.../pySTC/files/message_embed/R
	message_dir = gvar.directory['message_extract']
	message_dir_channel ={}
	for i in stego_image_folders:

		message_dir_channel[i] = os.path.join(message_dir, i)
		mlib.check_dir(message_dir_channel[i])
	
	print('In ' + str(stego_image_dir))
	print('Channel list: ' + str(stego_image_folders))
	print('Extract start...\n')
	
	for i in range(len(stego_image_folders)):
		
		# ex. files/stego/R
		stego_image_folders[i] = os.path.join(stego_image_dir, stego_image_folders[i])
		
		stego_image_filelist = os.listdir(stego_image_folders[i])
		stego_image_filelist.sort()
		
		data_size = len(stego_image_filelist)
		print(str(data_size) + " images to extract in " + str(stego_image_folders[i]))
		print("Start extracting...")
		
		for j in tqdm(range(int(data_size)), file = sys.stdout):
			
			# ex. files/stego/R\01-source-00002_stego_R.bmp
			stego_image = os.path.join(stego_image_folders[i], stego_image_filelist[j])
			
			# ex. 01-source-00002_stego_R
			stego_image_name = os.path.splitext(stego_image_filelist[j])[0]
			
			channel = stego_image_name.split('_')[-1]
			
			output_message_file = stego_image_name + '.txt'
			message_file = os.path.join(message_dir_channel[channel], output_message_file)
			#print(message_file)
			
			extract(stego_image, message_file, channel)
		print('Done.\n')
			
			
			
	
	

if __name__ == "__main__":
	extract_interface()