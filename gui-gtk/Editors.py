# -*- coding: utf-8 -*-
# Copyright (c) 2006-2007 Stas Zykiewicz <stas.zytkiewicz@gmail.com>
#
#           Editors.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Wraps the gtksourceview2

import logging
module_logger = logging.getLogger("gvr.Editors")
import os
import utils

from gi.repository import Gtk
from gi.repository import GtkSource


class Editor:

    """Wraps a gtrksourceview widget and adds a few abstraction methods."""

    def __init__(self,parent,title=''):
        self.parent = parent
        self.logger = logging.getLogger("gvr.Editors.Editor")
        self.logger.debug("Using GtkSource version 3.0")
        # remove any children from previous sessions

        for child in self.parent.get_children():
            self.parent.remove(child)

        # Look for the locale to which the syntax highlighting should be set
        # We assume the locale is available, if not there won't be any higlighting.

        try:
            loc = utils.get_locale()[:2]

        except Exception,info:
            self.logger.exception("Error in checking locale")
            loc = ''

        if loc:
            mime = 'gvr_%s' % loc
        else:
            mime = 'gvr_en'

        self.srcbuffer = GtkSource.Buffer()
        self.srcview = GtkSource.View.new_with_buffer(self.srcbuffer)
        man = GtkSource.LanguageManager()
        self.logger.debug("set search path to %s" % utils.GTKSOURCEVIEWPATH)
        man.set_search_path([utils.GTKSOURCEVIEWPATH])

        langs = man.get_language_ids()
        self.srcbuffer.set_highlight_syntax(True)
        self.logger.debug("Found language files:%s" % langs)
        for id in langs:
            if id == mime:
                self.logger.debug("GtkSource buffer syntax higlight set to %s" % mime)
                self.srcbuffer.set_language(man.get_language(id))
                break

        self.srcview.set_tab_width(4)

        # some methods that are the same on version 1 and 2
        self.tag_h = self.srcbuffer.create_tag(background='lightblue')
        self.srcbuffer.set_max_undo_levels(10)
        self.srcview.set_show_line_numbers(True)
        self.srcview.set_insert_spaces_instead_of_tabs(True)
        #self.srcview.set_wrap_mode(gtk.WRAP_CHAR)
        self.parent.add(self.srcview)
        self.parent.show_all()

        self.old_start_iter = None

    def get_all_text(self):
        """Return all text from the widget"""
        startiter = self.srcbuffer.get_start_iter()
        enditer = self.srcbuffer.get_end_iter()
        txt = self.srcbuffer.get_text(startiter,enditer)
        if not txt:
            return []

        if '\n' in txt:
            txt = txt.split('\n')
        else:# assuming a line without a end of line
            txt = [txt]

        return txt

    def set_text(self,txt):
        """Load a text in the widget"""
        #print self.__class__,'set_text',txt
        try:
            txt = ''.join(txt)
            utxt = unicode(txt)
        except Exception,info:
            print "Failed to set text in source buffer"
            print info

            return

        self.srcbuffer.set_text(utxt)

    def set_highlight(self,line):
        """Highlight the line in the editor"""
        if self.old_start_iter:
            self.srcbuffer.remove_tag(self.tag_h,self.old_start_iter,self.old_end_iter)

        end_iter = self.srcbuffer.get_iter_at_line(line)
        end_iter.forward_to_line_end()  
        start_iter = self.srcbuffer.get_iter_at_line(line)
        self.srcbuffer.apply_tag(self.tag_h,start_iter,end_iter)
        self.old_start_iter,self.old_end_iter = start_iter,end_iter
    
    def reset_highlight(self):
        self.set_highlight(0)
        
    
            

