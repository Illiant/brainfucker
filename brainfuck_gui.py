#!/usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import array

import wx
import brainfuck

import random
from itertools import izip, chain


def make_static(size):
    # print(size)
    mem = [random.randint(0, 255) for i in range(size[0] * size[1])]
    mem = list(chain.from_iterable(izip(mem, mem, mem)))
    data = array.array(b'B', mem)

    # print(type(data))
    # print(len(data))
    # print(size[0] * size[1] * 3)

    return wx.BitmapFromBuffer(size[0], size[1], data)


def from_memory(size, mem):
    data = list(chain.from_iterable(izip(mem, mem, mem)))
    data = array.array(b'B', data)

    return wx.BitmapFromBuffer(size[0], size[1], data)


class BFMemory(wx.Panel):
    fucker = None

    def __init__(self, *args, **kwargs):
        self.fucker = kwargs.pop('fucker')

        super(BFMemory, self).__init__(*args, **kwargs)

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.update()

    def create_bitmap(self):
        #image = get_image()
        #bitmap = pil_to_wx(image)
        #bitmap = make_static(self.Size)
        bitmap = from_memory((512, 512), self.fucker._memory)
        return bitmap

    def update(self):
        self.Refresh()
        self.Update()
        wx.CallLater(15, self.update)

    def onPaint(self, event):
        bitmap = self.create_bitmap()
        dc = wx.AutoBufferedPaintDC(self)
        dc.DrawBitmap(bitmap, 0, 0)


class BrainfuckGUI(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(BrainfuckGUI, self).__init__(*args, **kwargs)

        self.bf = brainfuck.Brainfucker(memory=512 * 512)

        self.initUI()

    def initUI(self):
        """
        Does main init of GUI
        """
        self.tools = {}
        self.toolbar = self.CreateToolBar()
        self.statusbar = self.CreateStatusBar()

        # State
        # Clock
        # Memory pointer / Memory size
        # Instruction pointer / Program size
        self.statusbar.SetFieldsCount(4)

        self.tools['quit'] = self.toolbar.AddLabelTool(wx.ID_EXIT,
                                                       'Quit',
                                                       wx.Bitmap('icons/exclamation.png'))

        self.toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnQuit, self.tools['quit'])

        panel = wx.Panel(self)
        #panel.SetBackgroundColour('#4f5049')

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        editor = self.initEditor(panel)
        hbox.Add(editor, 1, wx.EXPAND | wx.ALL, 10)

        buttons = self.initButtons(panel)
        hbox.Add(buttons, 0, wx.EXPAND | wx.ALL, 10)

        output = self.initOutput(panel)
        hbox.Add(output, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(hbox)

        self.updateStatus()

    def initEditor(self, parent):
        """
        Inits the text editor window
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.editor = wx.TextCtrl(parent, style=wx.TE_MULTILINE)
        sizer.Add(self.editor, 1, wx.EXPAND | wx.ALL, 5)

        return sizer
        #return wx.TextCtrl(self, style=wx.TE_MULTILINE)

    def initOutput(self, parent):
        """
        Inits the graphical output window
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(BFMemory(parent=parent, fucker=self.bf),
                  1,
                  wx.EXPAND | wx.ALL,
                  5)

        return sizer

    def initButtons(self, parent):
        """
        Inits a bar of buttons for doing stuff
        """
        self.buttons = {}

        self.buttons['step'] = wx.Button(parent, label="Step")
        self.Bind(wx.EVT_BUTTON, self.OnStep, self.buttons['step'])

        #self.buttons['run'] = wx.Button(parent, label="Run")
        #self.Bind(wx.EVT_BUTTON, self.OnRun, self.buttons['run'])

        self.buttons['reset'] = wx.Button(parent, label="Reset")
        self.Bind(wx.EVT_BUTTON, self.OnReset, self.buttons['reset'])

        self.buttons['program'] = wx.Button(parent, label="Program")
        self.Bind(wx.EVT_BUTTON, self.OnProgram, self.buttons['program'])

        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(parent, label="Actions")
        sizer.Add(label, 0)
        sizer.Add(self.buttons['step'], 0)
        #sizer.Add(self.buttons['run'], 0)
        sizer.Add(self.buttons['reset'], 0)
        sizer.Add(self.buttons['program'], 0)
        return sizer

    def updateStatus(self):
        self.statusbar.SetStatusText('State: %d' % self.bf._state, 0)
        self.statusbar.SetStatusText('Clock: %d' % self.bf._clock, 1)
        self.statusbar.SetStatusText('Memory: %d / %d' % (self.bf._sp,
                                                          self.bf._size),
                                     2)

        self.statusbar.SetStatusText('Instruction: %d / %d' % (self.bf._ip,
                                                               len(self.bf._program)),
                                     3)

    def OnStep(self, e):
        self.bf.step()
        self.updateStatus()

    def OnReset(self, e):
        self.bf.reset()
        self.updateStatus()

    def OnRun(self, e):
        self.bf.run()

    def OnProgram(self, e):
        self.bf.program(self.editor.GetValue())

    def OnQuit(self, e):
        self.Close()


def main():
    app = wx.App(redirect=False)
    window = BrainfuckGUI(parent=None,
                          id=wx.ID_ANY,
                          title='Brainfuck')
    window.Show(True)

    app.MainLoop()


if __name__ == '__main__':
    main()