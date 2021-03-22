import os
import filecmp
import global_var as gvar
from tqdm import tqdm

def compare():
	
	log = open('files/log_compare_message.log', 'w')
	
	now_dir = os.getcwd()
	
	message_embed_folder = os.path.join(now_dir, gvar.directory['message_embed'])
	message_extract_folder = os.path.join(now_dir, gvar.directory['message_extract'])
	
	message_embed_folderlist = os.listdir(message_embed_folder)
	message_extract_folderlist = os.listdir(message_extract_folder)
	
	message_embed_folderlist.sort()
	message_extract_folderlist.sort()
	
	if(len(message_embed_folderlist) != len(message_extract_folderlist)):
		print('Different folders to compare.')
		print('Please check your folders.')
	
	for j in range(len(message_embed_folderlist)):
		
		message_embed_file = os.path.join(message_embed_folder, message_embed_folderlist[j])
		message_extract_file = os.path.join(message_extract_folder, message_extract_folderlist[j])
		
		message_embed_filelist = os.listdir(message_embed_file)
		message_extract_filelist = os.listdir(message_extract_file)
		
		message_embed_filelist.sort()
		message_extract_filelist.sort()
		
		if(len(message_embed_filelist) != len(message_extract_filelist)):
			print('Different files to compare in')
			print(message_embed_file)
			print(message_extract_file)
			print('Please check your files.')
		
		same = 0
		different = 0
		for i in  tqdm(range(len(message_embed_filelist)), position=0, leave=True):

			f1 = os.path.join(message_embed_file, message_embed_filelist[i])
			f2 = os.path.join(message_extract_file, message_extract_filelist[i])

			log.write(f1 + '\n')
			log.write(f2 + '\n')

			if(filecmp.cmp(f1, f2, shallow=False)):	
				log.write('Same.\n\n\n')
				same = same + 1
			else:
				log.write('Different.\n\n\n')
				different = different + 1
		
		print('\nIn folder', flush=True)
		print(message_embed_file, flush=True)
		print(message_extract_file, flush=True)
		print('Same: ', same, flush=True)
		print('Different: ', different, flush=True)
		print('\n\n', flush=True)
		
	log.close()

if __name__ == '__main__':
	compare()