from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import Gdk


class QuitDialog(Gtk.Dialog):

    def __init__(self):
        Gtk.Dialog.__init__(self)

        self.set_title(_("Quit?"))
        self.set_resizable(False)
        self.set_modal(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_QuitDialog_delete_event)

        self.dialog_vbox1 = Gtk.VBox()
        self.vbox.pack_start(self.dialog_vbox1, True, True, 0)

        self.vbox2 = Gtk.VBox()
        self.dialog_vbox1.pack_start(self.vbox2, False, False, 2)

        self.image6 = Gtk.Image.new_from_stock(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG)
        self.vbox2.pack_start(self.image6, False, False, 0)

        self.label5 = Gtk.Label(_("Do you really want to quit?"))
        self.label5.set_padding(8, 27)
        self.label5.set_justify(Gtk.Justification.CENTER)
        self.vbox2.pack_start(self.label5, False, False, 1)

        self.dialog_action_area1 = Gtk.HButtonBox()
        self.dialog_action_area1.set_layout(Gtk.ButtonBoxStyle.END)
        self.dialog_vbox1.pack_end(self.dialog_action_area1, False, False, 2)

        self.cancelbutton1 = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        ##self.cancelbutton1.connect("cancel", self.on_QuitDialog_delete_event)
        self.dialog_action_area1.add(self.cancelbutton1)

        self.okbutton1 = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        ##self.okbutton1.connect("clicked", self.on_dialog_okbutton1_clicked)
        self.dialog_action_area1.add(self.okbutton1)

        self.show_all()


class AboutDialog(Gtk.AboutDialog):

    def __init__(self):
        Gtk.AboutDialog.__init__(self)

        self.set_title(_("Abort Gvr"))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_AboutDialog_delete_event)

        self.dialog_vbox2 = Gtk.VBox()
        self.vbox.pack_start(self.dialog_vbox2, True, True, 0)

        self.vbox3 = Gtk.VBox()
        self.dialog_vbox2.pack_start(self.vbox3, True, True, 0)

        self.hbox13 = Gtk.HBox()
        self.vbox3.pack_start(self.hbox13, False, False, 0)

        self.image252 = Gtk.Image.new_from_file("gvrIcon-big.png")
        self.image252.set_padding(10, 8)
        self.hbox13.pack_start(self.image252, False, False, 0)

        self.image253 = Gtk.Image.new_from_file("Xo_s.png")
        self.image252.set_padding(10, 8)
        self.hbox13.pack_start(self.image252, False, False, 0)

        self.text_label = Gtk.Label()
        self.dialog_vbox2.pack_start(self.text_label, False, False, 3)

        self.dialog_action_area2 = Gtk.HButtonBox()
        self.dialog_action_area2.set_layout(Gtk.ButtonBoxStyle.END)
        self.dialog_vbox2.pack_end(self.dialog_action_area2, False, False, 0)

        self.okbutton2 = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        ##self.okbutton2.connect("clicked", self.on_AboutDialog_delete_event)
        self.dialog_action_area2.add(self.okbutton2)

        self.show_all()


class FileDialog(Gtk.FileChooserDialog):

    def __init__(self):
        Gtk.FileChooserDialog.__init__(self)

        self.set_border_width(5)
        self.set_title(_("Chose a file"))
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_FileDialog_delete_event)

        self.dialog_vbox3 = Gtk.VBox()
        self.dialog_vbox3.set_spacing(24)
        self.vbox.pack_start(self.dialog_vbox3, True, True, 0)

        self.dialog_action_area3 = Gtk.HButtonBox()
        self.dialog_action_area3.set_layout(Gtk.ButtonBoxStyle.END)
        self.vbox.pack_end(self.dialog_action_area3, False, False, 0)

        self.buttoncancel = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        ##self.buttoncancel.connect("clicked", self.on_FileDialog_delete_event)
        self.dialog_action_area3.add(self.buttoncancel)

        self.okbutton3 = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        self.dialog_action_area3.add(self.okbutton3)

        self.show_all()


