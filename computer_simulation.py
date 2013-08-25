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

    self.create_components(self.gcomprisBoard.level)

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


  def get_current_tools(self):
    return (self.tools[self.current_tool])


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

  def create_components(self, level):

    if (level == 1):
      component_set = (CPU, Keyboard, Monitor, UPS)
    elif (level == 2):
      component_set = (motherboard, ram, harddisk, processor)

    Selector(self, component_set)


class Component(object):
  def __init__(self, computer, image, x, y):
    self.computer = computer
    self.canvas = computer.gcomprisBoard.canvas
    self.rootitem = computer.rootitem

    self.comp_rootitem = goocanvas.Group(
                           parent = self.rootitem,
                         )

    pixmap = gcompris.utils.load_pixmap(self.image)
    self.x = x
    self.y = y
    self.width = 70
    self.height = 70
    self.center_x = self.width/2
    self.center_y = self.height/2

    self.component_item_offset_x = 0
    self.component_item_offset_y = 0
    self.component_item = goocanvas.Image(
                            parent = self.comp_rootitem,
                            pixbuf = pixmap,
                            x = self.x - self.center_x,
                            y = self.y - self.center_y,
                            width = self.width,
                            height = self.height,
                          )
    self.component_item.connect("button_press_event",
                                self.component_move, self)
    self.component_item.connect("motion_notify_event",
                                self.component_move, self)

  def get_rootitem(self):
    return self.comp_rootitem

  def move(self, x, y):
    self.x = x - self.center_x
    self.y = y - self.center_y
    self.component_item.set_properties(x = self.x + self.component_item_offset_x,
                                       y = self.y + self.component_item_offset_y)

  def remove(self):
    self.comp_rootitem.remove()

  def component_move(self, widget, target, event, component):
    if event.type == gtk.gdk.MOTION_NOTIFY:
      print "type matched!!"
      if event.state & gtk.gdk.BUTTON1_MASK:
        print "event state matched"
        print "tool:", self.computer.get_current_tools()
        if (self.computer.get_current_tools()[0] == "SELECT"):
          print "it's being moved"
          component.move(event.x, event.y)

    else:
      if (self.computer.get_current_tools()[0] == "DEL"):
        print "will remove now"
        self.remove()

    return True

    
    

class CPU(Component):
  image = "computer/cpu.png"
  icon = "computer/cpu.png"
  
  def __init__(self, computer, x, y):
    print "CPU created at", x, "and", y
    super(CPU, self).__init__(computer, self.image, x, y)


class Keyboard(Component):
  image = "computer/keyboard.png"
  icon = "computer/keyboard.png"

  def __init__(self, computer, x, y):
    print "Keyboard created at", x, "and", y
    super(Keyboard, self).__init__(computer, self.image, x, y)


class Monitor(Component):
  image = "computer/monitor.png"
  icon = "computer/monitor.png"

  def __init__(self, computer, x, y):
    print "Monitor created at", x, "and", y
    super(Monitor, self).__init__(computer, self.image, x, y)


class UPS(Component):
  image = "computer/ups.png"
  icon = "computer/ups.png"

  def __init__(self, computer, x, y):
    print "UPS created at", x, "and", y
    super(UPS, self).__init__(computer, self.image, x, y)


class Selector(Component):
  def __init__(self, computer, components_class):
    self.computer = computer
    self.rootitem = computer.rootitem

    goocanvas.Svg(parent = self.rootitem,
                  svg_handle = gcompris.skin.svg_get(),
                  svg_id = "#SELECTOR"
                  )

    self.x = 15
    self.y = 60

    index_y = 10
    gap = 20
    width = 70
    height = 70
    self.init_coord = {}
    self.offset_x = self.offset_y = 0

    for component_class in components_class:
      pixmap = gcompris.utils.load_pixmap(component_class.icon)
      item = goocanvas.Image(
                parent = self.rootitem,
                pixbuf = pixmap,
                width = width,
                height = height,
                x = self.x,
                y = self.y + index_y
                )

      self.init_coord[component_class] = (self.x, self.y + index_y)
      index_y += height + gap

      item.connect("button_press_event", self.component_click, component_class)
      item.connect("button_release_event", self.component_click, component_class)
      item.connect("motion_notify_event", self.component_click, component_class)


  def component_click(self, widget, target, event, component_class):
    if (event.state & gtk.gdk.BUTTON1_MASK
        and self.computer.get_current_tools()[0]=="DEL"):
      self.computer.assign_tool(1)

    if event.type == gtk.gdk.MOTION_NOTIFY:
      if event.state & gtk.gdk.BUTTON1_MASK:
        if self.offset_x == 0:
          bounds = widget.get_bounds()
          self.offset_x = (event.x - bounds.x1)
          self.offset_y = (event.y - bounds.y1)

        widget.set_properties(x = event.x - self.offset_x,
                              y = event.y - self.offset_y)

    if event.type == gtk.gdk.BUTTON_RELEASE:
      if event.button == 1:
        bounds = widget.get_bounds()
        x_pos = event.x - self.offset_x + (bounds.x2 - bounds.x1)/2
        y_pos = event.y - self.offset_y + (bounds.y2 - bounds.y1)/2
        print "Placing at", x_pos, "and", y_pos
        component_class(self.computer,
                        event.x - self.offset_x + (bounds.x2 - bounds.x1)/2,
                        event.y - self.offset_y + (bounds.y2 - bounds.y1)/2,
                        )

        widget.set_properties(x = self.init_coord[component_class][0],
                              y = self.init_coord[component_class][1])

        self.offset_x = self.offset_y = 0

      return True
