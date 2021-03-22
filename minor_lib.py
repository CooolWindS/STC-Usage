#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 14:25:10 2021

@author: coolwind
"""
import os
import sys
from PIL import Image
from tqdm import tqdm
import string
import random
import global_var as gvar

def check_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def read_img(image_path):
	
	image = Image.open(image_path)
	(r, g, b) = image.split()
	image_split = {'R':r, 'G':g, 'B':b}

	return image_split


def channel_choose(mode):
	
	if(mode < 0 or mode > 5):
		print('Error channel code, please check channel code in parameter.')
		sys.exit(0)
	elif(mode > 0 and mode < 5):
		return [gvar.channel[mode]]
	else:
		return gvar.channel[1:]