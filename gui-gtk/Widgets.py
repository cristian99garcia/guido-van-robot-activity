# -*- coding: utf-8 -*-

# Copyright (c) 2006 Stas Zykiewicz <stas.zytkiewicz@gmail.com>
#
#           Widgets.py
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

# additional non-glade widgets and misc stuff
_WDEBUG = 0
import os
import sys
import logging
import gvr_gtk_glade

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
from gi.repository import GObject
from gi.repository import GdkPixbuf

from sugar3.graphics.toolbutton import ToolButton

app_name = "gvr_gtk"
import utils

from worldMap import lookup_dir_dict

glade_dir = utils.FRONTENDDIR


class WarningDialog(Gtk.MessageDialog):

    def __init__(self, parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.CLOSE, message_format='', txt=''):

        Gtk.MessageDialog.__init__(self,parent=parent, flags=flags, type=type, buttons=buttons, message_format=message_format)

        self.connect("response", self.response)
        self.set_markup('%s%s%s' % ('<b>',txt,'</b>'))
        self.show()

    def response(self,*args):
        """destroys itself on a respons, we don't care about the response value"""
        self.destroy()


class ErrorDialog(WarningDialog):

    def __init__(self, txt):
        WarningDialog.__init__(self, parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.CLOSE, message_format='', txt=txt)


class InfoDialog(WarningDialog):

    def __init__(self, txt):
        WarningDialog.__init__(self,parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.CLOSE, message_format='', txt=txt)


class YesNoDialog(Gtk.MessageDialog):

    def __init__(self, parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.YES_NO, message_format='', txt=''):
        Gtk.MessageDialog.__init__(self, parent=parent, flags=flags, type=type, buttons=buttons, message_format=message_format)

        #self.connect("response", self.response)
        self.set_markup('%s%s%s' % ('<b>', txt, '</b>'))
        self.show()


class BeeperDialog(YesNoDialog):

    def __init__(self, parent=None, flags=Gtk.DialogFlags.MODAL, type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.OK_CANCEL, message_format='', txt=''):
        YesNoDialog.__init__(self,parent=parent, flags=flags, type=type, buttons=buttons, message_format=message_format, txt=txt)

        hbox = Gtk.HBox(spacing=4)
        label = Gtk.Label(_("Number of beepers:"))
        self.entrybox = Gtk.Entry()
        self.entrybox.set_max_length(3)
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(self.entrybox, False, False, 0)
        self.vbox.pack_start(hbox, True, True, 0)
        self.vbox.show_all()

    def get_choice(self):
        choice = self.entrybox.get_text()
        try:
            beepers = int(choice)

        except ValueError,info:
            print info
            beepers = 0

        return beepers


# As a reminder:
# The toplevel window on the XO is always fullscreen with a size of 1200x900 
# and the canvas widget has a size of 638x737 (x,y)


