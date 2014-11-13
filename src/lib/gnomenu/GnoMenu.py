#!/usr/bin/env python

# This application is released under the GNU General Public License 
# v3 (or, at your option, any later version). You can find the full 
# text of the license under http://www.gnu.org/licenses/gpl.txt. 
# By using, editing and/or distributing this software you agree to 
# the terms and conditions of this license. 
# Thank you for using free software!
#
#(c) QB89Dragon 2007/8 <hughescih@hotmail.com>
#(c) Whise 2008,2009,2010 <helderfraga@gmail.com>
#
# Consolidated Gnome Menu
# This is free software made available under the GNU public license.
# Use 'run-in-window' command switch for development testing

import os
import gi
gi.require_version("Gtk", "2.0")

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import MatePanelApplet

class GnoMenu(MatePanelApplet.Applet):

	def __init__(self,applet):
		self.applet = applet
		self.Button_state = 0 # 0 = No change  1 = Mouse over  2 = Depressed

		self.EBox = Gtk.EventBox()
		self.applet_icon = Gtk.Image()
		pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("/usr/share/gnomenu/Themes/Button/XP/start-here.png",-1,-1)
		self.applet_icon.set_from_pixbuf(pixbuf)
		self.applet_icon.show()
		self.EBox.add(self.applet_icon)
		self.applet.add(self.EBox)
		self.EBox.connect("button-press-event",self.press_box)
		self.EBox.connect("enter-notify-event", self.select_box)
		self.EBox.connect("leave-notify-event", self.deselect_box)
		self.applet.show_all()
		from Menu_Main import Main_Menu
		self.hwg = Main_Menu(self.HideMenu)
		self.x,self.y = 0,10000
		self.time = 0
		self.hwg.Adjust_Window_Dimensions(self.x,self.y)

	def press_box(self, widget,event):
		if (event.button == 1) and (self.time != event.time):
			if not self.hwg.window.window:
				self.ShowMenu()
				self.Button_state = 2
			else:
				if self.Button_state == 2:
					self.HideMenu()
					self.Button_state = 1
				else:
					self.ShowMenu()
					self.Button_state = 2
			self.Redraw_graphics()
		self.time = event.time

	def ShowMenu(self):
		self.hwg.Adjust_Window_Dimensions(self.x,self.y)
		if self.hwg:
			self.hwg.show_window()
		

	def HideMenu(self):
		if self.hwg:
			if self.hwg.window.window:
				if self.hwg.window.window.is_visible()== True:
					self.hwg.hide_window()
		self.Button_state = 1
		self.Redraw_graphics()

	def release_box(self,widget,event):
		self.Button_state = 1
		self.Redraw_graphics()

	def select_box(self,widget,event):
		if self.Button_state == 0:
			self.Button_state = 1
			self.Redraw_graphics()

	def deselect_box(self,widget,event):
		if self.Button_state == 1:
			self.Button_state = 0
			self.Redraw_graphics()

	def Redraw_graphics (self):
		if self.Button_state == 0:
			self.applet_icon.set_from_file("/usr/share/gnomenu/Themes/Button/XP/start-here.png")
		if self.Button_state == 1:
			self.applet_icon.set_from_file("/usr/share/gnomenu/Themes/Button/XP/start-here-glow.png")
		if self.Button_state == 2:
			self.applet_icon.set_from_file("/usr/share/gnomenu/Themes/Button/XP/start-here-depressed.png")
		
		
def applet_factory(applet, iid, data):
    if iid != "GnoMenuApplet":
       return False

    import os
    HomeDirectory = os.path.expanduser("~")
    ENV_PATH = '/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:' + HomeDirectory + '/.local/bin:'  + HomeDirectory + '/bin'
    os.environ['PATH'] = ENV_PATH
    os.environ['GTK_IM_MODULE'] = 'ibus'
    os.environ['IMSETTINGS_INTEGRATE_DESKTOP'] = 'yes'
    os.environ['IMSETTINGS_MODULE'] = 'IBus'
    os.environ['QT_IM_MODULE'] = 'ibus'
    os.environ['XMODIFIERS'] = '@im=ibus'

    app = GnoMenu(applet)

    return True
	
if __name__ == '__main__':

	MatePanelApplet.Applet.factory_main("GnoMenuAppletFactory", True,
                                    MatePanelApplet.Applet.__gtype__,
                                    applet_factory, None)

