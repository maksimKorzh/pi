#!/bin/python3
import curses, json, sys, os, time
with open('bindings.json') as f: com = json.loads(f.read())
cur = [0, 0]; b = []; src = ''; ch = ''; s = None; req = ''; res = []; idx = 0; line = []
try:
  with open(sys.argv[1]) as f: cont = f.read().split('\n')
  for rw in cont[:-1] if len(cont) > 1 else cont: b.append([ord(c) for c in rw])
  b.append([])
  src = sys.argv[1]
except: b.append([]); b.append([])
def main(stdscr):
  global R, C, s, r, c, x, y, ch
  s = curses.initscr()
  s.keypad(True)
  s.nodelay(1)
  curses.noecho()
  curses.raw()
  R, C = s.getmaxyx(); R -= 1
  r, c, x, y = [0] * 4; m = 1
  while(True):  
    if m:
      if r < y: y = r
      if r >= y + R: y = r - R+1
      if c < x: x = c
      if c >= x + C: x = c - C+1
    for rw in range(R+1):
      brw = rw + y
      for cl in range(C):
        bcl = cl + x
        try: s.addch(rw, cl, b[-1][bcl]) if rw == R else s.addch(rw, cl, b[brw][bcl]) if brw != len(b)-1 else ''
        except: pass
      s.clrtoeol()
      try: s.addch('\n')
      except: pass
    curses.curs_set(0); s.move(0, 0)
    s.move(r - y, c - x) if m else s.move(R, c - x)
    curses.curs_set(1); s.refresh(); ch = -1;
    while (ch == -1): ch = s.getch()
    [exec('\n'.join(com[key]['exec']), globals()) for key in com.keys() if eval(com[key]['bind'])]; 
    if ch == curses.KEY_RESIZE: R, C = s.getmaxyx(); R -= 1; s.refresh(); y = 0
    if ((ord('e')) & 0x1f) == ch: m ^= 1; cur[0] = r; cur[1] = c; r = len(b)-1; c = 0;
    if ((ch) & 0x1f) != ch and ch < 128: b[r].insert(c, ch); c += 1
    if ch == ord('\n') and not m:
      m ^= 1;
      try: exec(''.join([chr(i) for i in b[-1]]), globals())
      except Exception as e: s.move(R, 0); s.addstr(str(e)); s.refresh(); time.sleep(3);
      b[-1] = []; r = cur[0]; c = cur[1]; continue
    if ch == ord('\n'): l = b[r][c:]; b[r] = b[r][:c]; r += 1; c = 0; b.insert(r, [] + l)
    if ch == curses.KEY_BACKSPACE and c: c -= 1; del b[r][c]
    elif ch == curses.KEY_BACKSPACE and c == 0 and r and m: l = b[r][c:]; del b[r]; r -= 1; c = len(b[r]); b[r] += l
    rw = b[r] if r < len(b)-1 else None
    if ch == curses.KEY_LEFT and c != 0: c -= 1
    elif ch == curses.KEY_LEFT and c == 0 and r > 0 and m: r -= 1; c = len(b[r])
    if ch == curses.KEY_RIGHT and not m: c += 1
    if ch == curses.KEY_RIGHT and rw is not None and c < len(rw): c += 1
    elif ch == curses.KEY_RIGHT and rw is not None and c == len(rw) and r < len(b)-2: r += 1; c = 0
    if ch == curses.KEY_UP and m and r != 0: r -= 1
    if ch == curses.KEY_DOWN and m and r < len(b)-2: r += 1
    rw = b[r] if r < len(b) else None; rwlen = len(rw) if rw is not None else 0
    if c > rwlen: c = rwlen
curses.wrapper(main)