class Canvas(Gtk.DrawingArea):

    """
    Wraps a Gtk.DrawingArea and a adds a few abstraction methods.
    Based on the example from the pygtk FAQ.
    """

    def __init__(self, parent=None):
        self.logger = logging.getLogger("gvr.Widgets.Canvas")
        self.logger.debug("start canvas creation")
        Gtk.DrawingArea.__init__(self)

        self.gvrparent = parent
        self.gc = None  # initialized in realize-event handler
        self.width  = 0 # updated in size-allocate handler
        self.height = 0 # idem
        self.connect('size-allocate', self._on_size_allocate)
        self.connect('draw',          self._on_expose_event)
        ##self.connect('realize',       self._on_realize)
        self._load_images()
        # image sizes
        self.spi_x = self.splash_pixbuf.get_width()
        self.spi_y = self.splash_pixbuf.get_height()
        
        # all guidos are the same size and square
        self.guido_x = self.robot_n_pixbuf.get_width()
        self.guido_y = self.guido_x
        # size of the matrix cells
        self.square = 40
        self.offset = (0,0)
        
        # 'stuff_to_draw' will hold references to the drawing methods.
        # They are set by the method draw_world and draw_splash.
        # The 'on_expose_event' callback just
        # calls all the methods that are in the list.
        # For example, when theres no world loaded the gvr splash screen
        # should be drawn and the list only holds '_draw_splash'.
        # When there's a world loaded the list could contain:
        # '_draw_empty_world','_draw_wal,sysls','_draw_beepers','_draw_robot'
        # The gui should call draw_world. The list
        # is parsed from item 0 upwards.
        self.stuff_to_draw = [self._draw_splash]
                
    def __repr__(self):
        return "Canvas"
        
    def _load_images(self):
        """Put loading in a seperate method which can be overridden by WBCanvas
        to load different images"""
        self.dot_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR, 'dot.png'))
        self.splash_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'gvr-splash.png'))
        self.robot_n_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_n.png'))
        self.robot_e_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_e.png'))
        self.robot_s_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_s.png'))
        self.robot_w_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_w.png'))

    def _on_realize(self, widget):
        ##cmap = widget.get_colormap()
        ##self.WHITE = cmap.alloc_color('white')
        ##self.BLACK = cmap.alloc_color('black')
        ##self.RED = cmap.alloc_color('red')
        ##self.BLUE = cmap.alloc_color('blue')
        ##self.gc = widget.get_window().new_gc()
        ##self.pangolayout = widget.create_pango_layout('')
        ##self.pangolayout_beeper = widget.create_pango_layout('')
        # create a font description
        ##font_desc = pango.FontDescription('Serif 8')
        # tell the layout which font description to use
        ##self.pangolayout.set_font_description(font_desc)
        # and one for the beepers

        ##if utils.platform == 'XO':
        ##    fn_size = '8'
        ##else:
        ##    fn_size = '12'

        ##font_desc = pango.FontDescription('Serif ' + fn_size)
        ##self.pangolayout_beeper.set_font_description(font_desc)

        return True
        
    def _on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height
        #print 'x,y', self.width,self.height
        self.screenX = self.width/self.square
        self.screenY = self.height/self.square
        return True
        
    def _on_expose_event(self, widget, context):
        # This is where the drawing takes place
        for func in self.stuff_to_draw:
            apply(func,(widget,))

        return True

    def _fill_background(self, widget, col=''):
        ##if not col:
        ##    col = self.WHITE

        ##self.gc.set_foreground(col)
        filled = 1
        ##widget.window.draw_rectangle(self.gc, filled, 0, 0, self.width, self.height)

    def _draw_splash(self,widget):
        """Draws the GvR splash screen onto the canvas."""
        self.world_size = (10,10)
        x = self.world_size[0] * self.square
        y = self.world_size[1] * self.square
        self.set_size_request(x,y)
        self._fill_background(widget)
        ##widget.get_window().draw_pixbuf(self.gc, self.splash_pixbuf, 0, 0, 8, 8, -1, -1)

    # these methods are used to blit the world for the first time
    def _reset_offset(self):
        self.offset = (0,0)
        self.screenX = self.width/self.square
        self.screenY = self.height/self.square
    
    def _draw_empty_world(self, widget):
        if repr(self) == "WBCanvas":
            col = self.BLUE
        else:
            col = self.RED

        #self.logger.debug("_draw_empty_world called")
        self._fill_background(widget)
        
        ##self.gc.set_line_attributes(line_width=2,
        ##                            line_style=gtk.gdk.LINE_SOLID,
        ##                            cap_style=gtk.gdk.CAP_NOT_LAST,
        ##                            join_style=gtk.gdk.JOIN_MITER)

        # create a font description
        font_desc = Pango.FontDescription('Serif 8')
        # tell the layout which font description to use
        ##self.pangolayout.set_font_description(font_desc)
        # set numbers and outer walls
        ##y = self.height - self.square + 4
        ##step = self.square
        # self.orig_x, self.orig_y are the coords of the upper left corner of
        # guido at the first square in the matrix. 
        # Used as starting point to calculate the robots and beepers position.
        ##self.orig_x, self.orig_y = step+9,y-self.square+6
        #print self.orig_x,self.orig_y
        #widget.window.draw_pixbuf(self.gc,self.dot_pixbuf,0,0,self.orig_x,self.orig_y,-1,-1)
        ##end = self.width/self.square
        # draw horizontal outer red wall
        ##self.gc.set_foreground(col)
        ##widget.window.draw_line(self.gc,step+4,y,self.width,y)
        ##step = self.height- self.square*2
        # draw vertical outer red wall
        ##self.gc.set_foreground(col)
        ##widget.window.draw_line(self.gc,self.square+4,step+self.square+4,self.square+4,0)
        #draw vertical labels
        ##self.gc.set_foreground(self.BLACK)
        ##x_range_dots = range(int(self.square*2),self.width,self.square)
        ##for y in range(1,self.height):
        ##    # draw dots on x-axes
        ##    for x in x_range_dots:
        ##        widget.window.draw_pixbuf(self.gc,self.dot_pixbuf,0,0,x,step,-1,-1)
        ##    step -= self.square
        return True
    
    def _draw_labels(self,widget=None):
        # used to determine the amount the world must shift as the robot moves
        # off screen
        ##offset_x,offset_y = self.offset
        # create a font description
        ##font_desc = pango.FontDescription('Serif 8')
        # tell the layout which font description to use
        ##self.pangolayout.set_font_description(font_desc)
        # draw horizontal labels
        ##self.gc.set_foreground(self.BLACK)
        ##end = self.width/self.square
        ##y = self.height - self.square + 8
        ##step = self.square
        ##for x in range(1+offset_x,end+offset_x+1):
        ##    self.pangolayout.set_text('%d' % x)
        ##    self.window.draw_layout(self.gc,
        ##                        step, y,
        ##                        self.pangolayout)
        ##    step += self.square
        # vertical labels
        ##step = self.height- self.square*2
        ##for y in range(1+offset_y,self.height+offset_y):
        ##    self.pangolayout.set_text('%d' % y)
        ##    self.window.draw_layout(self.gc,
        ##                        self.square/2, step+self.square/2,
        ##                        self.pangolayout)
        ##    step -= self.square
        pass

    def _draw_walls(self,widget):
        #self.logger.debug("_draw_walls called")
        ##self.gc.set_foreground(self.RED)
        ##self.gc.line_width = 3
        ##walls = self.world.get_walls_position()
        # used to determine the amount the world must shift as the robot moves
        # off screen
        ##offset_x,offset_y = self.offset
        ##for x,y in walls['west_wall']:
        ##    x = x * self.square + 4
        ##    y = self.height - self.square - y*self.square + 8
        ##    widget.window.draw_line(self.gc,x,y,x,y+(self.square-8))
        ##for x,y in walls['south_wall']:
        ##    x = x * self.square + 8
        ##    y = self.height - y*self.square + 4
        ##    widget.window.draw_line(self.gc,x,y,x+(self.square-8),y)
        pass

    # Used by the worldbuilder
    def _remove_wall(self,d,x,y):
        ##self.gc.set_foreground(self.WHITE)
        ##self.gc.line_width = 3
        ##if d == 'W':
        ##    x = x * self.square + 4
        ##    y = self.height - self.square - y*self.square + 8
        ##    self.window.draw_line(self.gc,x,y,x,y+(self.square-8))
        ##elif d == 'S':
        ##    x = x * self.square + 8
        ##    y = self.height - y*self.square + 4
        ##    self.window.draw_line(self.gc,x,y,x+(self.square-8),y)
        pass

    def _draw_beepers(self,widget):
        #self.logger.debug("_draw_beepers called")
        ##self.gc.set_foreground(self.BLUE)
        ##self.gc.line_width = 4
        ##for key,value in self.world.get_beepers().items():
        ##    self._draw_beeper(key,value)
        ##self.gc.line_width = 2
        #self.queue_draw()
        pass

    def _draw_beeper(self,pos,value):
        #self.logger.debug("_draw_beeper called")
        ##pos_x = self.orig_x + self.square*(pos[0]-1)
        ##pos_y = self.orig_y - self.square*(pos[1]-1)
        # used to determine the amount the world must shift as the robot moves
        # off screen
        ##offset_x,offset_y = self.offset

        ##self.window.draw_arc(self.gc,False,pos_x+2,pos_y+2,22,24,0,360*64)

        ##self.pangolayout_beeper.set_text('%d' % value)
        ##if value < 10:
        ##    pos_x += 8
        ##else:
        ##    pos_x += 4
        ##self.window.draw_layout(self.gc,
        ##                        pos_x,pos_y+4,
        ##                        self.pangolayout_beeper)
        pass

    def _draw_robot(self,widget):
        #self.logger.debug("_draw_robot called")
        ##pos = self.world.get_robots_position()
        ##dir = self.world.get_robots_direction()
