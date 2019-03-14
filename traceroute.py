#!/usr/bin/env python3
# A Traceroute Implementation

from sys import stdout
from time import sleep
from struct import pack
from random import randrange
from socket import AF_INET, IPPROTO_ICMP, IPPROTO_UDP, IP_TTL, SO_RCVTIMEO
from socket import SOCK_RAW, SOCK_DGRAM, SOL_IP, SOL_SOCKET, gethostbyname, socket

class Traceroute:

  def __init__(self, destination='www.ashenm.ml', file=stdout, callback=lambda: None):

    self.COGNITO = '*'
    self.SEPERATOR = '\n'
    self.DESTINATION = gethostbyname(destination)
    self.CALLBACK = callback
    self.OUTPUT = file

  def __cast(self, hop, host):

    if self.OUTPUT is stdout:
      print(f'{str(hop).rjust(2)} {host}', file=self.OUTPUT, flush=True)
      return

    self.OUTPUT.write(bytes(host + self.SEPERATOR, 'ascii'))

  def trace(self, ceiling=30, timeout=2500):

    port = randrange(33434, 33534)
    timeout = pack('ll', timeout // 1000, timeout % 1000)

    for hop in range(1, ceiling + 1):

      host = None
      receiver = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
      sender = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

      sender.setsockopt(SOL_IP, IP_TTL, hop)
      receiver.setsockopt(SOL_SOCKET, SO_RCVTIMEO, timeout)

      receiver.bind(('', port))
      sender.sendto(b'', (self.DESTINATION, port))

      try:
        data, (host, _) = receiver.recvfrom(32)
      except:
        self.__cast(hop, self.COGNITO)
      else:
        self.__cast(hop, host)
      finally:
        receiver.close()
        sender.close()

      if host == self.DESTINATION:
        self.CALLBACK()
        break;

      sleep(0.25)

    return self

if __name__  == '__main__':

  from os import getuid
  from signal import SIGINT, signal

  if getuid() != 0:
    print('Missing Administrative Access!')
    exit(2)

  signal(SIGINT, lambda signum, frame: exit(130))

  Traceroute().trace()
