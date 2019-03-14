#!/usr/bin/env python3
# GeoMap an IP

from math import log, pi, tan, radians
from geolocate import geocoords
from tkinter import NW, Canvas, PhotoImage, Tk
from markers import Marker

class Map:

  def __init__(self):

    self.window = Tk()
    self.markers = Marker()
    self.mercator = PhotoImage(master=self.window, file='mercator.png')
    self.canvas = Canvas(master=self.window)

    self.WIDTH = self.mercator.width()
    self.HEIGHT = self.mercator.height()

    self.window.title('GeoRoute')
    self.window.resizable(False, False)
    self.window.geometry('{}x{}'.format(self.WIDTH, self.HEIGHT))
    self.canvas.configure(width=self.mercator.width(), height=self.mercator.height())
    self.canvas.create_image(0, 0, anchor=NW, image=self.mercator)
    self.canvas.pack()

  def project(self, latitude, longitude):

    coordX = (self.WIDTH / 360) * (longitude + 180)
    coordY = (self.HEIGHT / 2) - (self.WIDTH * log(tan((pi / 4) + (radians(latitude) / 2))) / (2 * pi))

    self.canvas.create_line(
      coordX, coordY, *self.markers.last(default=((), (coordX, coordY)))[1], width=2, fill=self.markers.FILL)
    self.canvas.create_oval(
      coordX - self.markers.OFFSET, coordY - self.markers.OFFSET,
      coordX + self.markers.OFFSET, coordY + self.markers.OFFSET, fill=self.markers.FILL, outline='')
    self.markers.push((latitude, longitude), (coordX, coordY))

  def estimate(self, waypoints=[]):
    # TODO
    return self.markers.last()[0]

  def write(self, payload):

    address = payload.decode('ascii')
    coords = geocoords(address)

    # incognito host; use computed estimate
    if not coords and len(self.markers):
      coords = self.estimate()

    # probably still internal network
    elif not coords:
      return

    self.print(address)
    self.emit(coords)

  def emit(self, payload):
    self.project(*payload)
    self.window.update()

  def print(self, payload):
    print(len(self.markers) + 1, payload)

  def clean(self):
    self.canvas.itemconfig(len(self.markers) * 2 + 1, fill=self.markers.LFILL)

  def gmap(self):
    # TODO
    pass