##        # used to determine the amount the world must shift as the robot moves
##        # off screen
##        offset_x,offset_y = self.offset
        ##pos_x = self.orig_x + self.square*(pos[0]-1)
        ##pos_y = self.orig_y - self.square*(pos[1]-1)
        ##pixbuf = self._get_direction_pixbuf()
        ##widget.window.draw_pixbuf(self.gc,pixbuf,0,0,pos_x,pos_y,-1,-1)
        pass

    def _get_direction_pixbuf(self):
        return {'E':self.robot_e_pixbuf,'W':self.robot_w_pixbuf,
                'N':self.robot_n_pixbuf,'S':self.robot_s_pixbuf} \
                    [self.world.get_robots_direction()]

    # abstraction methods called by the parent
    def draw_splash(self):
        self.stuff_to_draw = [self._draw_splash]
        self.queue_draw()

    def draw_world(self,world):
        """Draws the complete world represented in @world"""
        self.world = world
        self.stuff_to_draw = [self._draw_empty_world,
                              self._draw_labels,
                              self._draw_walls,
                              self._draw_robot,
                              self._draw_beepers]

        self.queue_draw()

########################## work in progress
    def draw_scrolling_world(self,offset):
        self.logger.debug("draw_scrolling_world called")
        self.stuff_to_draw = [self._draw_empty_world,\
                              self._draw_walls,\
                              self._draw_beepers,\
                              self._draw_labels]

        self.queue_draw()

