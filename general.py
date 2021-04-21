#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import param
import util_zip
import txt
import util_excel
import update
import time
import shutil

txtdir_table = []
language_dict = {}
global_version = ''
global_date = ''

def get_platform_from_filename(filename):
	if False == isinstance(filename, str):
		print(sys._getframe().f_lineno, 'filename error', filename)
		return None
	position = filename.find('H1') #H1,H10,H14 all include 'H1'
	if -1 == position:
		print(sys._getframe().f_lineno, 'get platform error', filename)
		return None
	elif '_' == filename[position+2]:
		return filename[position:position+2]
	else:
		return filename[position:position+3]

def get_language_from_filename(filename):
	if False == isinstance(filename, str):
		print(sys._getframe().f_lineno, 'filename error', filename)
		return None
	start_position = filename.find('H1') #H1,H10,H14 all include 'H1'
	if -1 == start_position:
		print('get language error', filename)
		return None
	start_position = filename.find('_', start_position)
	
	end_position = filename.find('ML')
	if -1 == end_position:
		#print('try find _STD_')
		end_position = filename.find('STD')
		if -1 == end_position:
			print('line:', sys._getframe().f_lineno, 'error', filename)
			return None
	return filename[(start_position+1):(end_position-1)]

def get_version_from_filename(filename):
	if False == isinstance(filename, str):
		print(sys._getframe().f_lineno, 'filename error', filename)
		return None
	start_position = filename.find('_V')
	if -1 == start_position:
		print('line:', sys._getframe().f_lineno, 'error', filename)
		return None
	end_position = filename.find('_', start_position+1)
	if -1 == end_position:
		print('line:', sys._getframe().f_lineno, 'error', filename)
		return None
	return filename[(start_position+1):end_position]

def get_builddate_from_filename(filename):
	if False == isinstance(filename, str):
		print(sys._getframe().f_lineno, 'filename error', filename)
		return None
	start_position = filename.find('build')
	if -1 == start_position:
		print('line:', sys._getframe().f_lineno, 'error', filename)
		return None
	end_position = filename.find('.zip', start_position+1)
	if -1 == end_position:
		end_position = filename.find('_', start_position+1)
		if -1 == end_position:
			print('line:', sys._getframe().f_lineno, 'error', filename)
			return None
	return filename[start_position:end_position]

def update_excel():
	try:
		import openpyxl
	except ImportError:
		print('openpyxl has not been installed.')
		return None

	#更新excel文件
	excel_files = os.listdir(param.reference_file_path)
	for file in excel_files:
		if '.xls' in file and 'STD' in file:
			platform = get_platform_from_filename(file)
			language = get_language_from_filename(file)
			if platform in language_dict.keys() and language in language_dict[platform]:
				util_excel.update(global_version, global_date, os.path.join(param.reference_file_path, file))


def process_debug_file(filename):
	if 'DEBUG' not in filename:
		return None
	#更新参考历史固件识别码文件
	platform = get_platform_from_filename(filename)
	version = get_version_from_filename(filename)
	date = get_builddate_from_filename(filename)
	global global_version, global_date
	global_version = version
	global_date = date
	
	#更新txt文件
	update.update(platform, version, date, language_dict[platform])
	
	#解压
	src_file = os.path.join(param.unprocessed_file_path, filename)
	dst_dir = os.path.join(param.unprocessed_file_path, platform)
	ret_value = util_zip.unzip_txt(src_file, dst_dir)
	if 'OK' == ret_value:
		print('unzip %s OK' % src_file)
		txtdir_table.append(dst_dir)
		return ret_value
	else:
		print('line:', sys._getframe().f_lineno, ',unzip %s failed' % src_file)
		return 'Failed'

def process_std_file(filename):
	if 'STD' not in filename:
		return None
	language = get_language_from_filename(filename)
	platform = get_platform_from_filename(filename)
	if platform in language_dict.keys():
		temp = language_dict[platform]
	else:
		temp = []
	if language not in temp:
		temp.append(language)
	language_dict[platform] = temp

def main():
	#参数判断
	if False == isinstance(param.unprocessed_file_path, str) or \
	   '' == param.unprocessed_file_path:
		print('unprocessed_file_path error', param.unprocessed_file_path)
		return None
	if False == isinstance(param.reference_file_path, str) or \
	   '' == param.reference_file_path:
		print('reference_file_path error', param.reference_file_path)
		return None
	if False == isinstance(param.target_file_path, str) or \
	   '' == param.target_file_path:
		print('target_file_path error', param.target_file_path)
		return None

	#获取待处理目录下的文件列表
	'''
	目录下存在以下几种文件:
	1.DEBUG_FILE压缩包,需要解压以获得内部的文件
	2.STD固件包,需要根据此类包生成对应的txt文件,更新对应的excel文件
	3.NEU的中性包,暂不处理
	4.map和hicore_no_strip等调试文件,暂不处理
	'''
	unprocessed_files = os.listdir(param.unprocessed_file_path)

	#从unprocessed中, 根据固件包生成待处理语言表
	for file in unprocessed_files:
		process_std_file(file)
	print('language dict from different platforms:', language_dict)
	
	#备份参考文件
	backup_base_dir = os.path.join(param.reference_file_path, 'backup')
	if not os.path.exists(backup_base_dir):
		os.mkdir(path)
	cur_time = time.strftime('%Y-%m-%d-%H-%M-%S')
	backup_dir = os.path.join(backup_base_dir, cur_time)
	os.mkdir(backup_dir)
	
	backup_files = os.listdir(param.reference_file_path)
	for file in backup_files:
		file = os.path.join(param.reference_file_path, file)
		if os.path.isfile(file):
			shutil.copy(file, backup_dir)
	
	#解压unprocessed中的固件包信息,更新reference中的txt和excel文件
	for file in unprocessed_files:
		process_debug_file(file)
	

	update_excel()
	
	#转化txt文件,并将txt文件和excel表格存放到target文件夹中
	filenum = 0;
	for dir in txtdir_table:
		files = os.listdir(dir)
		for file in files:
			platform = get_platform_from_filename(file)
			language = get_language_from_filename(file)
			if platform in language_dict.keys() and language in language_dict[platform]:
				result = txt.fileExchange(file, dir, param.target_file_path, param.reference_file_path)
				if None != result:
					filenum += 1
	print('create %d txt files' % filenum)


if __name__ == '__main__':
	if 'unprocessed_file_path' not in dir(param) or \
	   'reference_file_path' not in dir(param) or \
	   'target_file_path' not in dir(param):
		print('param file is error, must have:')
		print('1.unprocessed_file_path')
		print('2.reference_file_path')
		print('3.target_file_path')
	else:
		main()


