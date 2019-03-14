#!/usr/bin/env python3
# Trace Geological Route

from socket import gethostbyname
from traceroute import Traceroute
from geomap import Map

class GeoRoute:

  def __init__(self, hostname):

    self.engine = Map()
    self.destination = gethostbyname(hostname)
    self.tracer = Traceroute(self.destination, self.engine)

    self.engine.markers.FILL = 'OrangeRed3'
    self.engine.markers.LFILL = 'OrangeRed4'
    self.tracer.CALLBACK = self.engine.clean
    self.tracer.SEPERATOR = ''

  def trace(self):
    self.tracer.trace()
    return self

if __name__ == '__main__':

  from os import getuid
  from sys import argv

  # ensure root access for
  # raw socket transmission
  if getuid() != 0:
    print('Missing Administrative Access!')
    exit(2)

  # TODO
  # standardize cli arguments
  if len(argv) == 2:
    geotracer = GeoRoute(argv[1])
  else:
    geotracer = GeoRoute('www.ashenm.ml')

  geotracer.trace().engine.window.mainloop()