#########################################################
    def draw_robot(self,obj,oldcoords):
        """Draws the robot and clears the old position of the robot.
        This is more efficient then redraw the whole world every time."""
        #self.logger.debug("draw_robot called")
        
        # we don't queue the drawing as the robot should move as fast as the user
        # intended, or the hardware allow
        pos = self.world.get_robots_position()
        dir = self.world.get_robots_direction()
        # we don't use a function for calculating the positions because
        # of the overhead of function calling. Speed is important in this case.
        pos_x = self.orig_x + self.square*(pos[0] + self.offset[0] - 1)
        pos_y = self.orig_y - self.square*(pos[1] - self.offset[1] - 1)
############### Scrolling is work in progress
        #print 
        #print 'draw_robot',pos,oldcoords
        scrolling, self.offset = self.world.newOffset(self.offset, (self.screenX,self.screenY))
        
        #print 'scrolling',scrolling,'self.offset',self.offset
        if scrolling:
            self.screenX += self.offset[0]
            self.screenY += self.offset[1]
            self.draw_scrolling_world(self.offset)
            # recalculate the robot's position
##            pos_x = self.orig_x + self.square*(pos[0] + self.offset[0] - 1)
##            pos_y = self.orig_y - self.square*(pos[1] - self.offset[1] - 1)
            
