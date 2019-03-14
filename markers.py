#!/usr/bin/env python3
# A Customised List Object

class Marker(list):

  def __init__(self, width=10, fill='red', lastfill='green', activefill='khaki'):

    self.LFILL = lastfill
    self.ACTIVEFILL = activefill
    self.OFFSET = width / 2
    self.WIDTH = width
    self.FILL = fill

  def push(self, geocoords, plotcoords=(None, None)):
    self.append((geocoords, plotcoords))
    return self[-1]

  def last(self, default=None):
    return self[-1] if len(self) else default
