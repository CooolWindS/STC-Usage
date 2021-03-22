
### Define all file directories, it is best not to change
#
directory =  {'cover': 'files/cover/',
              'stego': 'files/stego/',
              'message_extract': 'files/message_extract/',
              'message_embed': 'files/message_embed/',
              'message_default': 'files/message.txt',
              'root': '/'}


###
#
channel = ['Gray', 'R', 'G', 'B', 'RGB']
# mode = [0, 1, 2, 3, 4]
# mode 5 means embed in all "R G B RGB" 
mode = 5

#
password = 's3cr3t'

#
payload = 1.0

#
# 256*256*2bpp/8 = 16384 chars
#msg_len = 16384
msg_len = 8100

#
log_file = None

#
succeed_or_failed = 0