###########################################
        pixbuf = self._get_direction_pixbuf()
        self.gc.set_foreground(self.WHITE)
        if oldcoords:
            y = self.orig_y - self.square*(oldcoords[1]- self.offset[1] -1)
            x = self.orig_x + self.square*(oldcoords[0]+ self.offset[0] -1)
            self.window.draw_rectangle(self.gc,True,x,y,
                                    self.guido_x,self.guido_y)
            beepersdict = self.world.get_beepers()
            if beepersdict.has_key(pos):
                self.draw_beepers(None)
        # make sure all the previous events are processed before drawing the robot
        #while gtk.events_pending(): gtk.main_iteration()
        self.window.draw_pixbuf(self.gc, pixbuf, 0, 0, pos_x, pos_y, -1, -1)
        ##self.queue_draw()
        
    def draw_beeper(self,pos,value):
        """Draws the beepers and clears the old positions of the beepers.
        This is more efficient then redraw the whole world every time."""
        # XXX beepers are only picked up (cleared) when guido is on top
        #print pos,value
        #self.logger.debug("draw_beeper called")
        self._draw_beeper(pos,value)
        
    def draw_beepers(self,obj):
        #self.logger.debug("draw_beepers called")
        self._draw_beepers(None)


class WBCanvas(Canvas):
    """Canvas used for the worldbuilder.
    It extends the canvas object used by the GUI.
    """
    def __init__(self,parent=None,wcode=[]):
        Canvas.__init__(self,parent=parent)
        if wcode:
            # code comes from a editor widget and lacks \n tokens
            # we need those when we procces them in a worldbuilder.
            n_wcode = []
            for line in wcode:
                n_wcode.append(line+'\n')
            wcode = n_wcode
        self.wcode = wcode
        # connect mouse events 
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.POINTER_MOTION_MASK)
        self.connect('button-press-event', self.on_button_press_event_cb)  
        
        # grab the focus needed to receive the key events.
        self.grab_focus()
        
    def __repr__(self):
        return "WBCanvas"
        
    def _load_images(self):
        """Override the Canvas._load_images method to provide different
        world dots."""
        self.dot_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'dot_wb.png'))
        # The rest is the same
        self.splash_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'gvr-splash.png'))
        self.robot_n_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_n.png'))
        self.robot_e_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_e.png'))
        self.robot_s_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_s.png'))
        self.robot_w_pixbuf = GdkPixbuf.Pixbuf.new_from_file(os.path.join(utils.PIXMAPSDIR,'guido_w.png'))

    def _calculate_position(self,mx,my):
        """Turn mouse positions into grid positions.
        x,y is the gvr robot position.
        xx,yy are the remainders.
        Remaiders are used to determine walls orientation."""
        # adjustments to get it pixel perfect.
        height = self.height + 4
        mx -= 4
        x = int(mx) / self.square
        rx = max(1,int(mx) % self.square)
        y = (height - int(my)) / self.square
        ry = max(1,(height - int(my)) % self.square)

        if _WDEBUG:
            print "mouse x,y",mx,my
            print "grid x,rx,y,ry",x,rx,y,ry

        return (x,rx,y,ry)

    def on_button_press_event_cb(self,widget, event):
        # add the wall to the editor and worldobject then call draw_wall
        # which uses the world object.
        wline, bline = '', ''
        if event.button == 1:
            # valid is set hen we have a orientation and it's checked after 
            # remainder checking
            valid = False
            x, rx, y, ry = self._calculate_position(event.x,event.y)
            if x < 1 or y < 1:
                return

            # first set the square we are in
            wline = "%s " % _('wall')
            # now we check the remainders to determine the walls orientation
            # first we look for x
            if 30 <= rx <= 39:
                wline += "%s %s %s\n" % (x,y,_('E'))
                valid = True

            elif 1 <= rx <= 10 and x > 1:
               wline += "%s %s %s\n" % (x-1,y,_('E'))
               valid = True

            # now for y
            elif 30 <= ry <= 39 :
                wline += "%s %s %s\n" % (x,y,_('N'))
                valid = True

            elif 1 <= ry <= 10 and y > 1:
                wline += "%s %s %s\n" % (x,y-1,_('N'))
                valid = True

            if not valid:
                return True

            if _WDEBUG:
                print wline            
            
        elif event.button == 2:
            # As it's mandatory that the first line is the robot statement
            # we assume the first line is the one to change.
            line = self.wcode[0].split(' ')
            if not _('robot') in line[0]:
                print "no robot statement found in the first line"
                return True
                
            dlg = RobotDialog()
            dlg.entry_x.set_text(line[1])
            dlg.entry_y.set_text(line[2])
            dlg.entry_dir.set_text(line[3])
            dlg.entry_beepers.set_text(line[4][:-1])# loose the EOL
            response = dlg.RobotDialog.run()
            
            if response == Gtk.ResponseType.OK:
                choice = dlg.get_choice()
                dlg.RobotDialog.destroy()

            else:
                dlg.RobotDialog.destroy()
                return True
            
            line[1] = choice[0]
            line[2] = choice[1]
            line[3] = choice[2]
            line[4] = choice[3]
            self.wcode[0]=' '.join(line)+'\n'
            self.gvrparent.world_editor.editor.set_text(self.wcode)
            self.gvrparent.on_button_reload()

            return True
            
        elif event.button == 3:
            x,xx,y,yy = self._calculate_position(event.x,event.y)
            if x < 1 or y < 1:
                return True
            # placeholder: check code for beepers on this position
            # and fill the dialog if true
            #print self.wcode
            dlg = BeeperDialog(txt=_("Please give the number of beepers\nto place on %d,%d") % (x,y))
            beepersline = '%s %s %s' % (_('beepers'),x,y)
            for line in self.wcode:
                if line.find(beepersline) != -1:
                    self.wcode.remove(line)
                    dlg.entrybox.set_text(line.split(' ')[3][:-1])
                    break
            response = dlg.run()
            if response == Gtk.ResponseType.OK:
                num_beepers = dlg.get_choice()
                if not num_beepers:
                    dlg.destroy()
                    return True
                bline = "%s %d %d %d\n" % (_('beepers'),x,y,num_beepers)
            dlg.destroy()
        # code used by button 1 and 3    
        wcode = filter(None,[wline,bline])
        if wcode:
