import eel
import equationpainter.mainfile as mainfile
import sys
import logging
import os
import requests
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfile
import tkinter.messagebox
import json

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
path_to_dat = os.path.abspath(os.path.join(bundle_dir, 'web'))
logging.basicConfig(filename=path_to_dat + os.sep + 'log.txt', level=logging.INFO,format="[%(asctime)s] {%(name)s} %(levelname)s: %(message)s")

@eel.expose
def getFile():
	Tk().withdraw()
	try:
		filename = askopenfilename(initialdir=os.path.expanduser("~" + os.sep + 'Desktop' ))
		eel.chosefile(filename)
		logging.info("Got image file: {}".format(filename))
	except BaseException as e:
		logging.warn("Couldn't get image file: {}".format(e))


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
	try:
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
	except BaseException as e:
		Tk().withdraw()
		logging.error(e)
		tkinter.messagebox.showerror("Fatal Error:","EquationPainter had a fatal error that interrupted it's processing of your spreadsheet:\n\n\t{}\n\nThis may be cause you chose an option that was too large, or the spreadsheet name is already open. If you cannot resolve this error on your own, contact Cole at cole@colewilson.xyz.\nThank you for your patience!".format(e))


@eel.expose
def prev(name, prefill, url, path, width, eqtype, custom, maxans, numq):
	try:
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
		logging.info('Saved preview')
		eel.load_preview()
	except BaseException as e:
		logging.warn(e)

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
	try:
		main()
	except:
		logging.critical("Couldn't run main()")