#!/usr/bin/env python

import wx
import road

class SimFrame(wx.Frame):
    """
    A Frame that holds the road and the cars
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(SimFrame, self).__init__(*args, **kw)

        CELLW=100
        CELLH=100
        CELLSIZE = CELLW * CELLH
        self.fx=0
        self.fy=0
        self.GREEN = wx.Bitmap(CELLW,CELLH).FromBuffer(CELLW,CELLH,bytearray([0,200,0]*CELLSIZE))
        self.RED = wx.Bitmap(CELLW,CELLH).FromBuffer(CELLW,CELLH,bytearray([200,0,0]*CELLSIZE))
        self.BLACK = wx.Bitmap(CELLW,CELLH).FromBuffer(CELLW,CELLH,bytearray([0,0,0]*CELLSIZE))
        self.DEADN = road.Road(exits=1.1,controls=[0])
        self.DEADE = road.Road(exits=1.2,controls=[0])
        self.DEADS = road.Road(exits=1.3,controls=[0])
        self.DEADW = road.Road(exits=1.4,controls=[0])
        self.STR8NS = road.Road(exits=2.1,controls=[0,0])
        self.STR8EW = road.Road(exits=2.2,controls=[0,0])
        self.ELBNE = road.Road(exits=2.3,controls=[0,0])
        self.ELBES = road.Road(exits=2.4,controls=[0,0])
        self.ELBSW = road.Road(exits=2.5,controls=[0,0])
        self.ELBWN = road.Road(exits=2.6,controls=[0,0])
        self.NSTE = road.Road(exits=3.1,controls=[0,0,0])
        self.NSTW = road.Road(exits=3.2,controls=[0,0,0])
        self.EWTN = road.Road(exits=3.3,controls=[0,0,0])
        self.EWTS = road.Road(exits=3.4,controls=[0,0,0])
        self.FOUR = road.Road(exits=4.0,controls=[0,0,0,0])
        self.ROADROWS = 5
        self.ROADCOLS = 10
        self.roadcells = []
        self.tickTime = 300

        self.makeMenuBar()
        self.CreateStatusBar()
        self.Centre()
        self.gridsizer = wx.GridSizer(rows=self.ROADROWS, cols=self.ROADCOLS, gap=wx.Size(0,0))
        for shard in range(0,self.ROADROWS * self.ROADCOLS):
            self.roadcells.append(wx.StaticBitmap(self, bitmap=self.BLACK))
            self.gridsizer.Add(self.roadcells[-1])
        self.SetSizer(self.gridsizer)
        self.timer = wx.Timer(self)
        self.timer.Start(self.tickTime)
        self.mailbox = wx.StaticText(self)
        self.Bind(wx.EVT_TIMER, self.OnTick)

    def OnTick(self, e):
        self.timer.Start(self.tickTime)

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

    def setCell(self, content):
        cells = len(self.roadcells)
        for idx in range(cells-1):
            self.roadcells[-(idx+1)].SetBitmap(self.roadcells[-(idx+2)].GetBitmap())
        self.roadcells[0].SetBitmap(content)

    def setCells(self, content):
        for roadcell in self.roadcells:
            roadcell.SetBitmap(content)

    def OnGo(self, event):
        """Make the cars go."""
        self.mailbox.SetLabel("going")
        self.setCell(self.GREEN)

    def OnPause(self, event):
        """Make the cars stop."""
        self.mailbox.SetLabel("pausing")
        #self.setCell(self.RED)
        self.setCell(self.DEADE)

    def OnNew(self, event):
        """Clear the current scenario."""
        self.mailbox.SetLabel("cleaning")
        self.setCell(self.BLACK)

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
