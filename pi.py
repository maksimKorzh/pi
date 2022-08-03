#!/bin/python3
import curses, sys, os
s = curses.initscr()
s.keypad(True)
s.nodelay(1)
curses.noecho()
curses.raw()
ROWS, COLS = s.getmaxyx(); ROWS -= 1
r, c, x, y = [0] * 4; b = []
try:
  with open(sys.argv[1]) as f: content = f.read().split('\n')
  for rw in content[:-1]: b.append([ord(c) for c in rw])
except: b.append([])
while(True):  
  curses.curs_set(0); s.move(0, 0)
  if r < y: y = r
  if r >= y + ROWS: y = r - ROWS+1
  if c < x: x = c
  if c >= x + COLS: x = c - COLS+1
  for rw in range(ROWS):
    brw = rw + y
    for cl in range(COLS):
      bcl = cl + x
      try: s.addch(rw, cl, b[brw][bcl])
      except: pass
    s.clrtoeol()
    try: s.addch('\n')  if brw < len(b) else s.addstr('~\n')
    except: pass
  s.move(r - y, c - x)
  curses.curs_set(1); s.refresh(); ch = -1;
  while (ch == -1): ch = s.getch()
  if ((ch) & 0x1f) != ch and ch < 128: b[r].insert(c, ch); c += 1
  if ch == ord('\n'): l = b[r][c:]; b[r] = b[r][:c]; r += 1; c = 0; b.insert(r, [] + l)
  if ch == curses.KEY_BACKSPACE and c: c -= 1; del b[r][c]
  elif ch == curses.KEY_BACKSPACE and c == 0 and r: l = b[r][c:]; del b[r]; r -= 1; c = len(b[r]); b[r] += l
  rw = b[r] if r < len(b)-1 else None
  if ch == curses.KEY_LEFT and c != 0: c -= 1
  elif ch == curses.KEY_LEFT and c == 0 and r > 0: r -= 1; c = len(b[r])
  if ch == curses.KEY_RIGHT and rw is not None and c < len(rw): c += 1
  elif ch == curses.KEY_RIGHT and rw is not None and c == len(rw): r += 1; c = 0
  if ch == curses.KEY_UP and r != 0: r -= 1
  if ch == curses.KEY_DOWN and r < len(b)-1: r += 1
  rw = b[r] if r < len(b) else None; rwlen = len(rw) if rw is not None else 0
  if c > rwlen: c = rwlen
  
  