class EditorWin(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_size_request(300, 500)
        self.set_title(_("Gvr - Editor"))
        ##self.connect("delete-event", self.on_TextEditorWin_delete_event)

        self.vbox4 = Gtk.VBox()
        self.add(self.vbox4)

        self.menubar2 = Gtk.MenuBar()
        self.vbox4.pack_start(self.menubar2, False, False, 0)

        self.menuitem5 = Gtk.MenuItem(_("_File"))
        self.menuitem5.set_use_underline(True)
        self.menubar2.append(self.menuitem5)

        self.menuitem5_menu = Gtk.Menu()
        self.menuitem5.set_submenu(self.menuitem5_menu)

        self.new1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_NEW)
        ##self.new1.connect("activate", self.on_new1_activate)
        self.menuitem5_menu.append(self.new1)

        self.open1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_OPEN)
        ##self.open1.connect("activate", self.on_open1_activate)
        self.menuitem5_menu.append(self.open1)

        self.save1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_SAVE)
        ##self.save1.connect("activate", self.on_save1_activate)
        self.menuitem5_menu.append(self.save1)

        self.save_as1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_SAVE_AS)
        ##self.save_as1.connect("activate", self.on_save_as1_activate)
        self.menuitem5_menu.append(self.save_as1)

        self.menuitem5_menu.append(Gtk.SeparatorMenuItem())

        self.print1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PRINT)
        ##self.print1.connect("activate", self.on_print1_activate)
        self.menuitem5_menu.append(self.print1)

        self.menuitem6 = Gtk.MenuItem(_("_Edit"))
        self.menuitem6.set_use_underline(True)
        self.menubar2.append(self.menuitem6)

        self.menuitem6_menu = Gtk.Menu()
        self.menuitem6.set_submenu(self.menuitem6_menu)

        self.cut1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_CUT)
        ##self.cut1.connect("activate", self.on_cut1_activate)
        self.menuitem6_menu.append(self.cut1)

        self.copy1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_COPY)
        ##self.copy1.connect("activate", self.on_copy1_activate)
        self.menuitem6_menu.append(self.copy1)

        self.paste1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_PASTE)
        ##self.paste1.connect("activate", self.on_paste1_activate)
        self.menuitem6_menu.append(self.paste1)

        self.delete1 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_CUT)
        ##self.delete1.connect("activate", self.on_delete1_activate)
        self.menuitem6_menu.append(self.delete1)

        self.scrolledwindow1 = Gtk.ScrolledWindow()
        self.scrolledwindow1.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow1.set_shadow_type(Gtk.ShadowType.IN)
        self.vbox4.pack_start(self.scrolledwindow1, True, True, 0)

        self.statusbar2 = Gtk.Statusbar()
        self.vbox4.pack_end(self.statusbar2, False, False, 2)

        self.show_all()


class SetLanguageDialog(Gtk.Dialog):

    def __init__(self):
        Gtk.Dialog.__init__(self)

        self.set_title(_("Set language"))
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_SetLanguageDialog_delete_event)

        self.dialog_vbox4 = Gtk.VBox()
        self.vbox.pack_start(self.dialog_vbox4, True, True, 0)

        self.vbox5 = Gtk.VBox()
        self.dialog_vbox4.pack_start(self.vbox5, True, True, 0)

        self.label7 = Gtk.Label(_("Change the language used\n(After you restart GvR)"))
        self.label7.set_padding(0, 4)
        self.vbox5.pack_start(self.label7, False, False, 0)

        model = Gtk.ListStore(str)
        model.append([_("Catalan")])
        model.append([_("Dutch")])
        model.append([_("English")])
        model.append([_("French")])
        model.append([_("Norwegian")])
        model.append([_("Romenian")])
        model.append([_("Spanish")])
        model.append([_("Italian")])

        self.comboboxentry_language = Gtk.ComboBox.new_with_model_and_entry(model)
        self.vbox5.pack_start(self.comboboxentry_language, False, False, 4)

        self.comboboxentry_entry1 = self.comboboxentry_language.get_children()[0]

        self.dialog_action_area4 = Gtk.HButtonBox()
        self.dialog_action_area4.set_layout(Gtk.ButtonBoxStyle.END)
        self.vbox.pack_end(self.dialog_action_area4, False, False, 0)

        self.cancelbutton2 = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        ##self.cancelbutton2.connect("clicked", self.on_SetLanguageDialog_delete_event)
        self.dialog_action_area4.add(self.cancelbutton2)

        self.okbutton4 = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        ##self.okbutton4.connect("clicked", self.on_okbutton3_clicked)
        self.dialog_action_area4.add(self.okbutton4)

        self.show_all()


