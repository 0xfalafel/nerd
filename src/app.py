#!/usr/bin/env python3
#coding: utf-8

import sys
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = Gtk.Settings.get_default()
        #settings.set_property('gtk-application-prefer-dark-theme', True)

        self.set_default_size(600, 400)
        self.set_title("")


        # Make initial titlebar invisible
        self.invisible_titlebar = Gtk.Grid(
            visible=False
        )
        self.set_titlebar(self.invisible_titlebar)


        # Pane
        self.paned = Gtk.Paned(
            orientation=Gtk.Orientation.HORIZONTAL
        )
        self.set_child(self.paned)

        # First pane
        self.first_pane = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )
        self.first_pane.set_size_request(250, -1)
        self.paned.set_start_child(self.first_pane)

        # First headerbar
        self.first_headerbar = Gtk.HeaderBar(
            show_title_buttons=False,
            css_classes=['view', 'headerbar']
        )
        self.first_headerbar.pack_start(Gtk.WindowControls())
        self.first_pane.append(self.first_headerbar)

        # Second pane
        self.second_pane = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.paned.set_end_child(self.second_pane)

        # Second Headerbar
        self.second_headerbar = Gtk.HeaderBar(
            show_title_buttons=False,
            css_classes=['sidebar', 'headerbar']
        )
        window_control = Gtk.WindowControls(
            side=Gtk.PackType.END
        )
        self.second_pane.append(self.second_headerbar)
        self.second_headerbar.pack_end(window_control)


        # TextView of First Pane
        self.left_scrolledwindow = Gtk.ScrolledWindow(
            vexpand=True,
            css_classes=['view', 'headerbar', 'input-text']
        )
        self.first_pane.append(self.left_scrolledwindow)

        self.textview = NerdText(
            margin_start = 20
        )
        self.left_scrolledwindow.set_child(self.textview)

        self.textbuffer = self.textview.get_buffer();


        # Result view of Second Pane
        self.right_scrolledwindow = Gtk.ScrolledWindow(
            vexpand=True
        )
        self.second_pane.append(self.right_scrolledwindow)

        self.resultview = Gtk.TextView(
            editable=False,
            #css_classes=['right_pane']
            css_classes=['sidebar']
        )
        self.right_scrolledwindow.set_child(self.resultview)



    def hello(self, button):
        print("Hi mom !")

class NerdText(Gtk.TextView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buffer = self.get_buffer()
        self.buffer.connect('changed', self.extact_text)


    def my_func(self, textbuf):
        help(textbuf)        
        text = textbuf.get_text(textbuf.get_iter_at_line(), textbuf.get_end_iter(), True)
        print(text)

    def extact_text(self, textbuf):
        lines = textbuf.get_line_count()
        extract = []

        for i in range(0, lines):
            _, start = textbuf.get_iter_at_line(i)
            not_last_line, end = textbuf.get_iter_at_line(i+1)

            if not not_last_line:
                _, end = textbuf.get_bounds()

            text = textbuf.get_text(start, end, True)
            extract.append(text)
            # print(f"{i}: {text}", end="")

        print(f"-------------------")

        for line in extract:
            print(line, end="")

        print("")

class MyApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


# Add our custom CSS
css_provider = Gtk.CssProvider()
css_provider.load_from_path('style.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# Run the app
app = MyApp(application_id="io.github.falafel.nerd")
app.run(sys.argv)
