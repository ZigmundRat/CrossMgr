#-----------------------------------------------------------------------
# Set translation locale.
#
import wx
locale = wx.Locale()

from Version import AppVerName

# Currently only CrossMgr has translation files
#import gettext
#initTranslationCalled = False
#def initTranslation():
#	global initTranslationCalled
#	if not initTranslationCalled:
#		gettext.install(AppVerName.split(None, 1), './locale', unicode=True)
#		initTranslationCalled = True
		
#initTranslation()

#-----------------------------------------------------------------------
# Monkey-patch font so we always fetch a default font face.
#
FontFace = 'Arial'
'''
class ArialFont( wx.Font ):
	class __init__( self, *args, **kwargs ):
		kwargs['faceName'] = 'Arial'
		super( ArialFont, self ).__init__( *args, **kwargs )
wx.Font = ArialFont
'''

import datetime
import os
import re
import sys
import math
import socket

timeoutSecs = None

DEFAULT_HOST = '127.0.0.1'

'''
wx.ICON_EXCLAMATION	Shows an exclamation mark icon.
wx.ICON_HAND	Shows an error icon.
wx.ICON_ERROR	Shows an error icon - the same as wxICON_HAND.
wx.ICON_QUESTION	Shows a question mark icon.
wx.ICON_INFORMATION	Shows an information (i) icon.
'''

def MessageOK( parent, message, title = '', iconMask = wx.ICON_INFORMATION, pos = wx.DefaultPosition ):
	dlg = wx.MessageDialog(parent, message, title, wx.OK | iconMask, pos)
	dlg.ShowModal()
	dlg.Destroy()
	return True
	
def MessageOKCancel( parent, message, title = '', iconMask = wx.ICON_QUESTION):
	dlg = wx.MessageDialog(parent, message, title, wx.OK | wx.CANCEL | iconMask )
	response = dlg.ShowModal()
	dlg.Destroy()
	return True if response == wx.ID_OK else False
	
def SetValue( st, value ):
	if st.GetValue() != value:
		st.SetValue( value )
		return True
	return False

def SetLabel( st, label ):
	if st.GetLabel() != label:
		st.SetLabel( label )
		return True
	return False

def formatTime( secs, highPrecision = False ):
	if secs is None:
		secs = 0
	if secs < 0:
		sign = '-'
		secs = -secs
	else:
		sign = ''
	f, ss = math.modf(secs)
	secs = int(ss)
	hours = int(secs // (60*60))
	minutes = int( (secs // 60) % 60 )
	secs = secs % 60
	if highPrecision:
		decimal = '.%02d' % int( f * 100 )
	else:
		decimal = ''
	if hours > 0:
		return "%s%d:%02d:%02d%s" % (sign, hours, minutes, secs, decimal)
	else:
		return "%s%02d:%02d%s" % (sign, minutes, secs, decimal)

def formatTimeGap( secs, highPrecision = False ):
	if secs is None:
		secs = 0
	if secs < 0:
		sign = '-'
		secs = -secs
	else:
		sign = ''
	f, ss = math.modf(secs)
	secs = int(ss)
	hours = int(secs // (60*60))
	minutes = int( (secs // 60) % 60 )
	secs = secs % 60
	if highPrecision:
		decimal = '.%02d' % int( f * 100 )
	else:
		decimal = ''
	if hours > 0:
		return "%s%dh%d'%02d%s\"" % (sign, hours, minutes, secs, decimal)
	else:
		return "%s%d'%02d%s\"" % (sign, minutes, secs, decimal)

def formatTimeCompressed( secs, highPrecision = False ):
	f = formatTime( secs, highPrecision )
	if f[0] == '0':
		return f[1:]
	return f
		
def formatDate( date ):
	y, m, d = date.split('-')
	d = datetime.date( int(y,10), int(m,10), int(d,10) )
	return d.strftime( '%B %d, %Y' )
		
def StrToSeconds( str = '' ):
	secs = 0.0
	for f in str.split(':'):
		try:
			n = float(f)
		except ValueError:
			n = 0.0
		secs = secs * 60.0 + n
	return secs
	
def SecondsToStr( secs = 0 ):
	secs = int(secs)
	return '%02d:%02d:%02d' % (secs // (60*60), (secs // 60)%60, secs % 60)

def SecondsToMMSS( secs = 0 ):
	secs = int(secs)
	return '%02d:%02d' % ((secs // 60)%60, secs % 60)

def getHomeDir():
	sp = wx.StandardPaths.Get()
	homedir = sp.GetUserDataDir()
	try:
		if os.path.basename(homedir) == '.CrossMgr':
			homedir = os.path.join( os.path.dirname(homedir), '.CrossMgrApp' )
	except:
		pass
	if not os.path.exists(homedir):
		os.makedirs( homedir )
	return homedir

def getDocumentsDir():
	sp = wx.StandardPaths.Get()
	return sp.GetDocumentsDir()
	
#------------------------------------------------------------------------
if 'WXMAC' in wx.Platform:
	try:
		topdirName = os.environ['RESOURCEPATH']
	except:
		topdirName = os.path.dirname(os.path.realpath(__file__))
	if os.path.isdir( os.path.join(topdirName, 'CrossMgrCameraImages') ):
		dirName = topdirName
	else:
		dirName = os.path.normpath(topdirName + '/../Resources/')
	if not os.path.isdir(dirName):
		dirName = os.path.normpath(topdirName + '/../../Resources/')
	if not os.path.isdir(dirName):
		raise Exception("Resource Directory does not exist:" + dirName)
else:
	try:
		dirName = os.path.dirname(os.path.abspath(__file__))
	except:
		dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
	
	if os.path.basename(dirName) in ['library.zip', 'MainWin.exe', 'CrossMgrCamera.exe']:
		dirName = os.path.dirname(dirName)
	if 'CrossMgrCamera?' in os.path.basename(dirName):
		dirName = os.path.dirname(dirName)
	if not os.path.isdir( os.path.join(dirName, 'CrossMgrCameraImages') ):
		dirName = os.path.dirname(dirName)

	if os.path.isdir( os.path.join(dirName, 'CrossMgrCameraImages') ):
		pass
	elif os.path.isdir( '/usr/local/CrossMgrCameraImages' ):
		dirName = '/usr/local'

imageFolder = os.path.join(dirName, 'CrossMgrCameraImages')

def getDirName():		return dirName
def getImageFolder():	return imageFolder

def GetPngBitmap( fname ):
	return wx.Bitmap( os.path.join(imageFolder, fname), wx.BITMAP_TYPE_PNG )
#------------------------------------------------------------------------

def disable_stdout_buffering():
	fileno = sys.stdout.fileno()
	temp_fd = os.dup(fileno)
	sys.stdout.close()
	os.dup2(temp_fd, fileno)
	os.close(temp_fd)
	sys.stdout = os.fdopen(fileno, "w", 0)
		
def readDelimitedData( s, delim ):
	buffer = s.recv( 4096 )
	while 1:
		nl = buffer.find( delim )
		if nl >= 0:
			yield buffer[:nl]
			buffer = buffer[nl+len(delim):]
		else:
			more = s.recv( 4096 )
			if more:
				buffer = buffer + more
			else:
				break
	yield buffer
	
if __name__ == '__main__':
	print(getImageFolder(), os.path.join(getImageFolder(), 'CrossMgrHeader.png'))
