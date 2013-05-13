from utils import Observable
from utils import clamp

class MenuScreen(Observable):
    """Represents a List with menu entries"""

    def __init__(self, previous, menulist):
        super(MenuScreen, self).__init__()
        self.previous = previous
        self.menulist = menulist
        self._menu_pos = 0

    @property
    def menu_pos(self):
        return self._menu_pos

    @menu_pos.setter
    def menu_pos(self, value):
        oldpos = self._menu_pos
        newpos = clamp(value, 0, LCD_ROWS - 1)
        self._menu_pos = newpos
        if oldpos != newpos:
            print("notifying observers")
            self.notify_observers()
            """self.lcd.cursor_pos = (oldpos, 0)
            self.lcd.write_string(self.menu_prefix)
            self.lcd.cursor_pos = (newpos, 0)
            self.lcd.write_string(self.menu_selected)"""

    def redraw(self):
        print("Redrawing MenuScreen: ", id(self))
        pass