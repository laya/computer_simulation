#  gcompris - computer_simulation.py
#
# Copyright (C) 2003, 2008 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# computer_simulation activity.
import gtk
import gtk.gdk
import gcompris
import gcompris.utils
import gcompris.skin
import goocanvas
import pango

from gcompris import gcompris_gettext as _

#
# The name of the class is important. It must start with the prefix
# 'Gcompris_' and the last part 'computer_simulation' here is the name of
# the activity and of the file in which you put this code. The name of
# the activity must be used in your menu.xml file to reference this
# class like this: type="python:computer_simulation"
#
class Gcompris_computer_simulation:
  """Empty gcompris Python class"""


  def __init__(self, gcomprisBoard):
    print "computer_simulation init"

    # Save the gcomprisBoard, it defines everything we need
    # to know from the core
    self.gcomprisBoard = gcomprisBoard
    self.gcomprisBoard.level = 1
    self.gcomprisBoard.maxlevel = 1
    self.gcomprisBoard.sublevel = 1
    self.gcomprisBoard.number_of_sublevel = 1

    self.tools = [
      ["DEL", "computer/tool-del.png", "computer/tool-del_on.png", gcompris.CURSOR_DEL],
      ["SELECT", "computer/tool-select.png", "computer/tool-select_on.png", gcompris.CURSOR_SELECT]
      ]

    # The list of placed components
    self.components = []

    # Needed to get key_press
    gcomprisBoard.disable_im_context = True

  def start(self):
    print "computer_simulation start"

    # Set the buttons we want in the bar
    gcompris.bar_set(gcompris.BAR_LEVEL)

    gcompris.bar_set_level(self.gcomprisBoard)

    gcompris.bar_location(gcompris.BOARD_WIDTH - 190, -1, 0.7)

    # Set a background image
    gcompris.set_default_background(self.gcomprisBoard.canvas.get_root_item())

    # Create our rootitem. We put each canvas item in it so at the end we
    # only have to kill it. The canvas deletes all the items it contains
    # automaticaly.
    self.rootitem = goocanvas.Group(parent =
                                    self.gcomprisBoard.canvas.get_root_item())

    self.display_game()


  def end(self):
    print "computer_simulation end"
    # Remove the root item removes all the others inside it
    self.rootitem.remove()


  def ok(self):
    print("computer_simulation ok.")


  def repeat(self):
    print("computer_simulation repeat.")


  #mandatory but unused yet
  def config_stop(self):
    pass

  # Configuration function.
  def config_start(self, profile):
    print("computer_simulation config_start.")

  def key_press(self, keyval, commit_str, preedit_str):
    utf8char = gtk.gdk.keyval_to_unicode(keyval)
    strn = u'%c' % utf8char

    print("Gcompris_computer_simulation key press keyval=%i %s" % (keyval, strn))

  def pause(self, pause):
    print("computer_simulation pause. %i" % pause)


  def set_level(self, level):
    print("computer_simulation set level. %i" % level)


  def display_game(self):
    self.rootitem = \
      goocanvas.Group(parent = self.gcomprisBoard.canvas.get_root_item())

    self.create_components()

    # Display the tools
    x = 12
    y = 10

    for i in range(0, len(self.tools)):
      item = goocanvas.Image(
               parent = self.rootitem,
               pixbuf = gcompris.utils.load_pixmap(self.tools[i][1]),
               x = x,
               y = y
               )
      x += 45
      item.connect("button_press_event", self.tool_item_event, i)

      if (self.tools[i][0] == "SELECT"):
        self.select_tool = item
        self.select_tool_number = i
        # Always select the SELECT item by default
        self.current_tool = i
        self.old_tool_item = item
        self.old_tool_item.props.pixbuf = gcompris.utils.load_pixmap(self.tools[i][2])
        gcompris.set_cursor(self.tools[i][3]);

      # Add the item in self.tools for later use
      self.tools[i].append(item)

  def tool_item_event(self, item, target, event, tool):
    if event.type == gtk.gdk.BUTTON_PRESS:
      if event.button == 1:
        self.assign_tool(tool)
        return True

    return False

  def assign_tool(self, newtool):
    # Deactivate old button
    item = self.tools[self.current_tool][4]
    item.set_properties(pixbuf = gcompris.utils.load_pixmap(self.tools[self.current_tool][1]))

    # Activate new button
    self.current_tool = newtool
    item = self.tools[newtool][4]
    item.set_properties(pixbuf = gcompris.utils.load_pixmap(self.tools[self.current_tool][2]))
    gcompris.set_cursor(self.tools[self.current_tool][3]);

  def create_components(self):
    pass
