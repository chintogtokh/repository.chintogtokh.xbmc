import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import os

addon_handle = int(sys.argv[1])
base_url = sys.argv[0]

__settings__ = xbmcaddon.Addon(id='plugin.video.mongoltv')
rootDir = xbmc.translatePath(__settings__.getAddonInfo('path')).decode('utf-8')
image_dir = os.path.join(rootDir, 'resources', 'media')

print image_dir

xbmcplugin.setContent(addon_handle, 'videos')

names = ['UBS One','UBS Global', 'UBS Music','MNB 1','MNB 2','TV5','Education TV','Olloo']
urls = ['rtmp://202.131.233.170/live/ubslive2009',
	'rtmp://202.131.233.170/live1/ubslive',
	'rtmp://202.131.233.170/live3/ubslive2010',
	'rtmp://202.21.117.233/mnb/livestream',
	'rtmp://202.21.117.233/mn2/livestream',
	'rtmp://202.131.225.109/live/livestream',
	'rtmp://103.11.192.165/livepkgr//livestream',
	'rtmp://etv.olloo.mn:8000/live/livestream',
	]
icons=['ubs1.png','ubsglobal.png','ubsmusic.png','mnb1.png','mnb2.png','tv5.png','edutv.png','olloo.png']

for name,url,icon in zip(names,urls,icons):
	li = xbmcgui.ListItem(label=name, path=url)
	li.setThumbnailImage(os.path.join(image_dir,icon))
	li.setIconImage(os.path.join(image_dir,icon))
	li.setInfo(type='Video', infoLabels={ "Title": name })
	li.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

xbmcplugin.endOfDirectory(addon_handle)