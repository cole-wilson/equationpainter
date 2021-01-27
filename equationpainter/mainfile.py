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

def main():
	try:
		os.mkdir(os.path.expanduser("~"+os.sep+'Desktop'))
	except FileExistsError:
		pass
	try:
		os.mkdir(os.path.expanduser("~"+os.sep+'Desktop'+os.sep+'EquationPainter'))
	except FileExistsError:
		pass
	name = '{}.xlsx'.format(input('Give a name to your spreadsheet!\n> '))
	print("Your spreadsheet will be named",name+",","and saved on your Desktop in a folder called EquationPainter.")
	workbook = xlsxwriter.Workbook(os.path.expanduser("~"+os.sep+'Desktop'+os.sep)+'EquationPainter'+os.sep+name)
	worksheet = workbook.add_worksheet()



	prefill = (input('Prefill answers? [y/n]\n> ')+"n").lower()[0] == 'y'

	if (input('Use equation file? [y/n]\n> ')+"n").lower()[0] == 'y':
		filename = input("Filename:\n> Desktop"+os.sep)
		operations = "n/a"
	else:
		filename = ""
		operations = input('Which operations should I use? + or - or +-:\n> ')

	while True:
		if filename != "":
			break
		try:
			max_answer = abs(int(input('What should the highest answer be?\n> ')))
			break
		except:
			print('Please provide a number!')
	while True:
		try:
			siz = abs(int(input('What should the width of the image be in column pixels? (78 default)\n> ')))
			break
		except:
			print('Please provide a number!')

	offset = 3

	if filename != "":
		eqs = open(os.path.expanduser("~"+os.sep+'Desktop'+os.sep+filename)).read().split('\n')
		questions = len(eqs)

	# data = image pixels
	u = input("URL or path to image on desktop:\n> ")
	if u.startswith('http'):
		a = requests.get(u, stream=True).raw
	else:
		a = os.path.expanduser("~"+os.sep+'Desktop'+os.sep+u)

	img = Image.open(a)
	change_in_size = img.width/siz
	new_height = round(img.height/change_in_size)
	result = img.resize((siz,new_height),resample=Image.BILINEAR)
	normal_colors = result.convert('P', palette=Image.ADAPTIVE)
	numcol = len(set(normal_colors.getdata()))
	while True:
		if filename != "":
			break
		try:
			questions = abs(int(input('\nHow many questions should there be? (256 or less reccomended, must be more than 3)\n> ')))
			assert questions > 3
			assert questions <= 256
			break
		except:
			print('Non-valid input.')

	perq = 256//questions
	lefover = 256% questions

	width,height = result.size
	result = result.convert('P', palette=Image.ADAPTIVE, colors=questions)
	result = result.convert('RGB', palette=Image.ADAPTIVE, colors=questions)
	data = list(result.getdata())
	colors = set(data)


	key = {}
	keyRGB = {}
	answers = []
	count = 0
	for color in colors: # todo: make it so that there are no white colors.
		if filename != "":
			num = int(eqs[count].split('|=>|')[1].replace(' ',''))
			count += 1
		else:
			num = random.randint(0,max_answer)
		key[num] = '#%02x%02x%02x' % color
		keyRGB[color] = num
		answers.append(num)

	newdata = []
	for color in data:
		newdata.append(keyRGB[color])
	data = newdata
	white = workbook.add_format({'font_color':"#ffffff"})
	index3 = 3
	merge_format1 = workbook.add_format({'align': 'right',"valign":"vcenter","font_size":20})
	merge_format2 = workbook.add_format({'align': 'center',"valign":"vcenter","font_size":20})
	merge_format3 = workbook.add_format({'align': 'center',"valign":"vcenter","font_size":10,"bold":True})
	merge_format3.set_text_wrap()
	merge_format2.set_text_wrap()
	merge_format1.set_text_wrap()

	worksheet.merge_range(0,0,2,2, "Answer the problems below to paint the picture! You may have to zoom out a little.",merge_format3)
	for index, answer in enumerate(answers):
		hexcode = key[answer]
		forma = workbook.add_format({'font_color':"#aaaaaa","bold":True})
		forma.set_pattern(1)
		forma.set_bg_color(hexcode)
		worksheet.conditional_format(index3,1,index3+2,1, {'type':     'cell',
			'criteria': '=',
			'value':     answer,
			'format':    forma
		})
		if filename == "":
			operation = random.choice(operations)
			if operation == "+":
				p1 = random.randint(0, answer)
				p2 = answer - p1
			elif operation == "-":
				p1 = random.randint(0, answer)
				p2 = answer + p1
			equation = "{} {} {} =".format(p1,operation,p2)
		else:
			equation = eqs[index].split('|=>|')[0]
		worksheet.merge_range(index3,0,index3+2,0, equation,merge_format1)
		# print(index3,0,index3+2,0)
		if prefill:
			prefill_number = answer
		else:
			prefill_number = ""
		worksheet.merge_range(index3,1,index3+2,1, prefill_number,merge_format2)
		index3 += 3
	worksheet.merge_range(index3,0,index3+2,2, "Made with EquationPainter",merge_format2)

	count = 0
	for row in range(height):
		for col in range(width):
			num_for = data[count]
			forma = workbook.add_format({'font_color':key[num_for]})
			forma.set_pattern(1)
			forma.set_bg_color(key[num_for])
			worksheet.write(row, col+offset, "=B"+str((answers.index(num_for)*3)+4))
			worksheet.conditional_format(row,col+offset,row,col+offset, {'type':     'cell',
				'criteria': '=',
				'value':     num_for,
				'format':    forma
			})
			worksheet.conditional_format(row,col+offset,row,col+offset, {'type':     'cell',
				'criteria': '!=',
				'value':     num_for,
				'format':    white
			})
			count += 1
	worksheet.ignore_errors({'number_stored_as_text': 'A1:XFD1048576'})
	worksheet.ignore_errors({'empty_cell_reference': 'A1:XFD1048576'})
	worksheet.ignore_errors({'formula_differs': 'A1:XFD1048576'})
	worksheet.set_zoom(85)
	worksheet.set_column(offset,offset+width,1.5)
	worksheet.set_column(0,0,25)
	worksheet.hide_gridlines(2)
	workbook.close()