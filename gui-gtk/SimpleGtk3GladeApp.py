"""
 SimpleGladeApp.py
 Module that provides an object oriented abstraction to pygtk and libglade.
 Copyright (C) 2004 Sandino Flores Moreno
"""

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import logging
import os
import sys
import re
import tokenize
import weakref
import inspect
import __builtin__

import gvr_gtk_glade

#this is needed for py2exe
if sys.platform == 'win32':
    #win32 platform, add the "lib" folder to the system path
    os.environ['PATH'] += ";lib;"

from gi.repository import Gtk

module_logger = logging.getLogger("gvr.SimpleGladeApp")


def bindtextdomain(app_name, lang='',locale_dir=None):
    pass


class SimpleGladeApp:

    def __init__(self, root=None, domain=None, **kwargs):

        """
        Load a glade file specified by glade_filename, using root as
        root widget and domain as the domain for translations.

        If it receives extra named arguments (argname=value), then they are used
        as attributes of the instance.

        path:
                path to a glade filename.
                If glade_filename cannot be found, then it will be searched in the
                same directory of the program (sys.argv[0])

        root:
                the name of the widget that is the root of the user interface,
                usually a window or dialog (a top level widget).
                If None or ommited, the full user interface is loaded.

        domain:
                A domain to use for loading translations.
                If None or ommited, no translation is loaded.

        **kwargs:
                a dictionary representing the named extra arguments.
                It is useful to set attributes of new instances, for example:
                        glade_app = SimpleGladeApp("ui.glade", foo="some value", bar="another value")
                sets two attributes (foo and bar) to glade_app.
        """

        for key, value in kwargs.items():
            try:
                setattr(self, key, weakref.proxy(value))

            except TypeError:
                setattr(self, key, value)

        if root:
            self.main_widget = eval("gvr_gtk_glade.%s" % root)

        else:
            self.main_widget = None

        ##self.add_callbacks(self)
        self.new()

    def __repr__(self):
        class_name = self.__class__.__name__
        if self.main_widget:
            root = self.main_widget.get_name()
            repr = '%s(path="%s", root="%s")' % (class_name, root)

        else:
            repr = '%s(path="%s")' % (class_name)

        return repr

    def new(self):
        """
        Method called when the user interface is loaded and ready to be used.
        At this moment, the widgets are loaded and can be refered as self.widget_name
        """
        pass

    def add_callbacks(self, callbacks_proxy):
        """
        It uses the methods of callbacks_proxy as callbacks.
        The callbacks are specified by using:
                Properties window -> Signals tab
                in glade-2 (or any other gui designer like gazpacho).

        Methods of classes inheriting from SimpleGladeApp are used as
        callbacks automatically.

        callbacks_proxy:
                an instance with methods as code of callbacks.
                It means it has methods like on_button1_clicked, on_entry1_activate, etc.
        """
        ##self.glade.signal_autoconnect(callbacks_proxy)

    def custom_handler(self, glade, function_name, widget_name, str1, str2, int1, int2):
        """
        Generic handler for creating custom widgets, internally used to
        enable custom widgets (custom widgets of glade).

        The custom widgets have a creation function specified in design time.
        Those creation functions are always called with str1,str2,int1,int2 as
        arguments, that are values specified in design time.

        Methods of classes inheriting from SimpleGladeApp are used as
        creation functions automatically.

        If a custom widget has create_foo as creation function, then the a
        method named create_foo is called with str1,str2,int1,int2 as arguments.
        """
        try:
            handler = getattr(self, function_name)
            return handler(str1, str2, int1, int2)

        except AttributeError:
            return None

    def gtk_widget_show(self, widget, *args):
        """
        Predefined callback.
        The widget is showed.
        Equivalent to widget.show()
        """
        widget.show()

    def gtk_widget_hide(self, widget, *args):
        """
        Predefined callback.
        The widget is hidden.
        Equivalent to widget.hide()
        """
        widget.hide()

    def gtk_widget_grab_focus(self, widget, *args):
        """
        Predefined callback.
        The widget grabs the focus.
        Equivalent to widget.grab_focus()
        """
        widget.grab_focus()

    def gtk_widget_destroy(self, widget, *args):
        """
        Predefined callback.
        The widget is destroyed.
        Equivalent to widget.destroy()
        """
        widget.destroy()

    def gtk_window_activate_default(self, window, *args):
        """
        Predefined callback.
        The default widget of the window is activated.
        Equivalent to window.activate_default()
        """
        widget.activate_default()

    def gtk_true(self, *args):
        """
        Predefined callback.
        Equivalent to return True in a callback.
        Useful for stopping propagation of signals.
        """
        return True

    def gtk_false(self, *args):
        """
        Predefined callback.
        Equivalent to return False in a callback.
        """
        return False

    def gtk_main_quit(self, *args):
        """
        Predefined callback.
        Equivalent to Gtk.main_quit()
        """
        Gtk.main_quit()

    def main(self):
        """
        Starts the main loop of processing events.
        The default implementation calls Gtk.main()

        Useful for applications that needs a non gtk main loop.
        For example, applications based on gstreamer needs to override
        this method with gst.main()

        Do not directly call this method in your programs.
        Use the method run() instead.
        """
        Gtk.main()

    def quit(self):
        """
        Quit processing events.
        The default implementation calls Gtk.main_quit()

        Useful for applications that needs a non gtk main loop.
        For example, applications based on gstreamer needs to override
        this method with gst.main_quit()
        """
        Gtk.main_quit()

    def run(self):
        """
        Starts the main loop of processing events checking for Control-C.

        The default implementation checks wheter a Control-C is pressed,
        then calls on_keyboard_interrupt().

        Use this method for starting programs.
        """
        try:
            self.main()

        except KeyboardInterrupt:
            self.on_keyboard_interrupt()

    def on_keyboard_interrupt(self):
        """
        This method is called by the default implementation of run()
        after a program is finished by pressing Control-C.
        """
        pass

