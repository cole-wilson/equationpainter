#!/usr/bin/env python3

# +------------------------+			   
# | Created with Sailboat  |			   
# |			                   |			   
# | Do not edit this file  |			   
# | directly. Instead  	   |			   
# | you should edit the	   |			   
# | `sailboat.toml` file.  |			   
# +------------------------+	

import setuptools

try:
  with open("README.md", "r") as fh:
	  long_description = fh.read()
except:
	long_description = "# EquationPainter\nA way for teachers to make equation painter worksheets for their students.\n### Contributors\n- Cole Wilson\n### Contact\n<cole@colewilson.xyz> "

options = {
	"name":"equationpainter",
	"version":"3.3.14",
	"scripts":[],
	"entry_points":{'console_scripts': ['eqpaint=equationpainter.__main__:main']},
	"author":"Cole Wilson",
	"author_email":"cole@colewilson.xyz",
	"description":"A way for teachers to make equation painter worksheets for their students.",
	"long_description":long_description,
	"long_description_content_type":"text/markdown",
	"url":"https://github.com/cole-wilson/wsm",
	"packages":setuptools.find_packages(),
	"install_requires":['requests', 'pillow', 'xlsxwriter', 'Image', 'eel', 'gevent', 'bottle', 'bottle_websocket'],
	"classifiers":["Programming Language :: Python :: 3"],
	"python_requires":'>=3.6',
	"package_data":{"": ['web/*'],},
	"license":"MIT",
	"keywords":'',
}

custom_options = {}

if __name__=="__main__":
	setuptools.setup(**custom_options,**options)