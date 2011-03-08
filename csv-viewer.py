#!/usr/bin/env python3

from os.path import isfile
from sys import argv, exit
from consolecolors import *
from csv import reader as csvreader

# Base parameters
delimiter  = ';'
strlimit   = '"'
linelimit  = '\n'
useheader  = True	# Parse first line as header
spaces     = 2		# Spaces count between columns
add_spaces = ' ' *6	# Add extra whitespaces for each line
add_lines  = '\n'	# Add extra line after header

# Colors
color_direction = 1		# 0 - no colors (except header, see below), 1 - columns, 2 - rows
header_color = C_GREEN	# C_WHITE, C_RED, C_BLUE and etc.
						# 0 - no color, 1 - use colors according to color direction
even_color = C_WHITE	# 0, 2, 4, 6 and etc.
odd_color  = C_YELLOW	# 1, 3, 5, 7 and etc.

# Columns align
aligns = {0: '<'}		# Right padding (left-aligned)
default_align = '>'		# Left padding (right-aligned)
head_aligns = {0: '^'}	# Center align
default_head_align = '>'

files = []
for arg in argv[1:]:
	if isfile(arg):
		files.append(arg)
if not files:
	print ('No file specified')
	exit(1)

cfile = csvreader(open(files[0]), delimiter =';', quotechar ='"')

rows = []
maxs = []
for row in cfile:
	rows.append(row[:])
	if not maxs:
		maxs = [len(field) for field in row]
	else:
		if len(row) > len(maxs):
			maxs.extend([0] * (len(row) - len(maxs)))
		for i in range(len(row)):
			if maxs[i] < len(row[i]):
				maxs[i] = len(row[i])

# Header format and show
if useheader:
	header = rows.pop(0)
	headspec = ''
	for findex in range(len(header)):
		align = head_aligns.get(findex, default_head_align)
		if color_direction == 1 and header_color == 1:
			color = odd_color if findex%2 else even_color
			headspec += color + '{:' + align + str(maxs[findex] + spaces) + '}' + C_CANCEL
		else:
			headspec += '{:' + align + str(maxs[findex] + spaces) + '}'
	if type(header_color) == str:
		print (add_spaces + header_color + headspec.format(*header) + C_CANCEL)
	elif color_direction == 2 and header_color == 1:
		print (add_spaces + odd_color + headspec.format(*header) + C_CANCEL)
	else:
		print (add_spaces + headspec.format(*header))
	if add_lines:
		print (add_lines, end ='')

# Rows formatting
rowspec = ''
for findex in range(len(maxs)):
	align = aligns.get(findex, default_align)
	if color_direction == 1:
		color = odd_color if findex%2 else even_color
		rowspec += color + '{:' + align + str(maxs[findex] + spaces) + '}' + C_CANCEL
	else:
		rowspec += '{:' + align + str(maxs[findex] + spaces) + '}'

# Show rows
max_fields_count = len(maxs)
for row_index in range(len(rows)):
	if not rows[row_index]:
		print ()
	else:
		# Add extra empty fields if fields count in row is less than max fields count
		if len(rows[row_index]) < max_fields_count:
			rows[row_index].extend([''] * (max_fields_count - len(rows[row_index])))
		if color_direction == 2:
			color = odd_color if row_index%2 else even_color
			print (add_spaces + color + rowspec.format(*rows[row_index]).rstrip() + C_CANCEL)
		else:
			print (add_spaces + rowspec.format(*rows[row_index]).rstrip())

