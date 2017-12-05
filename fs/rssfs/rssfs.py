#~ # coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import feedparser
# ~ import urllib2
from six.moves.urllib.request import urlopen
from .. import errors
from ..base import FS
from ..info import Info
from ..mode import Mode
from ..path import join, dirname, split
from ..enums import ResourceType
from ..permissions import Permissions

class RSSFS(FS):
    
    """A filesystem over SMB.

    Arguments:
        host (str): the IP or NetBIOS hostname of the server.
        username (str): the username to connect with. Use `None` to
            connect anonymously. **[default: None]**
        passwd (str): the password to connect with. Set to `None` to connect
            anonymously. **[default: None]**
        timeout (int): the timeout of network operations, in seconds. Used for
            both NetBIOS and SMB communications. **[default: 15]**
        port (int): the port the SMB server is listening to. Often ``139`` for
            SMB over NetBIOS, sometimes ``445`` for an SMB server over direct
            TCP. **[default: 139]**
        name_port (int): the port the NetBIOS naming service is listening on.
            **[default: 137]**
        direct_tcp (int): set to True to attempt to connect directly to the
            server using TCP instead of NetBIOS. **[default: False]**

    Raises:
        `fs.errors.CreateFailed`: if the filesystem could not be created.

    Example:
        >>> import fs
        >>> smb_fs = fs.open_fs('smb://SOMESERVER/share')

    """

    _meta = {
        'case_insensitive': True,
        'invalid_path_chars': '\0"\[]+|<>=;?*',
        'network': True,
        'read_only': True,
        'thread_safe': False, # FIXME: make that True
        'unicode_paths': True,
        'virtual': False,
    }


    def __init__(self, url):
        super(RSSFS, self).__init__()
        self._url = url
        self._parser = feedparser.parse(self._url)
        self._title = self._parser['feed']['title']


    def __str__(self):
        return 'RSSFS: %s'%self._url
        
    def _find_entry(self,path):

        found = None
        if not path.startswith('/%s'%self._title):
            return None
            
        filepath = path.replace('/%s/'%self._title,'')
        
        for entry in self._parser['entries']:
            if filepath == u'%s.html'%entry['title']:
                return entry
                
        return None
    
        
    def listdir(self,path):
        _path = self.validatepath(path)

        if _path in [u'/',u'.',u'./']:

            return [self._title]
        elif _path in [u'/%s'%self._title]:
            self._parser = feedparser.parse(self._url)
            outlist = []
            for entry in self._parser['entries']:
                outlist.append(u'%s.html'%entry['title'])
            #~ print 'out',outlist
            return outlist
        else:
            pass
        #~ print 'error'
        raise errors.ResourceNotFound(path)

    def getinfo(self, path, namespaces=None):
        _path = self.validatepath(path)

        namespaces = namespaces or ()
        
        if _path == '/':
            return Info({
                "basic":
                {
                    "name": "",
                    "is_dir": True
                },
                "details":
                {
                    "type": int(ResourceType.directory)
                }
                })
                
        elif path == '/%s'%self._title:
            return Info({
                "basic":
                {
                    "name": self._title,
                    "is_dir": True
                },
                "details":
                {
                    "type": int(ResourceType.directory)
                }
                })

        else:

            found = self._find_entry(_path)

            if found:
                #~ print found
                return Info({
                    "basic":
                    {
                        "name": u'%s.html'%found['title'],
                        "is_dir": False
                    },
                    "details":
                    {
                        "type": int(ResourceType.file),
                        "size":len(str('a')),
                    }
                    })
        #~ print 'error'
        raise errors.ResourceNotFound(path)

    def openbin(self, path, mode=u'r',*args,**kwargs):
        _path = self.validatepath(path)
        
        if not 'r' in mode:
            raise errors.Unsupported()
            
        found = self._find_entry(_path)
        if found:
            #~ try:
            response = urlopen(found['link'])
            #~ except Exception as e:
                #~ exstring = """<!doctype html> <head> </head> <body> %s</body> </html>
                #~ """%str(e)
                #~ return io.BytesIO(exstring)
            #~ html = response.read()
            #~ f = io.BytesIO(html)

            def writable():
                if self._meta['read_only']:
                    return False
                else:
                    return True
            
            def seekable():
                return False
                
            response.writable = writable
            response.seekable = seekable
            
            return response
            
        raise errors.ResourceNotFound(path)



    def makedir(self,*args,**kwargs):
        raise errors.Unsupported()
    def remove(self,*args,**kwargs):
        raise errors.Unsupported()
    def removedir(self,*args,**kwargs):
        raise errors.Unsupported()
    def setinfo(self,*args,**kwargs):
        raise errors.Unsupported()
