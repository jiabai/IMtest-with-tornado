from __future__ import print_function

from websocket import *
import sys
import select

class EventPool(object):
  def __init__(self):
    self.__fdDict = {}
    self.__fdArgs = {}
    try:
      self.__epoll_fds = select.epoll()
    except select.error, msg:
      print(msg)

  def register(self, fd, func, args, action=select.EPOLLIN):
    try:
      self.__epoll_fds.register(fd, action)
      self.__fdDict[fd] = func
      self.__fdArgs[fd] = args
    except select.error, msg:
      print(msg)

  def dispatch(self):
    while True:
      epoll_list = self.__epoll_fds.poll()
      for fd, events in epoll_list:
        self.__fdDict[fd](self.__fdArgs[fd])

def StdinRead(ws):
  try:
    line = sys.stdin.readline()
    msg = '{"To": "NickBot", \
            "From": "Mark", \
            "Message": "%s"}' % line.strip()
    ws.send(msg)
  except Exception, e:
    print(e)

def WsRead(ws):
  try:
    result =  ws.recv()
    print("%s" % result)
  except Exception, e:
    print(e)

ws = create_connection("ws://127.0.0.1/ws")
print("start send...")

events = EventPool()
events.register(sys.stdin.fileno(), StdinRead, ws)
events.register(ws.sock.fileno(), WsRead, ws)
events.dispatch()
