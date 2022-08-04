# PI
Tiny terminal based text editor with python shell

# Intro
    I've been watching many VIM talks trying to explain
    the benefit of using VIM over the regular text editors
    and motivate people to invest their time and effort into
    learning VIM to get an exponentially growing productivity
    as a result benefit. The main idea behind VIM is to
    automate regular text editing tasks by mastering some
    basic commands and potentially using plugins to speed up
    the editing process however the downside is the learning
    curve - one needs to spend a lot of time and effort to turn
    a regular VIM text editing practice to a level where it's
    really worth it. Now what if I tell you that you can get
    the power of VIM without a need to learn anything about the
    text editor?


# Idea
    Text editing features are all about manipulating the buffer
    or positioning the cursor. In PI you can do it programmatically
    from a built-in python shell and then store your scripts as
    plugins/bindings in a configuration file.

# Example workflow
    Now let's consider a simple task - getting all the occurrences
    of a given text and replace them with a new string. In python
    this can be achieved as simple as:

```python
string.replace('old text', 'new text')
```

    PI provides a set of global variables allowing you to
    manipulate editor's internal state by changine the buffer's
    content, repositioning the cursor, etc.

    Let's take the previous example and see how it works in action,
    say we want to replace all the occurrences of a string in a given row:

```python
b[4]=[ord(c) for c in ''.join([chr(c) for c in b[4]]).replace('been', 'considered')]
```

    If you open this README with PI, press Ctrl-e to activate python shell and
    run the above line in the shell you'll get word 'been' on line 5 replaced
    with word 'considered'. All good but writing such one liners on the fly can
    be a pain, more over that if they contain errors you'll get notified but it
    won't work, so there's another option - once you've debugged the one liner
    you can store it into 'bindings.json' file and either call it by considering
    a key combination or invoking it directly from the command prompt. You can also
    write multiline 'plugins' and store them into 'bindings.json' file.

    To illustrate the above principal let's perform find & find next task with
    a pre-built feature:

    1. Press Ctrl-e to enter command line
    2. Type req='VIM' - this would init editor's internal variable 'req' with a search word
    3. Hit enter, then Ctrl-f. Press Ctrl-g if you want to find next matches.

    As mentioned earlier you can also run 'plugins' by invoking them directly in the shell.
    For instance to exit from PI you can either press Ctrl-z or Press Ctrl-e and type:
    
```python
exec(com['ctrl-z']['exec'][0])
```

    If you have a look at navigation bindings like Ctrl-HOME or PageUP
    you'll notice that they are altering cursor's position by setting
    the values to variables 'r' - row and 'c' - col. Cursor position
    can also be manipulated directly from the command prompt, type:

```python
cur=[3,4]
```

    and after you hit enter cursor would go to the 4th row and 5th column
    of the text buffer. The reason why different variables are used to
    manipulate the cursor position from 'plugins' and shell is because
    from plugins it gets altered directly while in shell it goes to the
    previously stored cursor location.

    Now imagine how many things you can do with this setup, here're just a few examples:
    1. Cutting/Copying & pasting customly selected blocks of text like VIM does in visual mode
    2. Bulk variable initialization
    3. Regular expression matches
    4. Executing OS commands and managing their outputs
    5. Or even making HTTP request to a certain URL and pasting it's response into a buffer

    I understand, all it sounds like DIY text editor but this is what PI essentially is.
    You can customize and extend it however you want. You can add syntax highlighting
    for instance (I just don't use it) or whatever!

# Default key bindings
    Ctrl-z        exit from the editor
    Ctrl-e        execute python code
    Ctrl-x        cut current line of code
    Ctrl-c        copy current of line
    Ctrl-v        paste current line of code
    Ctrl-s        save current file
    
    To 'save as' press Ctrl-e, type: "src='filename'", hit Enter and Ctrl-s

    Page DOWN     move the cursor down the number of screen rows
    Page UP       move the cursor up the number of screen rows
    Home          move the cursor to the beginning of the line
    End           move the cursor to the end of the line
    Ctrl-Home     move the cursor to the beginning of the file
    Ctrl-End      move the cursor to the end of the file
    Tab           inserts 4 spaces
    Shift-Tab     moves curso 4 space forward

# How to write your own plugin
    PI plugin is a piece of python code that can be invoked in 2 ways:
     - by a key bind
     - by calling the plugin from within a python shell

    Here's a sample plugin, allowing to save text buffer to a file:

```json
{
  {...},
  "ctrl-s": {
    "bind": "ch == ((ord('s')) & 0x1f)",
    "exec": [
      "cont=''",
      "for l in b[:-1]: cont += ''.join([chr(c) for c in l]) + '\\n'",
      "with open(src, 'w') as f: f.write(cont); d=0"
    ]
  },
  {...}
}
```

    You can reference/alter the editor's internal state variables from within
    a plugin as well as from the command prompt. Here's the list of the variables:

    r        cursor row
    c        cursor col
    x        screen col offset
    y        screen row offset
    b        screen buffer, [[], [], []] - list of rows, each row consists of integer ASCII codes
    d        file modified flag
    s        curses screen
    ch       character read from the STDIN
    src      active filename
    req      search word
    res      list of search results
    idx      search result index
    cur      [row, col] - manipulate cursor position from python shell
    line     line buffer used for copy/paste