class SetSpeedDialog(Gtk.Dialog):

    def __init__(self):
        Gtk.Dialog.__init__(self)

        self.set_title(_("Robot Speed"))
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_SetSpeedDialog_delete_event)

        self.dialog_vbox5 = Gtk.VBox()
        self.vbox.pack_start(self.dialog_vbox5, True, True, 0)

        self.vbox6 = Gtk.VBox()
        self.dialog_vbox5.pack_start(self.vbox6, True, True, 0)

        self.label8 = Gtk.Label(_("Set Robot Speed"))
        self.label8.set_padding(0, 8)
        self.vbox6.pack_start(self.label8, False, False, 0)

        model = Gtk.ListStore(str)
        model.append(["Instant"])
        model.append(["Fast"])
        model.append(["Medium"])
        model.append(["Slow"])

        self.comboboxentry_speed = Gtk.ComboBox.new_with_model_and_entry(model)
        self.vbox6.pack_start(self.comboboxentry_speed, False, False, 4)

        self.comboboxentry_entry2 = self.comboboxentry_speed.get_children()[0]

        self.dialog_action_area5 = Gtk.HButtonBox()
        self.dialog_action_area5.set_layout(Gtk.ButtonBoxStyle.END)
        self.vbox.pack_end(self.dialog_action_area5, False, False, 0)

        self.cancelbutton3 = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        ##self.cancelbutton3.connect("clicked", self.on_SetSpeedDialog_delete_event)
        self.dialog_action_area5.add(self.cancelbutton3)

        self.okbutton5 = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        ##self.okbutton5.connect("clicked", self.on_okbutton4_clicked)
        self.dialog_action_area5.add(self.okbutton5)

        self.show_all()


class SummaryDialog(Gtk.Dialog):

    def __init__(self):
        Gtk.Dialog.__init__(self)

        self.set_size_request(400, 400)
        self.set_title(_("Guido van Robot Programming Summary"))
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_SummaryDialog_delete_event)

        self.dialog_vbox6 = Gtk.VBox()
        self.vbox.pack_start(self.dialog_vbox6, True, True, 0)

        self.scrolledwindow3 = Gtk.ScrolledWindow()
        self.scrolledwindow3.set_border_width(4)
        self.scrolledwindow3.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow3.set_shadow_type(Gtk.ShadowType.IN)
        self.dialog_vbox6.pack_start(self.scrolledwindow3, True, True, 0)

        self.textview1 = Gtk.TextView()
        self.scrolledwindow3.add(self.textview1)

        self.hbuttonbox2 = Gtk.HButtonBox()
        self.hbuttonbox2.set_layout(Gtk.ButtonBoxStyle.END)
        self.vbox.pack_end(self.hbuttonbox2, False, False, 0)

        self.closebutton1 = Gtk.Button.new_from_stock(Gtk.STOCK_CLOSE)
        ##self.closebutton1.connect("clicked", on_SummaryDialog_delete_event)
        self.hbuttonbox2.add(self.closebutton1)

        self.show_all()


