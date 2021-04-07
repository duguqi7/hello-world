#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
platform_table = ['H1', 'H10', 'H14']
#reference_path = 'G:\\py_scrip\\reference'

def get_vernum(version):
	if False == isinstance(version, str):
		print(sys._getframe().f_lineno, 'version error', version)
		return ''
	elif version[0] != 'V' and version[0] != 'v':
		print(sys._getframe().f_lineno, 'version type error', version)
		return ''
	start_postion = 1;
	end_position = version.find('.', start_postion)
	if -1 == end_position:
		print('version error', version)
		return ''
	main = version[start_postion:end_position].rjust(2, '0')
	start_postion = 1+end_position;
	end_position = version.find('.', start_postion)
	if -1 == end_position:
		print('version error', version)
		return ''
	sub = version[start_postion:end_position].rjust(2, '0')
	start_postion = 1+end_position;
	end_position = version.find('build')
	if -1 == end_position:
		print('version error', version)
		return ''
	aux = version[start_postion:end_position].rjust(4, '0')
	return (main + sub + aux)

def get_date(version):
	if False == isinstance(version, str):
		print('version error', version)
		return ''
	start_postion = version.find('build') + len('build')
	year = int(version[start_postion:start_postion+2])
	month = int(version[start_postion+2:start_postion+4])
	day = int(version[start_postion+4:])
	if year < 20 or month > 12 or day > 31:
		print('version simple check error', version)
		return ''
	#组建版本日期
	date = hex(year)[2:4].rjust(2, '0') + hex(month)[2:4].rjust(2, '0') + hex(day)[2:4].rjust(2, '0')
	return date.rjust(8, '0')

def update(platform, version, date):
	if platform not in platform_table:
		print('platform error', platform)
		return None
	elif 'V' not in version:
		print('version error', version)
		return None
	elif 'build' not in date:
		print('date error', date)
		return None

	version_num = get_vernum(version)
	date = get_date(date)
	print(version_num, date)

	#打开文件
	if 'reference_path' not in locals().keys():
		reference_path = os.path.abspath('.')
	file_name = platform + '.txt'
	reference_file = os.path.join(reference_path, file_name)
	reference_fd = open(reference_file, 'r+')
	lines = reference_fd.readlines()
	
	#修改
	template = ''
	update_line = ''
	record_flag = 0
	reference_fd.seek(0)
	for line in lines:
		if ':' in line:
			print(line.strip())
			record_flag = 1
		elif '-' in line:
			if template != '':
				update_line = template[:64] + version_num + date + template[-9:]
				reference_fd.write(update_line)
		elif 1 == record_flag:
			template = line
			record_flag = 0
		reference_fd.write(line)
	reference_fd.close()



if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('usage: python update.py [platform(H1, H10, H14)] [build date]')
	else:
		main(sys.argv[1], sys.argv[2])

