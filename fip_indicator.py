#!/usr/bin/env python3
import subprocess
import os
import signal
import gi
import urllib.request, json 
import time
import threading
import webbrowser
import re
import textwrap
# import vlc

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

currpath = os.path.dirname(os.path.realpath(__file__))


# Roadmap
# If artist name is too long, cut after X chars /spaces
# If title name is too long, cut after X chars /spaces
# Show edition year 
# Link to album infos
# Disc Cover
# Play Station locally
# Launch Station on Alexa device
# Submit to last.fm

class fipIndicator():
    def __init__(self):
        self.app = 'fipIndicator'
        #iconpath = currpath+"/fip_100_color.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, os.path.abspath('fip_100_color.png'),
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.station = 7
        self.refresh_menu()

    def get_titles(self, data):
        #sep = Gtk.SeparatorMenuItem()
        for step in data['steps']:

            author=data['steps'][step]['authors']
            if len(author) > 35:
                author = textwrap.wrap(data['steps'][step]['authors'], 25)
                author = author[0]+" ..."

            title=data['steps'][step]['title']
            if len(title) > 35:
                title = textwrap.wrap(data['steps'][step]['title'], 25)
                title = title[0]+" ..."

            menustring=author+' - '+title

            nb_uppercases = len(re.findall(r'[A-Z]',menustring))
            if nb_uppercases > (len(menustring)/2):
                menustring = menustring.title()

            if data['steps'][step]['start'] <= time.time()  <= data['steps'][step]['end']:
                self.indicator.set_label(' '+menustring+' ', self.app)
                menustring = '-- '+menustring+' --'
                # TODO : Show Cover
            menuitem = Gtk.MenuItem(menustring)
            if 'path' in data['steps'][step] and data['steps'][step]['path']:
                menuitem.connect("activate", self.open_url, data['steps'][step]['path'])
            elif 'lienYoutube' in data['steps'][step] and data['steps'][step]['lienYoutube']:
                menuitem.connect("activate", self.open_url, data['steps'][step]['lienYoutube'])
            self.menu.append(menuitem)


    def create_menu(self, data):
        self.menu = Gtk.Menu()
        self.get_titles(data)

        sep = Gtk.SeparatorMenuItem()

        item_fip = Gtk.MenuItem('www.fip.fr')
        self.menu.append(sep)
        item_fip.connect("activate", self.open_url, 'https://www.fip.fr/')
        self.menu.append(item_fip)

        item_stations = Gtk.MenuItem('Stations')
        self.menu.append(item_stations)
        sub_menu = Gtk.Menu()

        # Stations submenu
        with open(currpath+'/fip_stations.json') as json_file:  
            data = json.load(json_file)
            for s in data['stations']:
                station_menu = Gtk.MenuItem(s['name'])
                station_menu.connect("activate", self.set_station, s)
                sub_menu.append(station_menu)

        item_stations.set_submenu(sub_menu)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.on_quit)
        self.menu.append(item_quit)

        self.menu.show_all()
        return self.menu

    def refresh_menu(self):
        threading.Timer(20.0, self.refresh_menu).start()
        with urllib.request.urlopen("https://www.fip.fr/livemeta/"+str(self.station)) as url:
            data = json.loads(url.read().decode())
        self.indicator.set_menu(self.create_menu(data))

    def open_url(self, widget, url):
        webbrowser.open_new(url)

    def set_station(self, widget, station):
        self.station = station["id"];
        self.refresh_menu()

    def on_quit(self, source):
        Gtk.main_quit()
        
fipIndicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()