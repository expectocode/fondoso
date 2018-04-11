from subprocess import Popen, PIPE, TimeoutExpired
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

FILE_NAME = "pyfondo.png"
DEFAULT_OPTIONS = "--random --delta 4 --kind treerev --positions 0,0:50,50 --size 500x500"

class Window(Gtk.Window):
    def __init__(self):
        super().__init__(title="Fondo viewer")
        self.set_default_size(500, 500)
        self.box = Gtk.VBox(spacing=4)
        self.add(self.box)

        self.viewer = Gtk.Image.new_from_file(FILE_NAME)
        self.runbutton = Gtk.Button(label="Run")
        self.runbutton.connect("clicked", self.run_button_clicked)

        self.resetbutton = Gtk.Button(label="Reset options")
        self.resetbutton.connect("clicked", self.reset_button_clicked)

        self.command_entry = Gtk.Entry()
        self.command_entry.set_text(DEFAULT_OPTIONS)
        self.hbox = Gtk.HBox(spacing=4)

        self.box.pack_start(self.viewer, True, True, 0)
        self.box.pack_start(self.command_entry, False, False, 0)

        self.hbox.pack_start(self.runbutton, True, True, 0)
        self.hbox.pack_start(self.resetbutton, True, True, 0)

        self.box.pack_start(self.hbox, False, False, 0)

        # Arguments at the end get preference, so put filename at end

    def run_button_clicked(self, widget):
        # TODO async
        command = "{} -o {}".format(self.command_entry.get_text(), FILE_NAME)
        proc = Popen("cargo run --release -- {}".format(command), shell=True,
                     stdout=PIPE, stderr=PIPE, universal_newlines=True)
        try:
            stout, sterr = proc.communicate(timeout=30)
        except TimeoutExpired:
            return # TODO display
        print(stout, sterr)
        # TODO display these
        self.viewer.set_from_file(FILE_NAME) # reload

    def reset_button_clicked(self, widget):
        self.command_entry.set_text(DEFAULT_OPTIONS)


if __name__ == "__main__":
    window = Window()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