##            self.stuff_to_draw = [self._draw_empty_world,
##                                self._draw_robot,
##                                self._draw_beepers,
##                                self._draw_labels,
##                                self._draw_walls]
            #print wcode
            if wcode[0] in self.wcode:
                #print "double:", wcode[0]
                self.wcode.remove(wcode[0])
            else:                
                self.wcode = self.wcode + wcode
            self.gvrparent.world_editor.editor.set_text(self.wcode)
            if event.button == 1:
                # t isn't used
                t,x,y,d = wline.split(' ')
                result = self.world.setWall_wb(x,y,lookup_dir_dict[d[:-1]])
                #print 'result',result
                if result[2] == 0:
                    # remove wall
                    self._remove_wall(result[0],result[1][0],result[1][1])
                else:
                    self._draw_walls(self)
            else:
                self.gvrparent.on_button_reload()
        return True
        
# setup the timer object the model can use
# The timer must provide the following methods:
# start, stop, set_func and set_interval
# see the methods for more info
class Timer:
    def __init__(self):
        """The timer register a function in the atexit module to cleanup any
        threads still running when the main application exits.
        Be aware that if your application doesn't exit in a 'normal' way the 
        atexit function might not work. (not normal ways are exceptions that are
        not cached by your app and terminates the program.) """       
        self.timer_id = None
        import atexit
        atexit.register(self.stop)
    def wakeup(self):
        """This is the actual 'worker' function."""
        if self.timer_id:
            apply(self.func)

            return True # run again after interval

        return False # stop running again

    # mandatory methods for any timer object
    def start(self):
        """Start the gtk timer"""
        print "Starting timer..."
        self.timer_id = GObject.timeout_add(self.interval, self.wakeup)

    def stop(self):
        """Stop the gtk timer"""
        #print "Stopping timer...",
        try:
            GObject.source_remove(self.timer_id)
            self.timer_id = None

        except:
            pass

    def set_func(self,func):
        """This will set the function that needs to be called by the timer.
        Because this timer object is passed to the gvr model by the controller
        we let the model set the function."""
        self.func = func

    def set_interval(self,interval):
        """Set the interval by which the function should be called. Like the
        set_func method, we don't know the interval when we pass this object"""
        self.interval = interval 


