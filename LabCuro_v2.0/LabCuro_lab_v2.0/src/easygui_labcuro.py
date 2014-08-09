"""
@version: 0.96(2010-08-29)

@note:
ABOUT EASYGUI
EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.
@note:
WARNING about using EasyGui with IDLE
You may encounter problems using IDLE to run programs that use EasyGui. Try it
and find out.  EasyGui is a collection of Tkinter routines that run their own
event loops.  IDLE is also a Tkinter application, with its own event loop.  The
two may conflict, with unpredictable results. If you find that you have
problems, try running your EasyGui program outside of IDLE.
Note that EasyGui requires Tk release 8.0 or greater.
@note:
LICENSE INFORMATION
EasyGui version 0.96
Copyright (c) 2010, Stephen Raymond Ferg
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer. 
    
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution. 
    
    3. The name of the author may not be used to endorse or promote products derived
       from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@note:
ABOUT THE EASYGUI LICENSE

This license is what is generally known as the "modified BSD license",
aka "revised BSD", "new BSD", "3-clause BSD".
See http://www.opensource.org/licenses/bsd-license.php

This license is GPL-compatible.
See http://en.wikipedia.org/wiki/License_compatibility
See http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses

The BSD License is less restrictive than GPL.
It allows software released under the license to be incorporated into proprietary products. 
Works based on the software may be released under a proprietary license or as closed source software.
http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29

"""
egversion = __doc__.split()[1]

__all__ = ['ynbox'
    , 'ccbox'
    , 'boolbox'
    , 'indexbox'
    , 'msgbox'
    , 'buttonbox'
    , 'integerbox'
    , 'multenterbox'
    , 'enterbox'
    , 'exceptionbox'
    , 'choicebox'
    , 'codebox'
    , 'textbox'
    , 'diropenbox'
    , 'fileopenbox'
    , 'filesavebox'
    , 'passwordbox'
    , 'multpasswordbox'
    , 'multchoicebox'
    , 'abouteasygui'
    , 'egversion'
    , 'egdemo'
    , 'EgStore'
    ]

import sys, os
import re
import datetime
import string
import pickle
import traceback


#--------------------------------------------------
# check python version and take appropriate action
#--------------------------------------------------
"""
From the python documentation:

sys.hexversion contains the version number encoded as a single integer. This is
guaranteed to increase with each version, including proper support for non-
production releases. For example, to test that the Python interpreter is at
least version 1.5.2, use:

if sys.hexversion >= 0x010502F0:
    # use some advanced feature
    ...
else:
    # use an alternative implementation or warn the user
    ...
"""


if sys.hexversion >= 0x020600F0:
    runningPython26 = True
else:
    runningPython26 = False

if sys.hexversion >= 0x030000F0:
    runningPython3 = True
else:
    runningPython3 = False

try:
    from PIL import Image   as PILImage
    from PIL import ImageTk as PILImageTk
    PILisLoaded = True
except:
    PILisLoaded = False

if runningPython3:
    from tkinter import *
    import tkinter.filedialog as tk_FileDialog
    from io import StringIO
else:
    from Tkinter import *
    import tkFileDialog as tk_FileDialog
    from StringIO import StringIO

def write(*args):
    args = [str(arg) for arg in args]
    args = " ".join(args)
    sys.stdout.write(args)

def writeln(*args):
    write(*args)
    sys.stdout.write("\n")

say = writeln

if TkVersion < 8.0 :
    stars = "*"*75
    writeln("""\n\n\n""" + stars + """
You are running Tk version: """ + str(TkVersion) + """
You must be using Tk version 8.0 or greater to use EasyGui.
Terminating.
""" + stars + """\n\n\n""")
    sys.exit(0)

def dq(s):
    return '"%s"' % s

rootWindowPosition = "+300+200"

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY    = ("Courier")

PROPORTIONAL_FONT_SIZE  = 10
MONOSPACE_FONT_SIZE     =  8  #a little smaller, because it it more legible at a smaller size
TEXT_ENTRY_FONT_SIZE    = 10  # a little larger makes it easier to see

#STANDARD_SELECTION_EVENTS = ["Return", "Button-1"]
STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]

# Initialize some global variables that will be reset later
__choiceboxMultipleSelect = None
__widgetTexts = None
__replyButtonText = None
__choiceboxResults = None
__firstWidget = None
__enterboxText = None
__enterboxDefaultText=""
__multenterboxText = ""
choiceboxChoices = None
choiceboxWidget = None
entryWidget = None
boxRoot = None
ImageErrorMsg = (
    "\n\n---------------------------------------------\n"
    "Error: %s\n%s")
#-------------------------------------------------------------------
# various boxes built on top of the basic buttonbox
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# ynbox
#-----------------------------------------------------------------------
def ynbox(msg="Shall I continue?"
    , title=" "
    , choices=("Yes", "No")
    , image=None
    ):
    """
    Display a msgbox with choices of Yes and No.

    The default is "Yes".

    The returned value is calculated this way::
        if the first choice ("Yes") is chosen, or if the dialog is cancelled:
            return 1
        else:
            return 0

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::
        if ynbox(): pass # continue
        else: sys.exit(0)  # exit the program

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    return boolbox(msg, title, choices, image=image)


#-----------------------------------------------------------------------
# ccbox
#-----------------------------------------------------------------------
def ccbox(msg="Shall I continue?"
    , title=" "
    , choices=("Continue", "Cancel")
    , image=None
    ):
    """
    Display a msgbox with choices of Continue and Cancel.

    The default is "Continue".

    The returned value is calculated this way::
        if the first choice ("Continue") is chosen, or if the dialog is cancelled:
            return 1
        else:
            return 0

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ccbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    return boolbox(msg, title, choices, image=image)


#-----------------------------------------------------------------------
# boolbox
#-----------------------------------------------------------------------
def boolbox(msg="Shall I continue?"
    , title=" "
    , choices=("Yes","No")
    , image=None
    ):
    """
    Display a boolean msgbox.

    The default is the first choice.

    The returned value is calculated this way::
        if the first choice is chosen, or if the dialog is cancelled:
            returns 1
        else:
            returns 0
    """
    reply = buttonbox(msg=msg, choices=choices, title=title, image=image)
    if reply == choices[0]: return 1
    else: return 0


