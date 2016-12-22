#!/usr/bin/python
"""This is an udp / binary client
  
Inspired by the PixelFlut projector on eth0:winter 2016 and
code from https://github.com/defnull/pixelflut/
"""
  
__version__ = 0.3
__author__ = "Jan Klopper <jan@underdark.nl>"

import random
import time
from vloed import PixelVloedClient, NewMessage, RGBPixel, MAX_PIXELS
import optparse
import colorsys

def RandomFill(message, width, height):
  """Generates a random number of pixels with a random color"""
  for pixel in xrange(0, random.randint(10, MAX_PIXELS)):
    pixel = RGBPixel(random.randint(0, width),
                     random.randint(0, height),
                     random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255))
    try:
      message.append(pixel)
    except IndexError:
      yield ''.join(message)
      message[2:] = [pixel]
  yield ''.join(message)


def createlist(r=0,g=0,b=0):
  listofpixels = []
  width = 1366
  height = 786

  for x in xrange(0, width):
    for y in xrange(0, height):
      pixel = RGBPixel(x, y, r, g, b)
      listofpixels.append(pixel)
  print "done making list"    
  random.shuffle(listofpixels)
  print "done shuffeling list"					
  return listofpixels

def hsv2rgb(h,s,v):
  print h,s,v
  h = float(h)/360
  s = float(s)/100
  v = float(v)/100
  print h,s,v
  r,g,b = colorsys.hsv_to_rgb(h,s,v)
  
  return int(r * 255), int(g * 255), int (b * 255)
# todo  
def randomColorCycle(message):
  h=0
  s=0
  v=random.randint(25,75)
  r,g,b = hsv2rgb(h,s,v)
  print r,g,b
  listofpixels = createlist(r, g, b)
  for x in xrange(0, len(listofpixels)):
  
    pixel = listofpixels[x]
    try:   
      message.append(pixel)
    except IndexError:
      yield ''.join(message)
      message[2:] = [pixel]
  yield ''.join(message)
  
def decay(message):
  listofpixels = createlist(0, 0, 0)
  while True:
    for x in xrange(0, len(listofpixels)):
      pixel = listofpixels[x]
      try:   
        message.append(pixel)
      except IndexError:
        yield ''.join(message)
        message[2:] = [pixel]
    yield ''.join(message)
    

def RunClient(options):
  """Discover the servers and start sending to the first one"""

  client = PixelVloedClient(True, # start as soon as we find a server
                            options.debug, # show debugging output
                            options.ip, # ip of the server, None for autodetect
                            options.port, # port of the server None for autodetect
                            options.width, # Screen pixels wide, None for autodetect
                            options.height  # Screen pixels height, None for autodetect
                            )
  
  message = NewMessage() #create a new message that buffers the output etc
  
  # loop the effect until we cancel by pressing ctrl+c / exit the program
  while True:
    # create a new message and send it every time the buffer is full
    #for packet in randomColorCycle(message):
    #for packet in decay(message):
    for packet in RandomFill(message, client.width, client.height):
    # send the message we just filled with random pixels
      client.SendPacket(packet,sleep=0.001)

if __name__ == '__main__':
  # if this script is called from the command line, and thus not imported
  # start a client and start sending messages
  parser = optparse.OptionParser()
  parser.add_option('-v', action="store_true", dest="debug", default=False)
  parser.add_option('-i', action="store", dest="ip", default=None)
  parser.add_option('-p', action="store", dest="port", default=None,
                    type="int")
  parser.add_option('-x', action="store", dest="width", default=None,
                    type="int")
  parser.add_option('-y', action="store", dest="height", default=None,
                    type="int")
  options, remainder = parser.parse_args()

  try:
    RunClient(options)
  except KeyboardInterrupt:
    print 'Closing client'
