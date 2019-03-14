#!/usr/bin/env python3
# Hostname to Geolocation

from json import load
from socket import gethostbyname
from urllib.request import urlopen

def geolocate(host):
  try:
    return load(urlopen('http://ip-api.com/json/{}'.format(gethostbyname(host))))
  except:
    return dict()

def geocoords(host):
  try:
    return tuple(load(urlopen('http://ip-api.com/json/{}?fields=lat,lon'.format(gethostbyname(host)))).values())
  except:
    return tuple()

if __name__ == '__main__':

  from re import match
  from sys import argv

  if len(argv) != 2:
    print(f'Usage: {argv[0]} HOSTNAME')
    exit(2)

  if not match(r'\w{2,}\.\w{2,}', argv[1]):
    print('Invalid HOSTNAME')
    exit(2)

  print(geolocate(argv[1]))