#-----------------------------------------------------------------------
# indexbox
#-----------------------------------------------------------------------
def indexbox(msg="Shall I continue?"
    , title=" "
    , choices=("Yes","No")
    , image=None
    ):
    """
    Display a buttonbox with the specified choices.
    Return the index of the choice selected.
    """
    reply = buttonbox(msg=msg, choices=choices, title=title, image=image)
    index = -1
    for choice in choices:
        index = index + 1
        if reply == choice: return index
    raise AssertionError(
        "There is a program logic error in the EasyGui code for indexbox.")


#-----------------------------------------------------------------------
# msgbox
#-----------------------------------------------------------------------
def msgbox(msg="(Your message goes here)", title=" ", ok_button="OK",image=None,root=None):
    """
    Display a messagebox
    """
    if type(ok_button) != type("OK"):
        raise AssertionError("The 'ok_button' argument to msgbox must be a string.")

    return buttonbox(msg=msg, title=title, choices=[ok_button], image=image,root=root)


#-------------------------------------------------------------------
# buttonbox
#-------------------------------------------------------------------
def buttonbox(msg="",title=" "
    ,choices=("Button1", "Button2", "Button3")
    , image=None
    , root=None
    ):
    """
    Display a msg, a title, and a set of buttons.
    The buttons are defined by the members of the choices list.
    Return the text of the button that the user selected.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    global boxRoot, __replyButtonText, __widgetTexts, buttonsFrame


    # Initialize __replyButtonText to the first choice.
    # This is what will be used if the window is closed by the close button.
    __replyButtonText = choices[0]

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        # gcz edit
        #icon_dir = os.path.join(os.path.dirname(__file__),'bin','images')
        #boxRoot.iconbitmap(default=os.path.join(icon_dir,'labcuro_chromatogram.ico'))
        #boxRoot.iconbitmap(default='bin\\images\\labcuro_chromatogram.ico')
        
        #if getattr(sys, 'frozen', False):
            #print 'script'
            
            #os.system("pause")
         #   boxRoot.iconbitmap(default=str(os.path.join(os.path.dirname(sys.executable), 'bin','images','labcuro_chromatogram.ico')))
            
      # elif __file__:
            #print 'frozen'
       #     'bin\\images\\labcuro_chromatogram.ico'

        #________
        boxRoot.withdraw()

    #boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.minsize(800, 100)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    tk_Image = None
    if image:
        imageFilename = os.path.normpath(image)
        junk,ext = os.path.splitext(imageFilename)

        if os.path.exists(imageFilename):
            if ext.lower() in [".gif", ".pgm", ".ppm"]:
                tk_Image = PhotoImage(master=boxRoot, file=imageFilename)
            else:
                if PILisLoaded:
                    try:
                        pil_Image = PILImage.open(imageFilename)
                        tk_Image = PILImageTk.PhotoImage(pil_Image, master=boxRoot)
                    except:
                        msg += ImageErrorMsg % (imageFilename,
                            "\nThe Python Imaging Library (PIL) could not convert this file to a displayable image."
                            "\n\nPIL reports:\n" + exception_format())

                else:  # PIL is not loaded
                    msg += ImageErrorMsg % (imageFilename,
                    "\nI could not import the Python Imaging Library (PIL) to display the image.\n\n"
                    "You may need to install PIL\n"
                    "(http://www.pythonware.com/products/pil/)\n"
                    "to display " + ext + " image files.")

        else:
            msg += ImageErrorMsg % (imageFilename, "\nImage file not found.")

    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame,image=tk_Image)
        label.image = tk_Image # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    # -------------------- place the widgets in the frames -----------------------
    messageWidget = Message(messageFrame, text=msg, width=800)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=TOP, expand=YES, fill=X, padx='3m', pady='3m')

    __put_buttons_in_buttonframe(choices)

    # -------------- the action begins -----------
    # put the focus on the first button
    __firstWidget.focus_force()

    boxRoot.deiconify()
    boxRoot.mainloop()
    boxRoot.destroy()
    if root: root.deiconify()
    return __replyButtonText


#-------------------------------------------------------------------
# integerbox
#-------------------------------------------------------------------
def integerbox(msg=""
    , title=" "
    , default=""
    , lowerbound=0
    , upperbound=99
    , image = None
    , root  = None
    , **invalidKeywordArguments
    ):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default argument may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    NOTE that the "argLowerBound" and "argUpperBound" arguments are no longer
    supported.  They have been replaced by "upperbound" and "lowerbound".
    """
    if "argLowerBound" in invalidKeywordArguments:
        raise AssertionError(
            "\nintegerbox no longer supports the 'argLowerBound' argument.\n"
            + "Use 'lowerbound' instead.\n\n")
    if "argUpperBound" in invalidKeywordArguments:
        raise AssertionError(
            "\nintegerbox no longer supports the 'argUpperBound' argument.\n"
            + "Use 'upperbound' instead.\n\n")

    if default != "":
        if type(default) != type(1):
            raise AssertionError(
                "integerbox received a non-integer value for "
                + "default of " + dq(str(default)) , "Error")

    if type(lowerbound) != type(1):
        raise AssertionError(
            "integerbox received a non-integer value for "
            + "lowerbound of " + dq(str(lowerbound)) , "Error")

    if type(upperbound) != type(1):
        raise AssertionError(
            "integerbox received a non-integer value for "
            + "upperbound of " + dq(str(upperbound)) , "Error")

    if msg == "":
        msg = ("Enter an integer between " + str(lowerbound)
            + " and "
            + str(upperbound)
            )

    while 1:
        reply = enterbox(msg, title, str(default), image=image, root=root)
        if reply == None: return None

        try:
            reply = int(reply)
        except:
            msgbox ("The value that you entered:\n\t%s\nis not an integer." % dq(str(reply))
                    , "Error")
            continue

        if reply < lowerbound:
            msgbox ("The value that you entered is less than the lower bound of "
                + str(lowerbound) + ".", "Error")
            continue

        if reply > upperbound:
            msgbox ("The value that you entered is greater than the upper bound of "
                + str(upperbound) + ".", "Error")
            continue

        # reply has passed all validation checks.
        # It is an integer between the specified bounds.
        return reply

#-------------------------------------------------------------------
# multenterbox
#-------------------------------------------------------------------
def multenterbox(msg="Fill in values for the fields."
    , title=" "
    , fields=()
    , values=()
    ):
    r"""
    Show screen with multiple data entry fields.

    If there are fewer values than names, the list of values is padded with
    empty strings until the number of values is the same as the number of names.

    If there are more values than names, the list of values
    is truncated so that there are as many values as names.

    Returns a list of the values of the fields,
    or None if the user cancels the operation.

    Here is some example code, that shows how values returned from
    multenterbox can be checked for validity before they are accepted::
        ----------------------------------------------------------------------
        msg = "Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "":
                break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))
        ----------------------------------------------------------------------

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg fields: a list of fieldnames.
    @arg values:  a list of field values
    """
    return __multfillablebox(msg,title,fields,values,None)