class RobotDialog(Gtk.Dialog):

    def __init__(self):
        Gtk.Dialog.__init__(self)

        self.set_size_request(450, 200)
        self.set_default_size(450, 200)
        self.set_title(_("Guido van Robot - Robot arguments"))
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        ##self.connect("delete-event", self.on_RobotDialog_delete_event)

        self.dialog_vbox7 = Gtk.VBox()
        self.vbox.pack_start(self.dialog_vbox7, True, True, 0)

        self.table1 = Gtk.Table(5, 2)
        self.table1.set_border_width(7)
        self.table1.set_row_spacing(8, 0)
        self.table1.set_homogeneous(True)
        self.dialog_vbox7.pack_start(self.table1, True, True, 0)

        self.entry_beepers = Gtk.Entry()
        self.entry_beepers.set_max_length(3)
        self.entry_beepers.set_invisible_char("*")
        self.table1.attach(self.entry_beepers, 1, 2, 4, 5)

        self.entry_dir = Gtk.Entry()
        self.entry_dir.set_max_length(1)
        self.entry_beepers.set_invisible_char("*")
        self.table1.attach(self.entry_dir, 1, 2, 3, 4)

        self.entry_y = Gtk.Entry()
        self.entry_y.set_max_length(2)
        self.entry_y.set_invisible_char("*")
        self.table1.attach(self.entry_y, 1, 2, 2, 3)

        self.entry_x = Gtk.Entry()
        self.entry_x.set_max_length(2)
        self.entry_x.set_invisible_char("*")
        self.table1.attach(self.entry_x, 1, 2, 1, 2)

        self.label14 = Gtk.Label(_("Robots position on the x-axes:"))
        self.label14.set_xalign(0)
        self.table1.attach(self.label14, 1, 2, 1, 1)

        self.label11 = Gtk.Label(_("Robots position on the y-axes:"))
        self.label11.set_xalign(0)
        self.table1.attach(self.label11, 2, 3, 1, 1)

        self.label13 = Gtk.Label(_("Direction robot is facing (N,E,S,W)"))
        self.label13.set_xalign(0)
        self.table1.attach(self.label13, 2, 3, 1, 1)

        self.label12 = Gtk.Label(_("Direction robot is facing (N,E,S,W)"))
        self.label12.set_xalign(0)
        self.table1.attach(self.label12, 4, 5, 1, 1)

        self.label9 = Gtk.Label()
        self.label9.set_markup("%s" % _("Alter the arguments for the 'robot' statement."))
        self.label9.set_xalign(0)
        self.table1.attach(self.label9, 2, 1, 1, 1)

        self.dialog_action_area7 = Gtk.HButtonBox()
        self.dialog_action_area7.set_layout(Gtk.ButtonBoxStyle.END)
        self.dialog_vbox7.pack_end(self.dialog_action_area7, False, False, 0)

        self.cancelbutton4 = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        ##self.cancelbutton4.connect("clicked", self.on_RobotDialog_delete_event)
        self.dialog_action_area7.add(self.cancelbutton4)

        self.okbutton6 = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        self.dialog_action_area7.add(self.okbutton6)

        self.show_all()


