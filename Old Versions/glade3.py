#!/usr/bin/env python
import sys
try:
  import pygtk
  pygtk.require('2.0')
except:
  pass
try:
  import gtk
  import gtk.glade
except:
  print('GTK not available')
  sys.exit(1)

class Buglump:

  def __init__(self):
    self.gladefile = "GUITest.glade"
    self.builder = gtk.Builder()
    self.builder.add_from_file(self.gladefile)
    self.builder.connect_signals(self)
    self.window = self.builder.get_object("window1")
    self.aboutdialog = self.builder.get_object("aboutdialog")
    self.statusbar = self.builder.get_object("statusbar1")
    self.context_id = self.statusbar.get_context_id("status")
    self.window.show()
    self.status_count = 0

  def on_window1_destroy(self, object, data=None):
    print "quit with cancel"
    gtk.main_quit()

  def on_gtk_quit_activate(self, menuitem, data=None):
    print "quit from menu"
    gtk.main_quit()

  def on_push_status_activate(self, menuitem, data=None):
    self.status_count += 1
    self.statusbar.push(self.context_id, "Message number %s" % str(self.status_count))

  def on_pop_status_activate(self, menuitem, data=None):
    self.status_count -= 1
    self.statusbar.pop(self.context_id)

  def on_clear_status_activate(self, menuitem, data=None):
    while (self.status_count > 0):
      self.statusbar.pop(self.context_id)
      self.status_count -= 1

  def on_gtk_about_activate(self, menuitem, data=None):
    print "help about selected"
    self.response = self.aboutdialog.run()
    self.aboutdialog.hide()


if __name__ == "__main__":
  main = Buglump()
  gtk.main()