#-----------------------------------------------------------------------
# multpasswordbox
#-----------------------------------------------------------------------
def multpasswordbox(msg="Fill in values for the fields."
    , title=" "
    , fields=tuple()
    ,values=tuple()
    ):
    r"""
    Same interface as multenterbox.  But in multpassword box,
    the last of the fields is assumed to be a password, and
    is masked with asterisks.

    Example
    =======

    Here is some example code, that shows how values returned from
    multpasswordbox can be checked for validity before they are accepted::
        msg = "Enter logon information"
        title = "Demo of multpasswordbox"
        fieldNames = ["Server ID", "User ID", "Password"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multpasswordbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues == None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
            fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))
    """
    return __multfillablebox(msg,title,fields,values,"*")

def bindArrows(widget):
    widget.bind("<Down>", tabRight)
    widget.bind("<Up>"  , tabLeft)

    widget.bind("<Right>",tabRight)
    widget.bind("<Left>" , tabLeft)

def tabRight(event):
    boxRoot.event_generate("<Tab>")

def tabLeft(event):
    boxRoot.event_generate("<Shift-Tab>")

#-----------------------------------------------------------------------
# __multfillablebox
#-----------------------------------------------------------------------
def __multfillablebox(msg="Fill in values for the fields."
    , title=" "
    , fields=()
    , values=()
    , mask = None
    ):
    global boxRoot, __multenterboxText, __multenterboxDefaultText, cancelButton, entryWidget, okButton

    choices = ["OK", "Cancel"]
    if len(fields) == 0: return None

    fields = list(fields[:])  # convert possible tuples to a list
    values = list(values[:])  # convert possible tuples to a list

    if   len(values) == len(fields): pass
    elif len(values) >  len(fields):
        fields = fields[0:len(values)]
    else:
        while len(values) < len(fields):
            values.append("")

    boxRoot = Tk()

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.bind("<Escape>", __multenterboxCancel)

    # -------------------- put subframes in the boxRoot --------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    #-------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame, width="4.5i", text=msg)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    global entryWidgets
    entryWidgets = []

    lastWidgetIndex = len(fields) - 1

    for widgetIndex in range(len(fields)):
        argFieldName  = fields[widgetIndex]
        argFieldValue = values[widgetIndex]
        entryFrame = Frame(master=boxRoot)
        entryFrame.pack(side=TOP, fill=BOTH)

        # --------- entryWidget ----------------------------------------------
        labelWidget = Label(entryFrame, text=argFieldName)
        labelWidget.pack(side=LEFT)

        entryWidget = Entry(entryFrame, width=40,highlightthickness=2)
        entryWidgets.append(entryWidget)
        entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,TEXT_ENTRY_FONT_SIZE))
        entryWidget.pack(side=RIGHT, padx="3m")

        bindArrows(entryWidget)

        entryWidget.bind("<Return>", __multenterboxGetText)
        entryWidget.bind("<Escape>", __multenterboxCancel)

        # for the last entryWidget, if this is a multpasswordbox,
        # show the contents as just asterisks
        if widgetIndex == lastWidgetIndex:
            if mask:
                entryWidgets[widgetIndex].configure(show=mask)

        # put text into the entryWidget
        entryWidgets[widgetIndex].insert(0,argFieldValue)
        widgetIndex += 1

    # ------------------ ok button -------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=BOTTOM, fill=BOTH)

    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __multenterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __multenterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------- time for action! -----------------
    entryWidgets[0].focus_force()    # put the focus on the entryWidget
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __multenterboxText


#-----------------------------------------------------------------------
# __multenterboxGetText
#-----------------------------------------------------------------------
def __multenterboxGetText(event):
    global __multenterboxText

    __multenterboxText = []
    for entryWidget in entryWidgets:
        __multenterboxText.append(entryWidget.get())
    boxRoot.quit()

def __multenterboxCancel(event):
    global __multenterboxText
    __multenterboxText = None

    boxRoot.quit()


#-------------------------------------------------------------------
# enterbox
#-------------------------------------------------------------------
def enterbox(msg="Enter something."
    , title=" "
    , default=""
    , strip=True
    , image=None
    , root=None
    ):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Returns the text that the user entered, or None if he cancels the operation.

    By default, enterbox strips its result (i.e. removes leading and trailing
    whitespace).  (If you want it not to strip, use keyword argument: strip=False.)
    This makes it easier to test the results of the call::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...
    """
    result = __fillablebox(msg, title, default=default, mask=None,image=image,root=root)
    if result and strip:
        result = result.strip()
    return result


def passwordbox(msg="Enter your password."
    , title=" "
    , default=""
    , image=None
    , root=None
    ):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """
    return __fillablebox(msg, title, default, mask="*",image=image,root=root)


