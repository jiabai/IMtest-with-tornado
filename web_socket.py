from __future__ import print_function

from websocket import *
import sys
import select

class EventPool(object):

  def __init__(self):
    fdDict = {}
    try:
      epoll_fds = select.epoll()
    except select.error, msg:
      print(msg)

  def register(self, fd, func, action=select.EPOLLIN):
    try:
      epoll_fds.register(fd, action)
      fdDict[fd] = func
    except select.error, msg:
      print(msg)


ws = create_connection("ws://127.0.0.1:2180/ws")
msg = '{"To": "NickBot", \
        "from": "Jabari", \
        "Message": "hoo yoo"}'
print("start send...")
while 1:
  try:
    line = sys.stdin.readline()
    msg = '{"To": "NickBot", \
            "From": "Jabari", \
            "Message": "%s"}' % line.strip()
    ws.send(msg)
    result =  ws.recv()
    print("%s" % result)
  except Exception,e:
    print(e)
    break
ws.close()
