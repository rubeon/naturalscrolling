#!/usr/bin/env python
import sys
import os
import gtk
import appindicator

from naturalscrolling_lib import naturalscrollingconfig 
from naturalscrolling.AboutNaturalscrollingDialog import AboutNaturalscrollingDialog

import gettext
from gettext import gettext as _
gettext.textdomain('naturalscrolling')

class NaturalscrollingIndicator: 
    def __init__(self):
        self.AboutDialog = AboutNaturalscrollingDialog
        self.mouseid = self.get_slave_pointer() 
        self.pingfrequency = 1 # in seconds
        
        self.ind = appindicator.Indicator("natural-scrolling-indicator", 'natural-scrolling-status-not-activated', appindicator.CATEGORY_APPLICATION_STATUS)

        media_path = "%s/media/" % naturalscrollingconfig.get_data_path()
        print media_path
        self.ind.set_icon_theme_path (media_path)
        self.ind.set_attention_icon  ("natural-scrolling-status-activated")
        
        self.menu_setup()
        self.ind.set_menu (self.menu)

    def get_slave_pointer (self):
        cmd = "xinput list | grep pointer | grep slave | grep -v XTEST | gawk -F'id=' '{print $2}' | gawk '{print $1}'"
        slavepointer = os.popen (cmd).read().split()
        return slavepointer

    def menu_setup(self):
        self.menu = gtk.Menu()
        
        #natural scrolling
        self.menu_item_natural_scrolling = gtk.CheckMenuItem(_('Natural Scrolling'))
        if self.isreversed():
            self.menu_item_natural_scrolling.set_active (True)
        self.menu_item_natural_scrolling.connect ('activate', self.on_natural_scrolling_toggled)
        self.menu_item_natural_scrolling.show()

        #seperator 1
        self.menu_item_seperator1 = gtk.SeparatorMenuItem()
        self.menu_item_seperator1.show()

        #preferences
        self.menu_sub = gtk.Menu()
        self.menu_item_preferences = gtk.MenuItem (_('Preferences'))
        self.menu_item_start_at_login = gtk.CheckMenuItem (_('Start at login'))
        self.menu_sub.append (self.menu_item_start_at_login)
        self.menu_item_preferences.set_submenu (self.menu_sub)

        self.menu_item_start_at_login.show()
        self.menu_item_preferences.show()

        #about
        self.menu_item_about = gtk.MenuItem (_('About...'))
        self.menu_item_about.connect ('activate', self.on_about_clicked)
        self.menu_item_about.show()

        #seperator 2
        self.menu_item_seperator2 = gtk.SeparatorMenuItem()
        self.menu_item_seperator2.show()

        #quit
        self.menu_item_quit = gtk.MenuItem(_('Quit Natural Srcolling'))
        self.menu_item_quit.connect("activate", self.quit)
        self.menu_item_quit.show()

        #add items to menu
        self.menu.append(self.menu_item_natural_scrolling)
        self.menu.append(self.menu_item_seperator1)
        self.menu.append(self.menu_item_preferences)
        self.menu.append(self.menu_item_about)
        self.menu.append(self.menu_item_seperator2)
        self.menu.append(self.menu_item_quit)

    def main(self):
        self.check_scrolling()
        gtk.timeout_add(self.pingfrequency * 1000, self.check_scrolling)
        gtk.main()

    def quit(self, widget):
        sys.exit(0)
    
    def isreversed (self):
        inreverseorder = False 
        
        for id in self.mouseid:
            map = os.popen('xinput get-button-map %s' % id).read().strip()

            if '3 5 4' in map:
                inreverseorder = True
                break
        
        return inreverseorder


    def on_natural_scrolling_toggled (self, widget, data=None):
        map = ''

        for id in self.mouseid:
            map = os.popen ('xinput get-button-map %s' % id).read().strip()

            if self.isreversed():
                map = map.replace ('3 5 4', '3 4 5')
            else:
                map = map.replace ('3 4 5', '3 5 4')

            os.system ('xinput set-button-map %s %s' % (id, map))
    
    def on_about_clicked (self, widget, data=None):
        about = self.AboutDialog() # pylint: disable=E1102
        response = about.run()
        about.destroy()


    def check_scrolling (self):
        if self.isreversed():
            self.ind.set_status(appindicator.STATUS_ATTENTION)
        else:
            self.ind.set_status(appindicator.STATUS_ACTIVE)
       
        return True