def __fillablebox(msg
    , title=""
    , default=""
    , mask=None
    , image=None
    , root=None
    ):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """

    global boxRoot, __enterboxText, __enterboxDefaultText
    global cancelButton, entryWidget, okButton

    if title == None: title == ""
    if default == None: default = ""
    __enterboxDefaultText = default
    __enterboxText        = __enterboxDefaultText

    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.bind("<Escape>", __enterboxCancel)

    # ------------- define the messageFrame ---------------------------------
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the imageFrame ---------------------------------
    tk_Image = None
    if image:
        imageFilename = os.path.normpath(image)
        junk,ext = os.path.splitext(imageFilename)

        if os.path.exists(imageFilename):
            if ext.lower() in [".gif", ".pgm", ".ppm"]:
                tk_Image = PhotoImage(master=boxRoot, file=imageFilename)
            else:
                if PILisLoaded:
                    try:
                        pil_Image = PILImage.open(imageFilename)
                        tk_Image = PILImageTk.PhotoImage(pil_Image, master=boxRoot)
                    except:
                        msg += ImageErrorMsg % (imageFilename,
                            "\nThe Python Imaging Library (PIL) could not convert this file to a displayable image."
                            "\n\nPIL reports:\n" + exception_format())

                else:  # PIL is not loaded
                    msg += ImageErrorMsg % (imageFilename,
                    "\nI could not import the Python Imaging Library (PIL) to display the image.\n\n"
                    "You may need to install PIL\n"
                    "(http://www.pythonware.com/products/pil/)\n"
                    "to display " + ext + " image files.")

        else:
            msg += ImageErrorMsg % (imageFilename, "\nImage file not found.")

    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame,image=tk_Image)
        label.image = tk_Image # keep a reference!
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)


    # ------------- define the entryFrame ---------------------------------
    entryFrame = Frame(master=boxRoot)
    entryFrame.pack(side=TOP, fill=BOTH)

    # ------------- define the buttonsFrame ---------------------------------
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)

    #-------------------- the msg widget ----------------------------
    messageWidget = Message(messageFrame, width="4.5i", text=msg)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')

    # --------- entryWidget ----------------------------------------------
    
    #gcz edit- changed width
    entryWidget = Entry(entryFrame, width=200)
    #________________________
    
    bindArrows(entryWidget)
    entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,TEXT_ENTRY_FONT_SIZE))
    if mask:
        entryWidget.configure(show=mask)
    entryWidget.pack(side=LEFT, padx="3m")
    entryWidget.bind("<Return>", __enterboxGetText)
    entryWidget.bind("<Escape>", __enterboxCancel)
    # put text into the entryWidget
    entryWidget.insert(0,__enterboxDefaultText)

    # ------------------ ok button -------------------------------
    okButton = Button(buttonsFrame, takefocus=1, text="OK")
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __enterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ------------------ cancel button -------------------------------
    cancelButton = Button(buttonsFrame, takefocus=1, text="Cancel")
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __enterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)

    # ------------------- time for action! -----------------
    entryWidget.focus_force()    # put the focus on the entryWidget
    boxRoot.deiconify()
    boxRoot.mainloop()  # run it!

    # -------- after the run has completed ----------------------------------
    if root: root.deiconify()
    boxRoot.destroy()  # button_click didn't destroy boxRoot, so we do it now
    return __enterboxText


def __enterboxGetText(event):
    global __enterboxText
    
    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    global entryWidget
    
    entryWidget.delete(0,len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)


def __enterboxCancel(event):
    global __enterboxText
    
    __enterboxText = None
    boxRoot.quit()

def denyWindowManagerClose():
    """ don't allow WindowManager close
    """
    x = Tk()
    x.withdraw()
    x.bell()
    x.destroy()



#-------------------------------------------------------------------
# multchoicebox
#-------------------------------------------------------------------
def multchoicebox(msg="Pick as many items as you like."
    , title=" "
    , choices=()
    , **kwargs
    ):
    """
    Present the user with a list of choices.
    allow him to select multiple items and return them in a list.
    if the user doesn't choose anything from the list, return the empty list.
    return None if he cancelled selection.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if len(choices) == 0: choices = ["Program logic error - no choices were specified."]

    global __choiceboxMultipleSelect
    __choiceboxMultipleSelect = 1
    return __choicebox(msg, title, choices)


#-----------------------------------------------------------------------
# choicebox
#-----------------------------------------------------------------------
def choicebox(msg="Pick something."
    , title=" "
    , choices=()
    ):
    """
    Present the user with a list of choices.
    return the choice that he selects.
    return None if he cancels the selection selection.

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg choices: a list or tuple of the choices to be displayed
    """
    if len(choices) == 0: choices = ["Program logic error - no choices were specified."]

    global __choiceboxMultipleSelect
    __choiceboxMultipleSelect = 0
    return __choicebox(msg,title,choices)


