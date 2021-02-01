import eel
import equationpainter.mainfile as mainfile
import sys
import os
import requests
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter.messagebox
import json

@eel.expose
def getFile():
	Tk().withdraw()
	filename = askopenfilename(initialdir=os.path.expanduser("~" + os.sep + 'Desktop' ))
	eel.chosefile(filename)

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_dat = os.path.abspath(os.path.join(bundle_dir, 'web'))
# input(path_to_dat)
# input(getattr(sys, '_MEIPASS'))
filename = ""
@eel.expose
def save(*args):
	Tk().withdraw()
	
	fname = asksaveasfile(initialfile="presetname",defaultextension=".json",initialdir=os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + "EquationPainter" + os.sep + "presets"))
	a = open(fname.name,'w+')
	a.write(json.dumps(args, indent=4, sort_keys=True))

@eel.expose
def load(*args):
	Tk().withdraw()
	fname = askopenfilename(initialdir=os.path.expanduser("~" + os.sep + 'Desktop' + os.sep + "EquationPainter" + os.sep + "presets"))
	a = open(fname,'r')
	d = json.loads(a.read())
	a.close()
	eel.loadpreset(*d)

@eel.expose
def generate(name, prefill, url, path, width, eqtype, custom, maxans, numq,dirs,offset,copyright,mergeheight,pixelcol,anscol,initzoom,fontsize):
	global filename
	filename = mainfile.main(
		name=name,
		prefill=prefill,
		url=url,
		path=path,
		width=int(width),
		eqtype=eqtype,
		custom=custom,
		maxans=int(maxans),
		numq=int(numq),
		dirs=dirs, offset=int(offset), copyright=copyright, mergeheight=int(mergeheight),pixelcol=float(pixelcol),
		anscol=anscol,
		initzoom=round(float(initzoom)),
		fontsize=int(fontsize)
	)
	print(filename)
	eel.done()

@eel.expose
def prev(name, prefill, url, path, width, eqtype, custom, maxans, numq):
	width = int(width)
	numq = int(numq)

	if url != "":
		a = requests.get(url, stream=True).raw
	else:
		a = os.path.expanduser(path)
	img = Image.open(a)
	change_in_size = img.width / width
	new_height = round(img.height / change_in_size)
	result = img.resize((width, new_height), resample=Image.BILINEAR)
	questions = numq
	if custom != "":
		eqs = []
		for line in custom.split('\n'):
			if "|=>|" in line and not line.startswith('//'):
				eqs.append(tuple(line.split('|=>|')))
		questions = len(eqs)
	width, height = result.size
	result = result.convert('P', palette=Image.ADAPTIVE, colors=questions)
	result = result.convert('RGB', palette=Image.ADAPTIVE, colors=questions)
	result.save(path_to_dat+os.sep+"preview.png",format="PNG")
	print(path_to_dat+os.sep+"preview.png")
	eel.load_preview()

@eel.expose
def launch():
	if sys.platform.startswith('win'):
		runcommand = "start excel.exe {}".format(filename)
		print(runcommand)
		os.system(runcommand)
	elif sys.platform.startswith('dar'):
		os.system("open -a Excel {}".format(filename))

def main():
	eel.init(path_to_dat)
	eel.start('main.html', size=(400, 500),port=7890)

if __name__ == "__main__":
	main()