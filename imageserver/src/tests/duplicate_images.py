import os
import os.path
import optparse
import os
import random
from shutil import copyfile
from uuid import uuid4


def generate_random_duplicate_images(nr):
	cwd = os.getcwd()
	image_dir = cwd.replace('tests', 'images')
	os.chdir(image_dir)
	images = [name for name in os.listdir(image_dir) if os.path.isfile(name)]

	for i in xrange(nr):
		dest = '{}.jpg'.format(uuid4().hex[:8])
		source = random.choice(images)
		try:
			copyfile(source, dest)
			print 'step {}: {} generated from {}'.format(i, dest, source)
		except Exception, e:
			print str(e)


if __name__ == '__main__':
	parser = optparse.OptionParser(usage='python duplicate_images.py -n 100')
	parser.add_option('-n', '--number', action='store', dest='nr', help='Please enter a number of images you wish to be generated')
	(args, _) = parser.parse_args()
	if args.nr is None:
		print 'Missing argument -n/--number'
	else:
		generate_random_duplicate_images(nr=int(args.nr))