class RobotDialog(gvr_gtk_glade.RobotDialog):

    def __init__(self):
        gvr_gtk_glade.RobotDialog.__init__(self)

    def new(self):
        self.connect("delete-event", self.on_RobotDialog_delete_event)
        self.cancelbutton4.connect("clicked", self.on_RobotDialog_delete_event)
    
    def get_choice(self):
        return (self.entry_x.get_text(),
                self.entry_y.get_text(),
                self.entry_dir.get_text(),
                self.entry_beepers.get_text())

    def on_RobotDialog_delete_event(self, widget, *args):
        self.RobotDialog.destroy()
    

class StatusBar:

    def __init__(self, glade_obj):
        self.logger = logging.getLogger("gvr.Widgets.StatusBar")
        self.statusbar = glade_obj
        self.context_id = self.statusbar.get_context_id('gvr_gtk')
        self.barmesg = _("Robots position is %s %s %s and carrying %s beepers")
        self.beep = 0
        self.pos = ((1,1),'N')
        self.data = [self.pos[0][0],self.pos[0][1],self.pos[1],self.beep]
    
    def update_robotposition(self,pos):
        self.data[0],self.data[1],self.data[2] = pos[0][0],pos[0][1],pos[1]
        #First we remove any message from the stack
        self.statusbar.pop(self.context_id)
        # Then we push a new one which is also displayed
        #self.logger.debug("statusbar update_robotposition %s" % self.data)
        self.statusbar.push(self.context_id,self.barmesg % tuple(self.data))
        
    def update_robotbeepers(self,beep):
        self.data[3] = beep
        self.statusbar.pop(self.context_id)
        #self.logger.debug("statusbar update_robotbeepers %s" % self.data)
        self.statusbar.push(self.context_id,self.barmesg % tuple(self.data))
    
    def set_text(self,text):
        self.statusbar.pop(self.context_id)
        #self.logger.debug("statusbar set_text: %s" % text)
        self.statusbar.push(self.context_id,text)
    
    def clear(self):
        self.statusbar.pop(self.context_id)


class WebToolbar(Gtk.Toolbar):

    def __init__(self,browser):
        self.logger = logging.getLogger("gvr.Widgets.WebToolbar")

        Gtk.Toolbar.__init__(self)
        self._browser = browser
        
        self._back = ToolButton('go-previous')                           
        self._back.set_tooltip(_('Go back one page'))                                       
        self._back.connect('clicked', self._go_back_cb)                         
        self.insert(self._back, -1)                                             
        self._back.show() 
        
        self._forw = ToolButton('go-next')                           
        self._forw.set_tooltip(_('Go one page forward'))                                       
        self._forw.connect('clicked', self._go_forward_cb)                         
        self.insert(self._forw, -1)                                             
        self._forw.show() 
    
    def _go_forward_cb(self, button):
        if self._browser.can_go_forward():
            self._browser.go_forward()

    def _go_back_cb(self, button):
        if self._browser.can_go_back():
            self._browser.go_back()


def get_active_text(combobox):
    """Unfortunately, the GTK+ developers did not provide a convenience method
    to retrieve the active text. That would seem to be a useful method.
    You'll have to create your own."""
    model = combobox.get_model()
    active = combobox.get_active()
    if active < 0:
        return None

    return model[active][0]

