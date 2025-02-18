#
#       Copyright (C) 2014-
#       Sean Poyser (seanpoyser@gmail.com)
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import sys
import xbmc
import xbmcgui
import xbmcaddon
import os
import pickle
from shortlistitem import ShortlistItem
from database import *

__addon__       = xbmcaddon.Addon(id='plugin.program.shortlist')

# if __name__ == '__main__':
def main():
    lst = listDatabases()

    dialog = xbmcgui.Dialog()
    ret = dialog.contextmenu(lst)

    if ret != -1:
        dbNice = lst[ret]
        dbName = dbNice.lower() + ".db"
        #xbmc.log( dbName, xbmc.LOGNOTICE);

        videoInfoTag = sys.listitem.getVideoInfoTag()

        item = ShortlistItem()
        item.filename = xbmc.getInfoLabel('ListItem.FilenameAndPath')
        # item.filename = sys.listitem.getfilename()
        item.title = sys.listitem.getLabel()
        item.duration = sys.listitem.getProperty('duration')
        item.rating = videoInfoTag.getRating()
        item.year = videoInfoTag.getYear()
        item.date = videoInfoTag.getPremiered()
        item.plot = videoInfoTag.getPlot()
        item.plotoutline = videoInfoTag.getPlotOutline()
        item.thumb = sys.listitem.getArt( 'thumb' )
        item.poster = sys.listitem.getArt( 'poster' )
        item.fanart = sys.listitem.getArt( 'fanart' )
        item.banner = sys.listitem.getArt( 'banner' )
        item.clearart = sys.listitem.getArt( 'clearart' )
        item.clearlogo = sys.listitem.getArt( 'clearlogo' )
        item.landscape = sys.listitem.getArt( 'landscape' )
        item.icon = sys.listitem.getArt( 'icon' )
        item.genre = videoInfoTag.getGenre()
        item.votes = videoInfoTag.getVotes()
        item.mpaa = xbmc.getInfoLabel('ListItem.Mpaa')
        item.writer = xbmc.getInfoLabel('ListItem.Writer')
        item.director = xbmc.getInfoLabel('ListItem.Director')

        if sys.argv[1] == "folder":
            item.is_folder = True

        result = addItemToDatabase( dbName, item )

        if result:
            title = "Added"
            message = "'%s' to %s" % (item.title, dbNice)
        else:
            lst = ['Keep','Remove']
            ret = dialog.contextmenu(lst)

            if ret == 0:
                # Keep
                title = "Kept"
                message = "'%s' in %s" % (item.title, dbNice)
            elif ret == 1:
                # Delete
                deleteItemFromDatabase( dbName, item.filename )
                title = "Deleted"
                message = "'%s' from %s" % (item.title, dbNice)

        xbmc.executebuiltin("Notification(\"%s\", \"%s\")" % (title, message) )

main()

