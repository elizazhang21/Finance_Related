__Author__ = 'Elizabeth Zhang'

import time

def is_dst():
	return bool(time.localtime().tm_isdst)

print(is_dst())