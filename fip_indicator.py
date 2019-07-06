#!/usr/bin/env python3
import subprocess
import os
import signal
import gi
import urllib.request, json 
import time, threading
import webbrowser
import re, textwrap
import sys
import yaml

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

class fipIndicator():
    def __init__(self):
        self.app = 'fipIndicator'
        self.indicator = AppIndicator3.Indicator.new(
            self.app, os.path.abspath('fip_100_color.png'),
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        with open(os.path.abspath('settings.yaml')) as settings_file:  
            settings = yaml.load(settings_file)

        self.station = settings['fip']['default_station']
        self.refresh_menu()

    def get_titles(self, data):
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

                self.t=threading.Timer(data['steps'][step]['end']-time.time(), self.refresh_menu)
                self.t=threading.Timer(120, self.refresh_menu)
                self.t.start()

            menuitem = Gtk.MenuItem.new_with_label(menustring)
            if 'path' in data['steps'][step] and data['steps'][step]['path']:
                menuitem.connect("activate", self.open_url, data['steps'][step]['path'])
            elif 'lienYoutube' in data['steps'][step] and data['steps'][step]['lienYoutube']:
                menuitem.connect("activate", self.open_url, data['steps'][step]['lienYoutube'])
                
            self.menu.append(menuitem)

    def create_menu(self, data):
        self.menu = Gtk.Menu()
        self.get_titles(data)

        sep = Gtk.SeparatorMenuItem()

        item_fip = Gtk.MenuItem.new_with_label('www.fip.fr')
        self.menu.append(sep)
        item_fip.connect("activate", self.open_url, 'https://www.fip.fr/')
        self.menu.append(item_fip)

        item_stations = Gtk.MenuItem.new_with_label('Stations')
        self.menu.append(item_stations)
        sub_menu = Gtk.Menu()

        # Stations submenu
        with open(os.path.abspath('fip_stations.yaml')) as stations_file:  
            data = yaml.load(stations_file)
            for station in data['stations']:
                station_menu = Gtk.MenuItem.new_with_label(station['name'])
                station_menu.connect("activate", self.set_station, station)
                sub_menu.append(station_menu)

        item_stations.set_submenu(sub_menu)

        item_quit = Gtk.MenuItem.new_with_label('Quit')
        item_quit.connect('activate', self.on_quit)
        self.menu.append(item_quit)

        self.menu.show_all()
        return self.menu

    def refresh_menu(self):
        with urllib.request.urlopen("https://www.fip.fr/livemeta/"+str(self.station)) as url:
            data = json.loads(url.read().decode())
        self.indicator.set_menu(self.create_menu(data))

    def open_url(self, widget, url):
        webbrowser.open_new(url)

    def set_station(self, widget, station):
        self.station = station["id"];
        self.refresh_menu()

    def on_quit(self, source):
        self.t.cancel()
        Gtk.main_quit()
        
fipIndicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
