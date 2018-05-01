#!/usr/bin/env python

import wx

class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """
    mpos=wx.Position(0,0)

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")

        self.Bind(wx.EVT_MOTION, self.OnMove)

        self.Centre()


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                "Help string shown in status bar for this menu item")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2",
                      wx.OK|wx.ICON_INFORMATION)

    def OnMove(self, e):
        dc=wx.BufferedDC(wx.ClientDC(self))
        width,height=self.GetSize().Get()
        dc.Clear()
        mx, my = e.GetLogicalPosition(dc).Get()
        self.SetStatusText("x:{}, y:{}".format(mx, my) )
        for x in range(0,9):
            for y in range(0,9):
                pen1=wx.Pen(wx.Colour(x*20,y*20,120), width=4, style=wx.PENSTYLE_USER_DASH)
                pen1.SetDashes([x+1])
                pen2=wx.Pen(wx.Colour(x*20,y*20,120), 4)
                x1=x*mx/10
                x2=x1+(x*mx/10)
                y1=y*my/5+5
                y2=y1+(y*my/5)+5
                dc.SetPen(pen2)
                dc.DrawLine(x1+width/2, y1, x2+width/2, y2)
                if x1 > width/2:
                    x1 = width/2
                if x2 > width/2:
                    x2 = width/2
                dc.SetPen(pen1)
                dc.DrawLine(x1, y1, x2, y2)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = HelloFrame(None, size=wx.Size(1000,500), title='Hello World 2')
    frm.Show()
    app.MainLoop()
