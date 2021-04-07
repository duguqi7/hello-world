#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zipfile

def unzip(src_file, dst_dir):
	if False == isinstance(src_file, str) or \
	   '' == src_file or \
	   False == isinstance(dst_dir, str) or \
	   '' == dst_dir:
		print(sys._getframe().f_lineno, 'src_file or dst_dir error', src_file, dst_dir)
		return None


def main():
	files = os.listdir(test_path)
	for file in files:
		if (-1 == file.find('CID')) and (file.find('STD') != -1):
			fileExchange(file)


if __name__ == '__main__':
	main()