#-----------------------------------------------------------------------
# __choicebox
#-----------------------------------------------------------------------
def __choicebox(msg
    , title
    , choices
    ):
    """
    internal routine to support choicebox() and multchoicebox()
    """
    global boxRoot, __choiceboxResults, choiceboxWidget, defaultText
    global choiceboxWidget, choiceboxChoices
    #-------------------------------------------------------------------
    # If choices is a tuple, we make it a list so we can sort it.
    # If choices is already a list, we make a new list, so that when
    # we sort the choices, we don't affect the list object that we
    # were given.
    #-------------------------------------------------------------------
    choices = list(choices[:])
    if len(choices) == 0:
        choices = ["Program logic error - no choices were specified."]
    defaultButtons = ["OK", "Cancel"]

    # make sure all choices are strings
    for index in range(len(choices)):
        choices[index] = str(choices[index])

    lines_to_show = min(len(choices), 20)
    lines_to_show = 20

    if title == None: title = ""

    # Initialize __choiceboxResults
    # This is the value that will be returned if the user clicks the close icon
    __choiceboxResults = None

    boxRoot = Tk()
    #boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )
    screen_width  = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width    = int((screen_width * .2))
    root_height   = int((screen_height * .4))
    root_xpos     = int((screen_width * 0.1))
    root_ypos     = int((screen_height * 0.05))

    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    rootWindowPosition = "+0+0"
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand=NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
    boxRoot.geometry(rootWindowPosition)

    # ---------------- put the frames in the window -----------------------------------------
    message_and_buttonsFrame = Frame(master=boxRoot)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)
    #messageFrame.pack(side=TOP, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO, pady=0)
    #buttonsFrame.pack(side=TOP, expand=YES, pady=0)

    choiceboxFrame = Frame(master=boxRoot)
    choiceboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)

    # -------------------------- put the widgets in the frames ------------------------------

    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

    # --------  put the choiceboxWidget in the choiceboxFrame ---------------------------
    choiceboxWidget = Listbox(choiceboxFrame
        , height=lines_to_show
        , borderwidth="1m"
        , relief="flat"
        , bg="white"
        )

    if __choiceboxMultipleSelect:
        choiceboxWidget.configure(selectmode=MULTIPLE)

    choiceboxWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))

    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(choiceboxFrame, orient=VERTICAL, command=choiceboxWidget.yview)
    choiceboxWidget.configure(yscrollcommand = rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(choiceboxFrame, orient=HORIZONTAL, command=choiceboxWidget.xview)
    choiceboxWidget.configure(xscrollcommand = bottomScrollbar.set)

    # pack the Listbox and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    bottomScrollbar.pack(side=BOTTOM, fill = X)
    rightScrollbar.pack(side=RIGHT, fill = Y)

    choiceboxWidget.pack(side=LEFT, padx="1m", pady="1m", expand=YES, fill=BOTH)

    #---------------------------------------------------
    # sort the choices
    # eliminate duplicates
    # put the choices into the choiceboxWidget
    #---------------------------------------------------
    for index in range(len(choices)):
        choices[index] = str(choices[index])

    if runningPython3:
        choices.sort(key=str.lower)
    else:
        choices.sort( lambda x,y: cmp(x.lower(),    y.lower())) # case-insensitive sort

    lastInserted = None
    choiceboxChoices = []
    for choice in choices:
        if choice == lastInserted: pass
        else:
            choiceboxWidget.insert(END, choice)
            choiceboxChoices.append(choice)
            lastInserted = choice

    boxRoot.bind('<Any-Key>', KeyboardListener)

    # put the buttons in the buttonsFrame
    if len(choices) > 0:
        okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
        bindArrows(okButton)
        okButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

        # for the commandButton, bind activation events to the activation event handler
        commandButton  = okButton
        handler = __choiceboxGetChoice
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

        # now bind the keyboard events
        choiceboxWidget.bind("<Return>", __choiceboxGetChoice)
        choiceboxWidget.bind("<Double-Button-1>", __choiceboxGetChoice)
    else:
        # now bind the keyboard events
        choiceboxWidget.bind("<Return>", __choiceboxCancel)
        choiceboxWidget.bind("<Double-Button-1>", __choiceboxCancel)

    cancelButton = Button(buttonsFrame, takefocus=YES, text="Cancel", height=1, width=6)
    bindArrows(cancelButton)
    cancelButton.pack(expand=NO, side=BOTTOM, padx='2m', pady='1m', ipady="1m", ipadx="2m")

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = cancelButton
    handler = __choiceboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # add special buttons for multiple select features
    if len(choices) > 0 and __choiceboxMultipleSelect:
        selectionButtonsFrame = Frame(messageFrame)
        selectionButtonsFrame.pack(side=RIGHT, fill=Y, expand=NO)

        selectAllButton = Button(selectionButtonsFrame, text="Select All", height=1, width=6)
        bindArrows(selectAllButton)

        selectAllButton.bind("<Button-1>",__choiceboxSelectAll)
        selectAllButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

        clearAllButton = Button(selectionButtonsFrame, text="Clear All", height=1, width=6)
        bindArrows(clearAllButton)
        clearAllButton.bind("<Button-1>",__choiceboxClearAll)
        clearAllButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")


    # -------------------- bind some keyboard events ----------------------------
    boxRoot.bind("<Escape>", __choiceboxCancel)

    # --------------------- the action begins -----------------------------------
    # put the focus on the choiceboxWidget, and the select highlight on the first item
    choiceboxWidget.select_set(0)
    choiceboxWidget.focus_force()

    # --- run it! -----
    boxRoot.mainloop()

    boxRoot.destroy()
    return __choiceboxResults


def __choiceboxGetChoice(event):
    global boxRoot, __choiceboxResults, choiceboxWidget
    
    if __choiceboxMultipleSelect:
        __choiceboxResults = [choiceboxWidget.get(index) for index in choiceboxWidget.curselection()]

    else:
        choice_index = choiceboxWidget.curselection()
        __choiceboxResults = choiceboxWidget.get(choice_index)

    # writeln("Debugging> mouse-event=", event, " event.type=", event.type)
    # writeln("Debugging> choice=", choice_index, __choiceboxResults)
    boxRoot.quit()


def __choiceboxSelectAll(event):
    global choiceboxWidget, choiceboxChoices
    
    choiceboxWidget.selection_set(0, len(choiceboxChoices)-1)

def __choiceboxClearAll(event):
    global choiceboxWidget, choiceboxChoices
    
    choiceboxWidget.selection_clear(0, len(choiceboxChoices)-1)



def __choiceboxCancel(event):
    global boxRoot, __choiceboxResults
    
    __choiceboxResults = None
    boxRoot.quit()


def KeyboardListener(event):
    global choiceboxChoices, choiceboxWidget
    key = event.keysym
    if len(key) <= 1:
        if key in string.printable:
            # Find the key in the list.
            # before we clear the list, remember the selected member
            try:
                start_n = int(choiceboxWidget.curselection()[0])
            except IndexError:
                start_n = -1

            ## clear the selection.
            choiceboxWidget.selection_clear(0, 'end')

            ## start from previous selection +1
            for n in range(start_n+1, len(choiceboxChoices)):
                item = choiceboxChoices[n]
                if item[0].lower() == key.lower():
                    choiceboxWidget.selection_set(first=n)
                    choiceboxWidget.see(n)
                    return
            else:
                # has not found it so loop from top
                for n in range(len(choiceboxChoices)):
                    item = choiceboxChoices[n]
                    if item[0].lower() == key.lower():
                        choiceboxWidget.selection_set(first = n)
                        choiceboxWidget.see(n)
                        return

                # nothing matched -- we'll look for the next logical choice
                for n in range(len(choiceboxChoices)):
                    item = choiceboxChoices[n]
                    if item[0].lower() > key.lower():
                        if n > 0:
                            choiceboxWidget.selection_set(first = (n-1))
                        else:
                            choiceboxWidget.selection_set(first = 0)
                        choiceboxWidget.see(n)
                        return

                # still no match (nothing was greater than the key)
                # we set the selection to the first item in the list
                lastIndex = len(choiceboxChoices)-1
                choiceboxWidget.selection_set(first = lastIndex)
                choiceboxWidget.see(lastIndex)
                return

#-----------------------------------------------------------------------
# exception_format
#-----------------------------------------------------------------------
def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
           sys.exc_info()[0]
        ,  sys.exc_info()[1]
        ,  sys.exc_info()[2]
        ))

#-----------------------------------------------------------------------
# exceptionbox
#-----------------------------------------------------------------------
def exceptionbox(msg=None, title=None):
    """
    Display a box that gives information about
    an exception that has just been raised.

    The caller may optionally pass in a title for the window, or a
    msg to accompany the error information.

    Note that you do not need to (and cannot) pass an exception object
    as an argument.  The latest exception will automatically be used.
    """
    if title == None: title = "Error Report"
    if msg == None:
        msg = "An error (exception) has occurred in the program."

    codebox(msg, title, exception_format())

#-------------------------------------------------------------------
# codebox
#-------------------------------------------------------------------

def codebox(msg=""
    , title=" "
    , text=""
    ):
    """
    Display some text in a monospaced font, with no line wrapping.
    This function is suitable for displaying code and text that is
    formatted using spaces.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.
    """
    return textbox(msg, title, text, codebox=1 )

