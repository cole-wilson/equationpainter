import eel
import equationpainter.mainfile as mainfile
import sys
import os

filename = ""
@eel.expose
def generate(name, prefill, url, path, width, eqtype, custom, maxans, numq):
	global filename
	filename = mainfile.main(
		name=name,
		prefill=bool(prefill),
		url=url,
		path=path,
		width=int(width),
		eqtype=eqtype,
		custom=custom,
		maxans=int(maxans),
		numq=int(numq)
	)
	print(filename)
	eel.done()

@eel.expose
def launch():
	if sys.platform.startswith('win'):
		runcommand = "start excel.exe {}".format(filename)
		print(runcommand)
		os.system(runcommand)
	elif sys.platform.startswith('dar'):
		os.system("open -a Excel {}".format(filename))

def main():
	eel.init('web')
	eel.start('main.html', size=(400, 500))

if __name__ == "__main__":
	main()