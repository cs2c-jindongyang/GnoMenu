#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!
#
#(c) Whise 2009 <helderfraga@gmail.com>
#
# backend for saving and loading settings
# Part of the GnoMenu

import os

BACKEND = 'xml'
import xml.dom.minidom
print "xml backend"

HomeDirectory = os.path.expanduser("~")
ConfigDirectory = HomeDirectory + '/.gnomenu'

def save_setting(name,value):

	if BACKEND == 'xml':
		if name == '': return
		if os.path.isfile(ConfigDirectory + "/.GnoMenu-Settings.xml"):
			XMLSettings = xml.dom.minidom.parse(ConfigDirectory + "/.GnoMenu-Settings.xml")
			XBase = XMLSettings.getElementsByTagName('GnoMenu')[0]
		else:
			XMLSettings = xml.dom.minidom.Document()
			XBase = XMLSettings.createElement('GnoMenu')

		try:
			node = XMLSettings.getElementsByTagName('settings')[0]
		except:
			node = XMLSettings.createElement('settings')
		node.setAttribute(name, str(value))
		XBase.appendChild(node)
		XMLSettings.appendChild(XBase)
		file = open(ConfigDirectory + "/.GnoMenu-Settings.xml","w")
		XMLSettings.writexml(file, "    ", "", "", "UTF-8")
		XMLSettings.unlink()

	else:
		pass



def load_setting(name):

	if BACKEND == 'xml':
		if os.path.isfile(ConfigDirectory + "/.GnoMenu-Settings.xml"):
			XMLSettings = xml.dom.minidom.parse(ConfigDirectory + "/.GnoMenu-Settings.xml")
			x = XMLSettings.getElementsByTagName('GnoMenu')[0].getElementsByTagName("settings")[0]
			try:
				x = x.attributes[name].value
				try: 
					a = int(x)
					
				except:
					if str(x).find('[]') != -1 and name == 'favorites': return []
					

					if str(x).find(':') != -1:
						
						x = str(x).replace(" u'","").replace("u'","").replace("[","").replace("]","").replace("'","").replace("  "," ").replace('&quot;','"').replace("\\\\","\\").replace(", ",",")
						a = x.split(',')
					else:
						a = str(x)
					
				return a


			except: 
				if name == 'favorites': return []
				return None

		else: 
			return None

	else:
		pass


def get_default_mail_client():

	if BACKEND == 'xml':
		return "xdg-open mailto:"
	else:
		pass

def get_default_internet_browser():

	if BACKEND == 'xml':
		return "xdg-open http:"
	else:
		pass