class window_main(Gtk.VBox):

    def __init__(self):
        Gtk.VBox.__init__(self)

        self.frame5 = Gtk.Frame()
        self.frame5.set_border_width(8)
        self.frame5.set_shadow_type(Gtk.ShadowType.NONE)
        self.frame5.props.label_xalign = 0
        self.add(self.frame5)

        self.alignment17 = Gtk.Alignment()
        self.frame5.add(self.alignment17)

        self.hpaned1 = Gtk.HPaned()
        self.alignment17.add(self.hpaned1)

        self.notebook1 = Gtk.Notebook()
        self.hpaned1.pack1(self.notebook1)

        self.frame4 = Gtk.Frame()
        self.frame4.set_size_request(400, 1)
        self.frame4.set_border_width(6)
        self.frame4.props.label_xalign = 0
        self.notebook1.append_page(self.frame4, Gtk.Label(_("Guido's World")))

        self.alignment11 = Gtk.Alignment()
        self.frame4.add(self.alignment11)

        self.vbox11 = Gtk.VBox()
        self.alignment11.add(self.vbox11)

        self.menubar7 = Gtk.MenuBar()
        self.vbox11.pack_start(self.menubar7, False, False, 0)

        self.menuitem31 = Gtk.MenuItem(_("GvR"))
        self.menubar7.append(self.menuitem31)

        self.menuitem31_menu = Gtk.Menu()
        self.menuitem31.set_submenu(self.menuitem31_menu)

        self.menuitem48 = Gtk.ImageMenuItem(_("Open worldbuilder"))
        self.menuitem48.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_LEAVE_FULLSCREEN, Gtk.IconSize.MENU))
        ##self.menuitem48.connect("activate", self.on_open_worldbuilder1_activate)
        self.menuitem31_menu.append(self.menuitem48)

        self.menuitem31_menu.append(Gtk.SeparatorMenuItem())

        self.imagemenuitem49 = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_QUIT)
        self.imagemenuitem49.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_LEAVE_FULLSCREEN, Gtk.IconSize.MENU))
        ##self.imagemenuitem49.connect("activate", self.on_quit1_activate)
        self.menuitem31_menu.append(self.imagemenuitem49)

        self.menuitem32 = Gtk.MenuItem(_("_Setup"))
        self.menuitem32.set_use_underline(True)
        self.menubar7.append(self.menuitem32)

        self.menuitem32_menu = Gtk.Menu()
        self.menuitem32.set_submenu(self.menuitem32_menu)

        self.imagemenuitem50 = Gtk.ImageMenuItem(_("Set speed..."))
        self.imagemenuitem50.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.MENU))
        ##self.imagemenuitem50.connect("activate", self.on_set_speed1_activate)
        self.menuitem32_menu.append(self.imagemenuitem50)

        self.imagemenuitem51 = Gtk.ImageMenuItem(_("Set language"))
        self.imagemenuitem51.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_SPELL_CHECK, Gtk.IconSize.MENU))
        ##self.imagemenuitem50.connect("activate", self.on_set_language1_activate)
        self.menuitem32_menu.append(self.imagemenuitem51)

        self.menuitem33 = Gtk.MenuItem(_("_Help"))
        self.menuitem33.set_use_underline(True)
        self.menubar7.append(self.menuitem33)

        self.menuitem33_menu = Gtk.Menu()
        self.menuitem33.set_submenu(self.menuitem33_menu)

        self.imagemenuitem52 = Gtk.ImageMenuItem(_("Gvr Lessons"))
        self.imagemenuitem52.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_DND_MULTIPLE, Gtk.IconSize.MENU))
        ##self.imagemenuitem52.connect("activate", self.on_gvr_lessons1_activate)
        self.menuitem33_menu.append(self.imagemenuitem52)

        self.imagemenuitem54 = Gtk.ImageMenuItem(_("GvR Worldbuilder"))
        self.imagemenuitem54.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_LEAVE_FULLSCREEN, Gtk.IconSize.MENU))
        ##self.imagemenuitem54.connect("activate", self.on_gvr_worldbuilder1_activate)
        self.menuitem33_menu.append(self.imagemenuitem54)

        self.menuitem33_menu.append(Gtk.SeparatorMenuItem())

        self.imagemenuitem55 = Gtk.ImageMenuItem(_("_About"))
        self.imagemenuitem55.set_use_underline(True)
        self.imagemenuitem55.set_image(Gtk.Image.new_from_stock(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.MENU))
        ##self.imagemenuitem55.connect("activate", self.on_about1_activate)
        self.menuitem33_menu.append(self.imagemenuitem55)

        self.frame6 = Gtk.Frame()
        self.frame6.set_border_width(2)
        self.frame6.set_label_align(0, 0)
        self.vbox11.pack_start(self.frame6, True, True, 0)

        self.alignment13 = Gtk.Alignment()
        self.alignment13.props.left_padding = 4
        self.alignment13.props.right_padding = 4
        self.frame6.add(self.alignment13)

        self.hbuttonbox1 = Gtk.HButtonBox()
        self.hbuttonbox1.set_layout(Gtk.ButtonBoxStyle.START)
        self.alignment13.add(self.hbuttonbox1)

        self.button_reload = Gtk.Button()
        ##self.button_reload.connect("clicked", self.on_button_reload)
        self.hbuttonbox1.add(self.button_reload)

        self.alignment14 = Gtk.Alignment()
        self.alignment14.props.xscale = 0
        self.alignment14.props.yscale = 0
        self.button_reload.add(self.alignment14)

        self.hbox9 = Gtk.HBox()
        self.hbox9.set_spacing(2)
        self.alignment14.add(self.hbox9)

        self.image235 = Gtk.Image.new_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.BUTTON)
        self.hbox9.pack_start(self.image235, False, False, 0)

        self.label21 = Gtk.Label(_("Reload"))
        self.hbox9.pack_start(self.label21, False, False, 0)

        self.button_step = Gtk.Button()
        ##self.button_step.connect("clicked", self.on_button_step)
        self.hbuttonbox1.add(self.button_step)

        self.alignment15 = Gtk.Alignment()
        self.alignment15.props.xscale = 0
        self.alignment15.props.yscale = 0
        self.button_step.add(self.alignment15)

        self.hbox10 = Gtk.HBox()
        self.hbox10.set_spacing(2)
        self.alignment15.add(self.hbox10)

        self.image236 = Gtk.Image.new_from_stock(Gtk.STOCK_REDO, Gtk.IconSize.BUTTON)
        self.hbox10.pack_start(self.image236, False, False, 0)

        self.label22 = Gtk.Label(_("Step"))
        self.hbox10.pack_start(self.label22, False, False, 0)

        self.button_execute = Gtk.Button()
        ##self.button_execute.connect("clicked", self.on_button_execute)
        self.hbuttonbox1.add(self.button_execute)

        self.alignment16 = Gtk.Alignment()
        self.alignment16.props.xscale = 0
        self.alignment16.props.yscale = 0
        self.button_execute.add(self.alignment16)

        self.hbox11 = Gtk.HBox()
        self.hbox11.set_spacing(2)
        self.alignment16.add(self.hbox11)

        self.image237 = Gtk.Image.new_from_stock(Gtk.STOCK_EXECUTE, Gtk.IconSize.BUTTON)
        self.hbox11.pack_start(self.image237, False, False, 0)

        self.label23 = Gtk.Label(_("Execute"))
        self.hbox11.pack_start(self.label23, False, False, 0)

        self.button_abort = Gtk.Button()
        ##self.button_abort.connect("clicked", self.on_button_abort)
        self.hbuttonbox1.add(self.button_abort)

        self.alignment1 = Gtk.Alignment()
        self.alignment1.props.xscale = 0
        self.alignment1.props.yscale = 0
        self.button_abort.add(self.alignment1)

        self.hbox12 = Gtk.HBox()
        self.hbox12.set_spacing(2)
        self.alignment1.add(self.hbox12)

        self.image238 = Gtk.Image.new_from_stock(Gtk.STOCK_CANCEL, Gtk.IconSize.BUTTON)
        self.hbox12.pack_start(self.image238, False, False, 0)

        self.label24 = Gtk.Label(_("Abort"))
        self.hbox12.pack_start(self.label24, False, False, 0)

        self.scrolledwindow8 = Gtk.ScrolledWindow()
        self.scrolledwindow8.set_size_request(400, 500)
        self.scrolledwindow8.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vbox11.pack_start(self.scrolledwindow8, False, False, 0)

        self.statusbar7 = Gtk.Statusbar()
        ##self.statusbar7.connect("text-pushed", self.on_statusbar1_text_pushed)
        ##self.statusbar7.connect("text-popped", self.on_statusbar1_text_popped)
        self.vbox11.pack_end(self.statusbar7, False, False, 0)

        self.label19 = Gtk.Label()
        self.label19.set_markup("<b>%s</b>" % _("Guido's World"))
        self.frame6.add(self.label19)

        self.eventboxlanguage = Gtk.EventBox()
        self.notebook1.append_page(self.eventboxlanguage, Gtk.Label(_("Language reference")))

        self.scrolledwindow9 = Gtk.ScrolledWindow()
        self.scrolledwindow9.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow9.set_shadow_type(Gtk.ShadowType.IN)
        self.eventboxlanguage.add(self.scrolledwindow9)

        self.textview_languagereference = Gtk.TextView()
        self.textview_languagereference.set_size_request(410, 1)
        self.textview_languagereference.set_border_width(8)
        self.textview_languagereference.set_editable(False)
        self.textview_languagereference.set_cursor_visible(False)
        self.scrolledwindow9.add(self.textview_languagereference)

        self.eventboxlessons = Gtk.EventBox()
        self.notebook1.append_page(self.eventboxlessons, Gtk.Label(_("Lessons")))

        self.eventboxintro = Gtk.EventBox()
        self.eventboxintro.set_border_width(4)
        self.notebook1.append_page(self.eventboxintro, Gtk.Label(_("Intro")))

        self.scrolledwindow10 = Gtk.ScrolledWindow()
        self.scrolledwindow10.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolledwindow10.set_shadow_type(Gtk.ShadowType.IN)
        self.eventboxintro.add(self.scrolledwindow10)

        self.textview_intro = Gtk.TextView()
        self.textview_intro.set_editable(False)
        self.textview_intro.set_cursor_visible(False)
        self.scrolledwindow10.add(self.textview_intro)

        self.notebook2 = Gtk.Notebook()
        self.hpaned1.pack2(self.notebook2)

        self.frame8 = Gtk.Frame()
        self.frame8.set_size_request(240, 1)
        self.frame8.set_border_width(1)
        self.frame8.props.label_xalign = 0
        self.notebook2.append_page(self.frame8, Gtk.Label(_("Code editor")))

        self.alignment19 = Gtk.Alignment()
        self.frame8.add(self.alignment19)

        self.frame7 = Gtk.Frame()
        self.frame7.set_size_request(120, 1)
        self.frame7.set_border_width(1)
        self.frame7.props.label_xalign = 0
        self.notebook2.append_page(self.frame7, Gtk.Label(_("World editor")))

        self.alignment18 = Gtk.Alignment()
        self.frame7.add(self.alignment18)

        self.show_all()

if __name__ == "__main__":
    QuitDialog()
    AboutDialog()
    FileDialog()
    EditorWin()
    SetLanguageDialog()
    SetSpeedDialog()
    SummaryDialog()
    RobotDialog()
    window_main()

