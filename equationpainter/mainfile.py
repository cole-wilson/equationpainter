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

def main(name="", prefill=True, url="", path="", width=70, eqtype="+", custom="", maxans=100, numq=20,
		 dirs="", offset=3, copyright="", mergeheight=3, pixelcol=1.5,anscol="#aaaaaa",initzoom=70,fontsize=20):
	try:
		os.mkdir(os.path.expanduser("~" + os.sep + 'Desktop'))
	except FileExistsError:
		pass
	try:
		os.mkdir(os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter'))
	except FileExistsError:
		pass
	try:
		os.mkdir(os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter' + os.sep + "presets"))
	except FileExistsError:
		pass
	try:
		os.mkdir(os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter' + os.sep + "images"))
	except FileExistsError:
		pass
	
	name = '{}.xlsx'.format(name)
	# print("Your spreadsheet will be named",name+",","and saved on your Desktop in a folder called EquationPainter.")
	workbook = xlsxwriter.Workbook(
		os.path.expanduser("~" + os.sep + 'Desktop' + os.sep) + 'EquationPainter' + os.sep + name)
	worksheet = workbook.add_worksheet()

	prefill = prefill == "true"

	if custom != "":
		filename = path
		operations = "n/a"
	else:
		filename = ""
		operations = eqtype

	max_answer = maxans
	siz = width


	# data = image pixels
	if url != "":
		a = requests.get(url, stream=True).raw
	else:
		a = os.path.expanduser(path)
	if custom != "":
		eqs = []
		for line in custom.split('\n'):
			if "|=>|" in line and not line.startwith('//'):
				eqs.append(tuple(line.split('|=>|')))
		print(eqs)
		questions = len(eqs)
	img = Image.open(a)
	if url != "":
		img.save(os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter' + os.sep + "images" + os.sep + name + ".png"),format="PNG")
	change_in_size = img.width / siz
	new_height = round(img.height / change_in_size)
	result = img.resize((siz, new_height), resample=Image.BILINEAR)
	if custom == "":
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
	if maxans < questions:
		maxans = questions + 1
	randomints = random.sample(list(range(0,maxans)),questions)
	print(questions)
	print(colors)
	for icount,color in enumerate(colors):  # todo: make it so that there are no white colors.
		if filename != "":
			print(eqs[count])
			num = int(eqs[count-1][1].replace(' ', ''))
			count += 1
		else:
			num = randomints[icount]
		key[num] = '#%02x%02x%02x' % color
		keyRGB[color] = num
		answers.append(num)

	newdata = []
	for color in data:
		newdata.append(keyRGB[color])
	data = newdata
	white = workbook.add_format({'font_color': "#ffffff"})
	index3 = mergeheight
	merge_format1 = workbook.add_format({'align': 'right', "valign": "vcenter", "font_size": fontsize})
	merge_format2 = workbook.add_format({'align': 'center', "valign": "vcenter", "font_size": fontsize})
	merge_format3 = workbook.add_format({'align': 'center', "valign": "vcenter", "font_size": round(fontsize*0.7), "bold": True})
	merge_format3.set_text_wrap()
	merge_format2.set_text_wrap()
	merge_format1.set_text_wrap()

	worksheet.merge_range(0, 0, mergeheight-1, offset-1,
						  dirs,
						  merge_format3)
	for index, answer in enumerate(answers):
		hexcode = key[answer]
		forma = workbook.add_format({'font_color': anscol, "bold": True})
		forma.set_pattern(1)
		forma.set_bg_color(hexcode)
		worksheet.conditional_format(index3, 1, index3 + mergeheight - 1, 1, {'type': 'cell',
																'criteria': '=',
																'value': answer,
																'format': forma
																})
		if eqtype != "custom":
			operation = random.choice(operations)
			if operation == "+":
				p1 = random.randint(0, answer)
				p2 = answer - p1
			elif operation == "-":
				p1 = random.randint(0, answer)
				p2 = answer + p1
			equation = "{} {} {} =".format(p1, operation, p2)
		else:
			equation = eqs[index][0]
		worksheet.merge_range(index3, 0, index3 + mergeheight - 1, 0, equation, merge_format1)
		# print(index3,0,index3+2,0)
		if prefill:
			prefill_number = answer
		else:
			prefill_number = ""
		worksheet.merge_range(index3, 1, index3 + mergeheight - 1, 1, prefill_number, merge_format2)
		index3 += mergeheight
	worksheet.merge_range(index3, 0, index3 + mergeheight - 1, 2, "Made with EquationPainter" if copyright=="true" else "", merge_format2)

	count = 0
	for row in range(height):
		for col in range(width):
			num_for = data[count]
			forma = workbook.add_format({'font_color': key[num_for]})
			forma.set_pattern(1)
			forma.set_bg_color(key[num_for])
			worksheet.write(row, col + offset, "=B" + str((answers.index(num_for) * mergeheight + 1) + mergeheight))
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
	worksheet.set_zoom(initzoom)
	worksheet.set_column(offset, offset + width, pixelcol)
	worksheet.set_column(0, 0, 25)

	worksheet.hide_gridlines(2)
	workbook.close()
	return os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + 'EquationPainter') + os.sep + name
