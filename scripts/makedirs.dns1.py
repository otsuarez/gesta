import errno
import os

ROOT_DNSFILES_CONF  =  '/opt/sites/chroot/dns1.example.com/etc/includes/'
ROOT_DNSFILES_ZONES =  '/opt/sites/chroot/dns1.example.com/var/named/masters/'

dirs = (ROOT_DNSFILES_ZONES,ROOT_DNSFILES_CONF)

alphabet = 'abcdefghkmnopqrstuvwxyz'


def mk_path(root,dir):
	return os.path.join(root,dir)
	

def mk_dirs(root):
	for i in alphabet:
		DIRNAME = mk_path(root,i)

		try:
		# os.makedirs will also create all the parent directories
		    os.makedirs(DIRNAME)
		except OSError, err:
		    if err.errno == errno.EEXIST:
		        if os.path.isdir(DIRNAME):
		            print "directory already exists"
		        else:
		            print "file already exists, but not a directory"
		            raise # re-raise the exception
		    else:
		        raise
	

for i in dirs:
	mk_dirs(i)
