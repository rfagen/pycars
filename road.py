#!/usr/bin/env python

import wx

class Road(wx.Bitmap):
    """
    A bitmap that represents the different types of road surface
    """
    controlmap = {
                0: 'no-control.jpg',
                1: 'yield.jpg',
                2: 'stop.jpg',
                3: 'light-red.jpg',
                4: 'light-yellow.jpg',
                5: 'light-green.jpg'
                }
    exitmap = {
                1.1: './dead-end-north.jpeg',
                1.2: './dead-end-east.jpeg',
                1.3: './dead-end-south.jpg',
                1.4: './dead-end-west.jpeg',
                2.1: './straight-n-s.jpg',
                2.2: './straight-e-w.jpeg',
                2.3: './elbow-n-e.jpg',
                2.4: './elbow-e-s.jpeg',
                2.5: './elbow-s-w.jpeg',
                2.6: './elbow-w-n.jpeg',
                3.1: './tee-n-s-e.jpg',
                3.2: './tee-n-s-w.jpeg',
                3.3: './tee-e-w-n.jpeg',
                3.4: './tee-e-w-s.jpeg',
                4.0: './four-way.jpg'
              }

    def __init__(self, *args, **kw):
        #super(Road, self).__init__(*args, **kw)
        super(Road, self).__init__()

        self.lanes = kw.get('lanes')
        if self.lanes == None:
            self.lanes = 2
        if self.lanes <= 0:
            raise Exception('BAD_LANE',self.lanes)

        self.exits = kw.get('exits')
        if self.exits == None:
            self.exits = 2.1 # straight n/s road
        if self.exits not in self.exitmap.keys():
#        [
#                1.1, # dead end open to north
#                1.2, # dead end open to east
#                1.3, # dead end open to south
#                1.4, # dead end open to west
#                2.1, # straight n/s road 
#                2.2, # straight e/w road
#                2.3, # n -> e elbow
#                2.4, # e -> s elbow
#                2.5, # s -> w elbow
#                2.6, # w -> n elbow
#                3.1, # n/s tee east
#                3.2, # n/s tee west
#                3.3, # e/w tee north
#                3.4, # e/w tee south
#                4.0  # 4 way
#                ]:
            raise Exception('BAD_EXITS', self.exits)

        self.controls = kw.get('controls')
        if self.controls == None:
            self.controls = [0]*int(self.exits) # no controls on any exit
        if len(self.controls) != int(self.exits):
            raise Exception('BAD_CONTROL_COUNT', self.exits, self.controls)

        self.LoadFile(self.getRoadPictureName(),type=wx.BITMAP_TYPE_JPEG)
        self.SetSize(wx.Size(100,100))

    def getLanes(self):
        return self.lanes

    def getExits(self):
        return self.exits

    def getControls(self):
        return self.controls

    def getAll(self):
        return {
            'lanes': self.getLanes(),
            'exits': self.getExits(),
            'controls': self.getControls()
            }

    def getRoadPictureName(self):
        return self.exitmap[self.exits]

    def getControlPictureName(self):
        return self.controlmap[self.controls]

    def setLightColor(self, lightnum, lightval):
        if lightval not in [3, 4, 5] or lightnum > len(self.controls):
            raise Exception('BAD_CONTROL_LIGHT_VALUE', lightnum, lightval, self.controls)
        self.controls[lightnum]=lightval
