#!/usr/bin/env python
import gtk

class BugLump:
    def on_window1_destroy (self, object, data = None):
	print "quit with cancel"
	gtk.main_quit()
    def on_gtk_quit_activate(self, menuitem, data=None):
	print "quit from menu"
	gtk.main_quit()
    def on_gtk_about_activate(self, menuitem, data=None):
	print "help about selected"
	self.response = self.aboutdialog.run()
	self.aboutdialog.hide()
    def __init__(self):
        self.gladefile = "GUITest.glade" # store the file name
	self.builder = gtk.Builder() # create an instance of the gtk.Builder
	self.builder.add_from_file(self.gladefile) # add the xml file to the Builder
	self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
	self.aboutdialog = self.builder.get_object("aboutdialog1")
	self.statusbar = self.builder.get_object("statusbar1")
	self.entry2 = self.builder.get_object("entry2")
	#self.entry2.set_text("Hello")
	#self.entry2.set_editable(True)
	self.context_id = self.statusbar.get_context_id("status")
	self.window.show()
	self.status_count = 0
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
    def on_sfm_button_clicked(self, button, data=None):
	#create an instance of the entry objects
	# so we can get and set the text values
	self.entry1 = self.builder.get_object("entry1")
	self.entry2 = self.builder.get_object("entry2")
	self.result1 = self.builder.get_object("result1")
	#get text from the GtkEntry widget and convert
	#it into a float value so we can calculate the result
	self.sfm = float(self.entry1.get_text())
	self.diameter = float(self.entry2.get_text())

	#calculate the result convert to an int to round the number
	#then convert to a string to set the text in our label
	self.rpm = str(int(self.sfm * ((12/3.14159)/self.diameter)))
	print "entry1: %s" % str(self.entry1.get_text())
	print "calculate rpm clicked"
	self.result1.set_text(self.rpm)

if __name__ == "__main__":
    main = BugLump() # create an instance of our class
    gtk.main() # run the code
