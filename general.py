#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import param
#import util_zip
#import util_txt
#import util_excel
import update

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
			print('error', filename)
			return None
	return filename[(start_position+1):(end_position-1)]

def get_version_from_filename(filename):
	if False == isinstance(filename, str):
		print(sys._getframe().f_lineno, 'filename error', filename)
		return None
	start_position = filename.find('_V')
	if -1 == start_position:
		print('error', filename)
		return None
	end_position = filename.find('_', start_position+1)
	if -1 == end_position:
		print('error', filename)
		return None
	return filename[(start_position+1):end_position]

def get_builddate_from_filename(filename):
	if False == isinstance(filename, str):
		print(sys._getframe().f_lineno, 'filename error', filename)
		return None
	start_position = filename.find('build')
	if -1 == start_position:
		print('error', filename)
		return None
	end_position = filename.find('.zip', start_position+1)
	if -1 == end_position:
		print('error', filename)
		return None
	return filename[start_position:end_position]



def process_debug_file(filename):
	if 'DEBUG' not in filename:
		return None
	#更新参考历史固件识别码文件
	platform = get_platform_from_filename(filename)
	version = get_version_from_filename(filename)
	date = get_builddate_from_filename(filename)
	update.update(platform, version, date)
	#解压
	

def process_std_file(filename):
	if 'STD' not in filename::
		return None
	

def main(unprocessed_file_path, reference_file_path, target_file_path):
	#参数判断
	if False == isinstance(unprocessed_file_path, str) or \
	   '' == unprocessed_file_path:
		print('unprocessed_file_path error', unprocessed_file_path)
		return None
	if False == isinstance(reference_file_path, str) or \
	   '' == reference_file_path:
		print('reference_file_path error', reference_file_path)
		return None
	if False == isinstance(target_file_path, str) or \
	   '' == target_file_path:
		print('target_file_path error', target_file_path)
		return None
	#获取待处理目录下的文件列表
	'''
	目录下存在以下几种文件:
	1.DEBUG_FILE压缩包,需要解压以获得内部的资料
	2.STD固件包,需要根据此类包生成对应的txt文件,更新对应的excel文件
	3.NEU的中性包,暂不处理
	4.map和hicore_no_strip等调试文件,暂不处理
	'''
	unprocessed_files = os.list(unprocessed_file_path)

	#解压压缩文件
	for file in unprocessed_files:
		process_debug_file(file)
	#生成txt文件和excel函数
	for file in unprocessed_files:
		process_std_file(file)





if __name__ == '__main__':
	if 'unprocessed_file_path' not in dir(param) or \
	   'reference_file_path' not in dir(param) or \
	   'target_file_path' not in dir(param):
		print('param file is error, must have:')
		print('1.unprocessed_file_path')
		print('2.reference_file_path')
		print('3.target_file_path')
	else:
		main(param.unprocessed_file_path, param.reference_file_path, param.target_file_path)


