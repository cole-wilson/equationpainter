#!/usr/local/bin/python3
try:
	from PIL import Image
except:
	try:
		import Image
	except:
		from pillow import Image

import random
import xlsxwriter
import requests
import os


def main(name="", prefill=True, url="", path="", width=70, eqtype="+", custom="", maxans=100, numq=20):
	try:
		os.mkdir(os.path.expanduser("~" + os.sep + 'Desktop'))
	except FileExistsError:
		pass
	try:
		os.mkdir(os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter'))
	except FileExistsError:
		pass
	name = '{}.xlsx'.format(name)
	# print("Your spreadsheet will be named",name+",","and saved on your Desktop in a folder called EquationPainter.")
	workbook = xlsxwriter.Workbook(
		os.path.expanduser("~" + os.sep + 'Desktop' + os.sep) + 'EquationPainter' + os.sep + name)
	worksheet = workbook.add_worksheet()

	prefill = prefill

	if custom != "":
		filename = path
		operations = "n/a"
	else:
		filename = ""
		operations = eqtype

	max_answer = maxans
	siz = width
	offset = 3

	if filename != "":
		eqs = open(os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + filename)).read().split('\n')
		questions = len(eqs)

	# data = image pixels
	if url != "":
		a = requests.get(url, stream=True).raw
	else:
		a = os.path.expanduser(path)

	img = Image.open(a)
	change_in_size = img.width / siz
	new_height = round(img.height / change_in_size)
	result = img.resize((siz, new_height), resample=Image.BILINEAR)
	questions = numq
	width, height = result.size
	result = result.convert('P', palette=Image.ADAPTIVE, colors=questions)
	result = result.convert('RGB', palette=Image.ADAPTIVE, colors=questions)
	data = list(result.getdata())
	colors = set(data)

	key = {}
	keyRGB = {}
	answers = []
	count = 0
	for color in colors:  # todo: make it so that there are no white colors.
		if filename != "":
			num = int(eqs[count].split('|=>|')[1].replace(' ', ''))
			count += 1
		else:
			num = random.randint(0, max_answer)
		key[num] = '#%02x%02x%02x' % color
		keyRGB[color] = num
		answers.append(num)

	newdata = []
	for color in data:
		newdata.append(keyRGB[color])
	data = newdata
	white = workbook.add_format({'font_color': "#ffffff"})
	index3 = 3
	merge_format1 = workbook.add_format({'align': 'right', "valign": "vcenter", "font_size": 20})
	merge_format2 = workbook.add_format({'align': 'center', "valign": "vcenter", "font_size": 20})
	merge_format3 = workbook.add_format({'align': 'center', "valign": "vcenter", "font_size": 10, "bold": True})
	merge_format3.set_text_wrap()
	merge_format2.set_text_wrap()
	merge_format1.set_text_wrap()

	worksheet.merge_range(0, 0, 2, 2,
						  "Answer the problems below to paint the picture! You may have to zoom out a little.",
						  merge_format3)
	for index, answer in enumerate(answers):
		hexcode = key[answer]
		forma = workbook.add_format({'font_color': "#aaaaaa", "bold": True})
		forma.set_pattern(1)
		forma.set_bg_color(hexcode)
		worksheet.conditional_format(index3, 1, index3 + 2, 1, {'type': 'cell',
																'criteria': '=',
																'value': answer,
																'format': forma
																})
		if filename == "":
			operation = random.choice(operations)
			if operation == "+":
				p1 = random.randint(0, answer)
				p2 = answer - p1
			elif operation == "-":
				p1 = random.randint(0, answer)
				p2 = answer + p1
			equation = "{} {} {} =".format(p1, operation, p2)
		else:
			equation = eqs[index].split('|=>|')[0]
		worksheet.merge_range(index3, 0, index3 + 2, 0, equation, merge_format1)
		# print(index3,0,index3+2,0)
		if prefill:
			prefill_number = answer
		else:
			prefill_number = ""
		worksheet.merge_range(index3, 1, index3 + 2, 1, prefill_number, merge_format2)
		index3 += 3
	worksheet.merge_range(index3, 0, index3 + 2, 2, "Made with EquationPainter", merge_format2)

	count = 0
	for row in range(height):
		for col in range(width):
			num_for = data[count]
			forma = workbook.add_format({'font_color': key[num_for]})
			forma.set_pattern(1)
			forma.set_bg_color(key[num_for])
			worksheet.write(row, col + offset, "=B" + str((answers.index(num_for) * 3) + 4))
			worksheet.conditional_format(row, col + offset, row, col + offset, {'type': 'cell',
																				'criteria': '=',
																				'value': num_for,
																				'format': forma
																				})
			worksheet.conditional_format(row, col + offset, row, col + offset, {'type': 'cell',
																				'criteria': '!=',
																				'value': num_for,
																				'format': white
																				})
			count += 1
	worksheet.ignore_errors({'number_stored_as_text': 'A1:XFD1048576'})
	worksheet.ignore_errors({'empty_cell_reference': 'A1:XFD1048576'})
	worksheet.ignore_errors({'formula_differs': 'A1:XFD1048576'})
	worksheet.set_zoom(85)
	worksheet.set_column(offset, offset + width, 1.5)
	worksheet.set_column(0, 0, 25)
	worksheet.hide_gridlines(2)
	workbook.close()
	return os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter') + os.sep + name