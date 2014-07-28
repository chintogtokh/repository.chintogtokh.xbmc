import urllib,urllib2,re,sys,socket,xbmcplugin,xbmcgui,htmllib
#import urlresolver Unforunately not working

#[(url,show)]
def getSouthparkEpisodes(url):
        res=[]
        f=urllib.urlopen(url)
        a=f.read()
        f.close()
        p=re.compile(r'previewDescriptionTitle\" href=\"(.+)\">(.+)</a>')
        match=p.findall(a)
        for url,name in match:
                episodeNum = re.split(r'[?=&]+',url)
                f=urllib.urlopen("http://allsp.ch/xml.php?id="+episodeNum[2])
                a=f.read()
                f.close()
                p=re.compile(r'<location>(.+)</location>')
                match = p.findall(a)
                streamURL = match[0]
                print episodeNum
                res.append((streamURL,episodeNum[2] + ": " + name))
        return res

def getParams():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
        return param

       
def addLink(name,url):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
def showCats():
        cat=[]
        for i in xrange(1,20):
                try:
                        cat.append(("http://allsp.ch/episodes.php?season=" + str(i),"Season " + str(i)))
                except:
                        pass
        for url,name in cat:
                addDir(name,url,1)

def showEpisodes(url,name):
        print name
        shows=getSouthparkEpisodes(url)
        for url,name in shows:
                if(url.find("iframe")>-1):
                        url=url[6:]
                        # print url
                        # newurl=urlresolver.resolve(url)
                        # if(newurl):
                        #         url = newurl
                        #         addLink(name,url)
                        # else:
                        #         print "Couldn't resolve"
                        addLink("[Video unsupported] " + name,url)
                else:
                        addLink(name,url)
        
params=getParams()
url=None
name=None
mode=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print "Showing seasons"
        showCats()
elif mode==1:
        try:
                print "Showing episodes : "+url
                showEpisodes(url,name)
        except:
                pass

xbmcplugin.endOfDirectory(int(sys.argv[1]))