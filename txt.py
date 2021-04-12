#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

test_path = 'G:\\py_scrip\\test'
target_path = 'G:\\py_scrip\\target'
reference_path = 'G:\\py_scrip\\reference'
language_table = ['EN', 'ES', 'RU', 'CZ', 'GR', 'HR', 'PL', 'RO', 'TR', 'SI', 'SK', 'PT_BR', 'CN']

def get_language(filename):
	if False == isinstance(filename, str):
		print('filename error', filename)
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

def getKeyValue(string, key):
	if False == isinstance(string, str) or False == isinstance(key, str):
		print('arguments error: find ', key, 'in ', string)
		return []
	start_position = 0
	end_position = 0
	result = []
	start_position = string.find(key)
	if start_position != -1:
		end_position = string.find('\n', start_position)
	else:
		print('can not find %s in %s' % (key, string))
		return result
	if -1 == end_position:
		print('file error')
		return result
	result = string[(start_position+1+len(key)) : end_position]
	return result

def fileExchange(file, test_path, target_path, reference_path):
	if False == isinstance(file, str):
		print('argument error', file)
		return None
	language = get_language(file)
	
	if language not in language_table:
		return None
	
	#print('deal with ', file)
	target_file = os.path.join(target_path, file)
	test_file = os.path.join(test_path, file)
	target_fd = open(target_file, 'w')
	#print(test_file)
	test_fd = open(test_file, 'r')
	words = test_fd.read()
	test_fd.close()
	#version
	key_value = getKeyValue(words, 'soft_version')
	version = key_value
	write_line = 'version=' + key_value + '\n'
	target_fd.write(write_line)
	#pversion
	key_value = version[:6]
	write_line = 'pversion=' + key_value + '\n'
	target_fd.write(write_line)
	#md5
	key_value = getKeyValue(words, 'digicap_md5')
	write_line = 'md5=' + key_value + '\n'
	target_fd.write(write_line)
	#platform
	key_value = getKeyValue(words, 'platform')
	field = key_value
	write_line = 'platform=' + key_value + '\n'
	target_fd.write(write_line)
	#language
	language = getKeyValue(words, 'language')
	write_line = 'language=' + language + '\n'
	target_fd.write(write_line)
	#config
	key_value = getKeyValue(words, 'config')
	write_line = 'config=' + key_value + '\n'
	target_fd.write(write_line)
	#field
	write_line = 'field=' + field + '\n'
	target_fd.write(write_line)
	#zipmd5
	key_value = getKeyValue(words, 'zip_md5')
	write_line = 'zipmd5=' + key_value + '\n'
	target_fd.write(write_line)
	#filename
	filename = 'digicap.dav'
	write_line = 'filename=' + filename + '\n'
	target_fd.write(write_line)
	#firmwarecode
	firmwarecode = ''
	reference_name = field + '.txt'
	reference_file = os.path.join(reference_path, reference_name)
	reference_fd = open(reference_file, 'r')
	while True:
		line_temp = reference_fd.readline()
		if False == bool(line_temp) or line_temp.find(language) != -1:
			break
	if True == bool(line_temp):
		while True:
			line_temp = reference_fd.readline().strip()
			if line_temp.find('---') != -1:
				break
			elif False == bool(firmwarecode):
				firmwarecode = firmwarecode + line_temp
			else:
				firmwarecode = firmwarecode + ',' + line_temp
	write_line = 'firmwarecode=' + firmwarecode
	target_fd.write(write_line)
	reference_fd.close()
	target_fd.close()
	print('create %s OK' % target_file)

def main():
	files = os.listdir(test_path)
	for file in files:
		if (-1 == file.find('CID')) and (file.find('STD') != -1):
			fileExchange(file, test_path, target_path, reference_path)


if __name__ == '__main__':
	main()
