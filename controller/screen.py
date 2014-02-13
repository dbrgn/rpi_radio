# -*- coding: utf-8 -*-
"""
The virtual screens that are printed to the LCD.
"""
import os
import time


class ScreenManager(object):
    """
    Manages screen call stack
    """

    def __init__(self, startscreen, device):
        self.device = device
        self.screen = startscreen
        self.draw()
        self.call_stack = []
        self.call_stack.append(startscreen)

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        self.screen.draw(self)

    def scrollup(self):
        self.screen.scrollup()
        self.screen.draw(self)

    def scrolldown(self):
        self.screen.scrolldown()
        self.screen.draw(self)

    def enter(self):
        new_screen = self.screen.enter()

        #screen is not an end screen (screen without further navigation)
        if new_screen:
            self.call_stack.append(self.screen)
            self.screen = new_screen
        self.draw()

    def exit(self):
        if len(self.call_stack) > 0:
            self.screen = self.call_stack.pop()
        self.draw()


class Screen(object):
    """
    Represents the screen interface
    """

    def draw(self, screen_manager):
        pass

    def scrollup(self):
        pass

    def scrolldown(self):
        pass

    def enter(self):
        return None

    def exit(self):
        pass


class ListScreen(Screen):
    def __init__(self, items):
        self.items = items
        self.pos = 0

    def scrollup(self):
        self.pos -= 1

    def scrolldown(self):
        self.pos += 1

    def draw(self, screen_manager):
        for idx, (screen_object, string) in enumerate(self.items):
            if self.get_pos() == idx:
                print "> " + string
                screen_manager.device.draw_text(0, 0, "> " + string)
            else:
                screen_manager.device.draw_text(0, 0, " " + string)
                print "  " + string

    def get_pos(self):
        return self.pos % len(self.items)

    def get_current_item(self):
        return self.items[self.get_pos()]

    def enter(self):
        return self.get_current_item()[0]


class DirScreen(ListScreen):
    def __init__(self, path):
        self.path = path
        self.items = os.listdir(path)
        super(DirScreen, self).__init__(self.items)

    def enter(self):

        if os.path.isfile(self.path + "/" + self.get_current_item()):
            return FileScreen(self.get_current_item())
        else:
            if len(os.listdir(self.path + "/" + self.get_current_item())) == 0:
                return TextScreen("<empty folder>")
            return DirScreen(self.path + "/" + self.get_current_item())

    def draw(self, screen_manager):
        for idx, string in enumerate(self.items):
            if self.get_pos() == idx:
                print "-> " + string
            else:
                print "   " + string


class FileScreen(Screen):
    def __init__(self, filename):
        self.filename = filename

    def draw(self, screen_manager):
        print "File: " + self.filename
        print "Go to parent with key 3"


class TextScreen(Screen):
    def __init__(self, text):
        self.text = text

    def draw(self, screen_manager):
        print "This is the {0} Text Screen".format(self.text)

    def enter(self):
        return None


class ActionScreen(Screen):
    def __init__(self, text, action):
        self.text = text
        self.action = action

    def draw(self, screen_manager):
        print self.text
        self.action()


class TimeScreen(Screen):
    def draw(self, screen_manager):
        print "======================"
        print "Time is: {0}".format(time.strftime("%H:%M:%S"))
        print "======================"
