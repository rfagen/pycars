#!/usr/bin/env python

import wx

class SimFrame(wx.Frame):
    """
    A Frame that holds the road and the cars
    """
    fx=0
    fy=0
    GREEN = bytearray([0,200,0])
    RED = bytearray([200,0,0])
    BLACK = bytearray([0,0,0])
    CELLSIZE = 100*100
    ROADROWS = 5
    ROADCOLS = 10
    roadcells = []

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(SimFrame, self).__init__(*args, **kw)

        self.makeMenuBar()
        self.CreateStatusBar()
        self.Centre()
        self.content = wx.Bitmap(100,100)
        self.content.CopyFromBuffer(self.BLACK*self.CELLSIZE)
        self.gridsizer = wx.GridSizer(rows=self.ROADROWS, cols=self.ROADCOLS, gap=wx.Size(1,1))
        for shard in range(0,self.ROADROWS * self.ROADCOLS):
            self.roadcells.append(wx.StaticBitmap(self, bitmap=self.content))
            self.gridsizer.Add(self.roadcells[-1])
        self.SetSizer(self.gridsizer)

        self.mailbox = wx.StaticText(self)

    def makeMenuBar(self):
        """
        The menu bar
        """

        fileMenu = wx.Menu()
        goItem = fileMenu.Append(-1, "&Go\tCtrl-g",
                "Make the cars go")
        pauseItem = fileMenu.Append(-1, "&Pause\tCtrl-p",
                "Make the cars stop")
        newItem = fileMenu.Append(-1, "&New\tCtrl-n",
                "Clear the current workspace without saving")
        loadItem = fileMenu.Append(-1, "&Load\tCtrl-l",
                "Load a saved workspace")
        saveItem = fileMenu.Append(-1, "&Save\tCtrl-s",
                "Save the current workspace")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnGo, goItem)
        self.Bind(wx.EVT_MENU, self.OnPause, pauseItem)
        self.Bind(wx.EVT_MENU, self.OnNew,  newItem)
        self.Bind(wx.EVT_MENU, self.OnLoad, loadItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def setCells(self, content):
        for roadcell in self.roadcells:
            roadcell.SetBitmap(content)

    def OnGo(self, event):
        """Make the cars go."""
        self.mailbox.SetLabel("going")
        self.content.CopyFromBuffer(self.GREEN*self.CELLSIZE)
        self.setCells(self.content)

    def OnPause(self, event):
        """Make the cars stop."""
        self.mailbox.SetLabel("pausing")
        self.content.CopyFromBuffer(self.RED*self.CELLSIZE)
        self.setCells(self.content)

    def OnNew(self, event):
        """Clear the current scenario."""
        self.mailbox.SetLabel("cleaning")
        self.content.CopyFromBuffer(self.BLACK*self.CELLSIZE)
        self.setCells(self.content)

    def OnLoad(self, event):
        """Load a saved scenario."""
        self.mailbox.SetLabel("loading")

    def OnSave(self, event):
        """Save the current scenario."""
        self.mailbox.SetLabel("saving")

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnSize(self, event=None):
        self.fx,self.fy=self.GetSize().Get()
        shardsize = self.fx / 10
        shard = 0
        for roadcell in self.roadcells:
            roadcell.pos = wx.Point((shardsize+1)*shard, self.fy/2)
            shard += 1

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Simulate traffic",
                      "About Cars",
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
    frm = SimFrame(None, size=wx.Size(1000,500), title='Cars')
    frm.Show()
    app.MainLoop()