#-------------------------------------------------------------------
# textbox
#-------------------------------------------------------------------
def textbox(msg=""
    , title=" "
    , text=""
    , codebox=0
    ):
    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.
    """

    if msg == None: msg = ""
    if title == None: title = ""

    global boxRoot, __replyButtonText, __widgetTexts, buttonsFrame
    global rootWindowPosition
    choices = ["OK"]
    __replyButtonText = choices[0]


    boxRoot = Tk()

    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose )

    screen_width = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width = int((screen_width * 0.8))
    root_height = int((screen_height * 0.5))
    root_xpos = int((screen_width * 0.1))
    root_ypos = int((screen_height * 0.05))

    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    rootWindowPosition = "+0+0"
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand=NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = "+" + str(root_xpos) + "+" + str(root_ypos)
    boxRoot.geometry(rootWindowPosition)

    mainframe = Frame(master=boxRoot)
    mainframe.pack(side=TOP, fill=BOTH, expand=YES)

    # ----  put frames in the window -----------------------------------
    # we pack the textboxFrame first, so it will expand first
    textboxFrame = Frame(mainframe, borderwidth=3)
    textboxFrame.pack(side=BOTTOM , fill=BOTH, expand=YES)

    message_and_buttonsFrame = Frame(mainframe)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)

    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)

    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO)

    # -------------------- put widgets in the frames --------------------

    # put a textArea in the top frame
    if codebox:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(textboxFrame,height=25,width=character_width, padx="2m", pady="1m")
        textArea.configure(wrap=NONE)
        textArea.configure(font=(MONOSPACE_FONT_FAMILY, MONOSPACE_FONT_SIZE))

    else:
        character_width = int((root_width * 0.6) / MONOSPACE_FONT_SIZE)
        textArea = Text(
            textboxFrame
            , height=25
            , width=character_width
            , padx="2m"
            , pady="1m"
            )
        textArea.configure(wrap=WORD)
        textArea.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))


    # some simple keybindings for scrolling
    mainframe.bind("<Next>" , textArea.yview_scroll( 1,PAGES))
    mainframe.bind("<Prior>", textArea.yview_scroll(-1,PAGES))

    mainframe.bind("<Right>", textArea.xview_scroll( 1,PAGES))
    mainframe.bind("<Left>" , textArea.xview_scroll(-1,PAGES))

    mainframe.bind("<Down>", textArea.yview_scroll( 1,UNITS))
    mainframe.bind("<Up>"  , textArea.yview_scroll(-1,UNITS))


    # add a vertical scrollbar to the frame
    rightScrollbar = Scrollbar(textboxFrame, orient=VERTICAL, command=textArea.yview)
    textArea.configure(yscrollcommand = rightScrollbar.set)

    # add a horizontal scrollbar to the frame
    bottomScrollbar = Scrollbar(textboxFrame, orient=HORIZONTAL, command=textArea.xview)
    textArea.configure(xscrollcommand = bottomScrollbar.set)

    # pack the textArea and the scrollbars.  Note that although we must define
    # the textArea first, we must pack it last, so that the bottomScrollbar will
    # be located properly.

    # Note that we need a bottom scrollbar only for code.
    # Text will be displayed with wordwrap, so we don't need to have a horizontal
    # scroll for it.
    if codebox:
        bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)

    textArea.pack(side=LEFT, fill=BOTH, expand=YES)


    # ---------- put a msg widget in the msg frame-------------------
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY,PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')

    # put the buttons in the buttonsFrame
    okButton = Button(buttonsFrame, takefocus=YES, text="OK", height=1, width=6)
    okButton.pack(expand=NO, side=TOP,  padx='2m', pady='1m', ipady="1m", ipadx="2m")

    # for the commandButton, bind activation events to the activation event handler
    commandButton  = okButton
    handler = __textboxOK
    for selectionEvent in ["Return","Button-1","Escape"]:
        commandButton.bind("<%s>" % selectionEvent, handler)


    # ----------------- the action begins ----------------------------------------
    try:
        # load the text into the textArea
        if type(text) == type("abc"): pass
        else:
            try:
                text = "".join(text)  # convert a list or a tuple to a string
            except:
                msgbox("Exception when trying to convert "+ str(type(text)) + " to text in textArea")
                sys.exit(16)
        textArea.insert(END,text, "normal")

    except:
        msgbox("Exception when trying to load the textArea.")
        sys.exit(16)

    try:
        okButton.focus_force()
    except:
        msgbox("Exception when trying to put focus on okButton.")
        sys.exit(16)

    boxRoot.mainloop()

    # this line MUST go before the line that destroys boxRoot
    areaText = textArea.get(0.0,END)
    boxRoot.destroy()
    return areaText # return __replyButtonText

#-------------------------------------------------------------------
# __textboxOK
#-------------------------------------------------------------------
def __textboxOK(event):
    global boxRoot
    boxRoot.quit()



#-------------------------------------------------------------------
# diropenbox
#-------------------------------------------------------------------
def diropenbox(msg=None
    , title=None
    , default=None
    ):
    """
    A dialog to get a directory name.
    Note that the msg argument, if specified, is ignored.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.
    """
    title=getFileDialogTitle(msg,title)
    localRoot = Tk()
    localRoot.withdraw()
    if not default: default = None
    f = tk_FileDialog.askdirectory(
          parent=localRoot
        , title=title
        , initialdir=default
        , initialfile=None
        )
    localRoot.destroy()
    if not f: return None
    return os.path.normpath(f)

#-------------------------------------------------------------------
# getFileDialogTitle
#-------------------------------------------------------------------
def getFileDialogTitle(msg
    , title
    ):
    if msg and title: return "%s - %s" % (title,msg)
    if msg and not title: return str(msg)
    if title and not msg: return str(title)
    return None # no message and no title

#-------------------------------------------------------------------
# class FileTypeObject for use with fileopenbox
#-------------------------------------------------------------------
class FileTypeObject:
    def __init__(self,filemask):
        if len(filemask) == 0:
            raise AssertionError('Filetype argument is empty.')

        self.masks = []

        if type(filemask) == type("abc"):  # a string
            self.initializeFromString(filemask)

        elif type(filemask) == type([]): # a list
            if len(filemask) < 2:
                raise AssertionError('Invalid filemask.\n'
                +'List contains less than 2 members: "%s"' % filemask)
            else:
                self.name  = filemask[-1]
                self.masks = list(filemask[:-1] )
        else:
            raise AssertionError('Invalid filemask: "%s"' % filemask)

    def __eq__(self,other):
        if self.name == other.name: return True
        return False

    def add(self,other):
        for mask in other.masks:
            if mask in self.masks: pass
            else: self.masks.append(mask)

    def toTuple(self):
        return (self.name,tuple(self.masks))

    def isAll(self):
        if self.name == "All files": return True
        return False

    def initializeFromString(self, filemask):
        # remove everything except the extension from the filemask
        self.ext = os.path.splitext(filemask)[1]
        if self.ext == "" : self.ext = ".*"
        if self.ext == ".": self.ext = ".*"
        self.name = self.getName()
        self.masks = ["*" + self.ext]

    def getName(self):
        e = self.ext
        if e == ".*"  : return "All files"
        if e == ".txt": return "Text files"
        if e == ".py" : return "Python files"
        if e == ".pyc" : return "Python files"
        if e == ".xls": return "Excel files"
        if e.startswith("."):
            return e[1:].upper() + " files"
        return e.upper() + " files"


#-------------------------------------------------------------------
# fileopenbox
#-------------------------------------------------------------------
def fileopenbox(msg=None
    , title=None
    , default="*"
    , filetypes=None
    ):
    """
    A dialog to get a file name.

    About the "default" argument
    ============================
        The "default" argument specifies a filepath that (normally)
        contains one or more wildcards.
        fileopenbox will display only files that match the default filepath.
        If omitted, defaults to "*" (all files in the current directory).

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/*.py"
        will open in directory c:\myjunk\ and show all Python files.

        WINDOWS EXAMPLE::
            ...default="c:/myjunk/test*.py"
        will open in directory c:\myjunk\ and show all Python files
        whose names begin with "test".


        Note that on Windows, fileopenbox automatically changes the path
        separator to the Windows path separator (backslash).

    About the "filetypes" argument
    ==============================
        If specified, it should contain a list of items,
        where each item is either::
            - a string containing a filemask          # e.g. "*.txt"
            - a list of strings, where all of the strings except the last one
                are filemasks (each beginning with "*.",
                such as "*.txt" for text files, "*.py" for Python files, etc.).
                and the last string contains a filetype description

        EXAMPLE::
            filetypes = ["*.css", ["*.htm", "*.html", "HTML files"]  ]

    NOTE THAT
    =========

        If the filetypes list does not contain ("All files","*"),
        it will be added.

        If the filetypes list does not contain a filemask that includes
        the extension of the "default" argument, it will be added.
        For example, if     default="*abc.py"
        and no filetypes argument was specified, then
        "*.py" will automatically be added to the filetypes argument.

    @rtype: string or None
    @return: the name of a file, or None if user chose to cancel

    @arg msg: the msg to be displayed.
    @arg title: the window title
    @arg default: filepath with wildcards
    @arg filetypes: filemasks that a user can choose, e.g. "*.txt"
    """
    localRoot = Tk()
    localRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default,filetypes)

    #------------------------------------------------------------
    # if initialfile contains no wildcards; we don't want an
    # initial file. It won't be used anyway.
    # Also: if initialbase is simply "*", we don't want an
    # initialfile; it is not doing any useful work.
    #------------------------------------------------------------
    if (initialfile.find("*") < 0) and (initialfile.find("?") < 0):
        initialfile = None
    elif initialbase == "*":
        initialfile = None

    f = tk_FileDialog.askopenfilename(parent=localRoot
        , title=getFileDialogTitle(msg,title)
        , initialdir=initialdir
        , initialfile=initialfile
        , filetypes=filetypes
        )

    localRoot.destroy()

    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
# filesavebox
#-------------------------------------------------------------------
def filesavebox(msg=None
    , title=None
    , default=""
    , filetypes=None
    ):
    """
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    The "default" argument should contain a filename (i.e. the
    current name of the file to be saved).  It may also be empty,
    or contain a filemask that includes wildcards.

    The "filetypes" argument works like the "filetypes" argument to
    fileopenbox.
    """

    localRoot = Tk()
    localRoot.withdraw()

    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default,filetypes)

    f = tk_FileDialog.asksaveasfilename(parent=localRoot
        , title=getFileDialogTitle(msg,title)
        , initialfile=initialfile
        , initialdir=initialdir
        , filetypes=filetypes
        )
    localRoot.destroy()
    if not f: return None
    return os.path.normpath(f)


#-------------------------------------------------------------------
#
# fileboxSetup
#
#-------------------------------------------------------------------
def fileboxSetup(default,filetypes):
    if not default: default = os.path.join(".","*")
    initialdir, initialfile = os.path.split(default)
    if not initialdir : initialdir  = "."
    if not initialfile: initialfile = "*"
    initialbase, initialext = os.path.splitext(initialfile)
    initialFileTypeObject = FileTypeObject(initialfile)

    allFileTypeObject = FileTypeObject("*")
    ALL_filetypes_was_specified = False

    if not filetypes: filetypes= []
    filetypeObjects = []

    for filemask in filetypes:
        fto = FileTypeObject(filemask)

        if fto.isAll():
            ALL_filetypes_was_specified = True # remember this

        if fto == initialFileTypeObject:
            initialFileTypeObject.add(fto) # add fto to initialFileTypeObject
        else:
            filetypeObjects.append(fto)

    #------------------------------------------------------------------
    # make sure that the list of filetypes includes the ALL FILES type.
    #------------------------------------------------------------------
    if ALL_filetypes_was_specified:
        pass
    elif allFileTypeObject == initialFileTypeObject:
        pass
    else:
        filetypeObjects.insert(0,allFileTypeObject)
    #------------------------------------------------------------------
    # Make sure that the list includes the initialFileTypeObject
    # in the position in the list that will make it the default.
    # This changed between Python version 2.5 and 2.6
    #------------------------------------------------------------------
    if len(filetypeObjects) == 0:
        filetypeObjects.append(initialFileTypeObject)

    if initialFileTypeObject in (filetypeObjects[0], filetypeObjects[-1]):
        pass
    else:
        if runningPython26:
            filetypeObjects.append(initialFileTypeObject)
        else:
            filetypeObjects.insert(0,initialFileTypeObject)

    filetypes = [fto.toTuple() for fto in filetypeObjects]

    return initialbase, initialfile, initialdir, filetypes

#-------------------------------------------------------------------
# utility routines
#-------------------------------------------------------------------
# These routines are used by several other functions in the EasyGui module.

def __buttonEvent(event):
    """
    Handle an event that is generated by a person clicking a button.
    """
    global  boxRoot, __widgetTexts, __replyButtonText
    __replyButtonText = __widgetTexts[event.widget]
    boxRoot.quit() # quit the main loop


def __put_buttons_in_buttonframe(choices):
    """Put the buttons in the buttons frame
    """
    global __widgetTexts, __firstWidget, buttonsFrame

    __firstWidget = None
    __widgetTexts = {}

    i = 0

    for buttonText in choices:
        tempButton = Button(buttonsFrame, takefocus=1, text=buttonText)
        bindArrows(tempButton)
        tempButton.pack(expand=YES, side=LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')

        # remember the text associated with this widget
        __widgetTexts[tempButton] = buttonText

        # remember the first widget, so we can put the focus there
        if i == 0:
            __firstWidget = tempButton
            i = 1

        # for the commandButton, bind activation events to the activation event handler
        commandButton  = tempButton
        handler = __buttonEvent
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

#-----------------------------------------------------------------------
#
#     class EgStore
#
#-----------------------------------------------------------------------
class EgStore:
    r"""
A class to support persistent storage.

You can use EgStore to support the storage and retrieval
of user settings for an EasyGui application.


# Example A
#-----------------------------------------------------------------------
# define a class named Settings as a subclass of EgStore
#-----------------------------------------------------------------------
class Settings(EgStore):
::
    def __init__(self, filename):  # filename is required
        #-------------------------------------------------
        # Specify default/initial values for variables that
        # this particular application wants to remember.
        #-------------------------------------------------
        self.userId = ""
        self.targetServer = ""

        #-------------------------------------------------
        # For subclasses of EgStore, these must be
        # the last two statements in  __init__
        #-------------------------------------------------
        self.filename = filename  # this is required
        self.restore()            # restore values from the storage file if possible



# Example B
#-----------------------------------------------------------------------
# create settings, a persistent Settings object
#-----------------------------------------------------------------------
settingsFile = "myApp_settings.txt"
settings = Settings(settingsFile)

user    = "obama_barak"
server  = "whitehouse1"
settings.userId = user
settings.targetServer = server
settings.store()    # persist the settings

# run code that gets a new value for userId, and persist the settings
user    = "biden_joe"
settings.userId = user
settings.store()


# Example C
#-----------------------------------------------------------------------
# recover the Settings instance, change an attribute, and store it again.
#-----------------------------------------------------------------------
settings = Settings(settingsFile)
settings.userId = "vanrossum_g"
settings.store()

"""
    def __init__(self, filename):  # obtaining filename is required
        self.filename = None
        raise NotImplementedError()

    def restore(self):
        """
        Set the values of whatever attributes are recoverable
        from the pickle file.

        Populate the attributes (the __dict__) of the EgStore object
        from     the attributes (the __dict__) of the pickled object.

        If the pickled object has attributes that have been initialized
        in the EgStore object, then those attributes of the EgStore object
        will be replaced by the values of the corresponding attributes
        in the pickled object.

        If the pickled object is missing some attributes that have
        been initialized in the EgStore object, then those attributes
        of the EgStore object will retain the values that they were
        initialized with.

        If the pickled object has some attributes that were not
        initialized in the EgStore object, then those attributes
        will be ignored.

        IN SUMMARY:

        After the recover() operation, the EgStore object will have all,
        and only, the attributes that it had when it was initialized.

        Where possible, those attributes will have values recovered
        from the pickled object.
        """
        if not os.path.exists(self.filename): return self
        if not os.path.isfile(self.filename): return self

        try:
            f = open(self.filename,"rb")
            unpickledObject = pickle.load(f)
            f.close()

            for key in list(self.__dict__.keys()):
                default = self.__dict__[key]
                self.__dict__[key] = unpickledObject.__dict__.get(key,default)
        except:
            pass

        return self

    def store(self):
        """
        Save the attributes of the EgStore object to a pickle file.
        Note that if the directory for the pickle file does not already exist,
        the store operation will fail.
        """
        f = open(self.filename, "wb")
        pickle.dump(self, f)
        f.close()


    def kill(self):
        """
        Delete my persistent file (i.e. pickle file), if it exists.
        """
        if os.path.isfile(self.filename):
            os.remove(self.filename)
        return

    def __str__(self):
        """
        return my contents as a string in an easy-to-read format.
        """
        # find the length of the longest attribute name
        longest_key_length = 0
        keys = []
        for key in self.__dict__.keys():
            keys.append(key)
            longest_key_length = max(longest_key_length, len(key))

        keys.sort()  # sort the attribute names
        lines = []
        for key in keys:
            value = self.__dict__[key]
            key = key.ljust(longest_key_length)
            lines.append("%s : %s\n" % (key,repr(value))  )
        return "".join(lines)  # return a string showing the attributes


def _dummy():
    pass
#____________________________________________
#CUSTOM CLASS
#_______________________
class inputgui():    
    def inputstuff(self, title, msg_fileopenbox, file_type, file_extension, msg_enterbox):
        #Create time-stamp 'yearmonthdayhourminutesseconds'
        now = "".join([str(datetime.datetime.now())[0:4],str(datetime.datetime.now())[5:7],
                     str(datetime.datetime.now())[8:10],str(datetime.datetime.now())[11:13],
                     str(datetime.datetime.now())[14:16],str(datetime.datetime.now())[17:19],
                     str(datetime.datetime.now())[20:len(str(datetime.datetime.now()))-1]])
        #Select input file
        openfile = fileopenbox(title = title, msg = msg_fileopenbox, filetypes= file_type)
        if openfile[-4:] == file_extension:
            pass
        else:
            msgbox(msg ='NO OUTPUT PRODUCED\nMAKE SURE YOU USE AN ACCEPTED FILE FORMAT', title=title, ok_button='OK', image=None, root=None)
            raw_input("Press enter to continue")
            quit()
        filepath = os.path.dirname(os.path.abspath(openfile))
        #openfile_temp = os.path.abspath(openfile)        
        print "Input file: " + openfile + "\n"
        #Create default name for output directory from name of input file
        defname = re.match(r'.*\\(.+)\.txt',openfile).group(1)
        #Create name for project and replace illegal characters with "_" 
        nameproject = enterbox(msg = msg_enterbox, title = title, default = defname, strip = True, image = None, root = None)        
        nameproject = re.sub(r'[\s\\,\/,\.\?\!&\^\:\*]',"_",nameproject)
        #Create default location for output directory from current loication of input file, then select directory
        defdir = re.match(r'(.+)\\.+\.txt',openfile).group(1)
        savedir = diropenbox(msg = "Choose a directory to save output", title = "", default = defdir)
        if len(nameproject)>0:
            outdir = os.path.join(savedir, str(nameproject + "_" + str(now)))
        else:
            outdir = os.path.join(savedir , str(defname + "_" + str(now)))
        os.mkdir(outdir)
        #return openfile, outdir
        return openfile, outdir, filepath
#____________________________________________
# END CUSTOM CLASS
#_______________________




