#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import zipfile

def unzip_txt(src_file, dst_dir):
	if False == isinstance(src_file, str) or \
	   '' == src_file or \
	   False == isinstance(dst_dir, str) or \
	   '' == dst_dir:
		print(sys._getframe().f_lineno, 'src_file or dst_dir error', src_file, dst_dir)
		return None

	zip_files = zipfile.ZipFile(src_file)
	for zip_file in zip_files.namelist():
		if 'STD' in zip_file and 'CI' not in zip_file:
			zip_files.extract(zip_file, dst_dir)
	return 'OK'

def unzip(src_file, dst_dir):
	if False == isinstance(src_file, str) or \
	   '' == src_file or \
	   False == isinstance(dst_dir, str) or \
	   '' == dst_dir:
		print(sys._getframe().f_lineno, 'src_file or dst_dir error', src_file, dst_dir)
		return None
	
	zip_files = zipfile.ZipFile(src_file)
	for zip_file in zip_files.namelist():
		zip_files.extract(zip_file, dst_dir)


def main():
	files = os.listdir('.')
	for file in files:
		file_name, file_type = os.path.splitext(file)
		if file_type == '.zip':
			src_file = os.path.join((os.path.abspath('.')), file)
			dst_dir = os.path.join((os.path.abspath('.')), (file_name+'_unzip'))
			unzip(src_file, dst_dir)


if __name__ == '__main__':
	main()
