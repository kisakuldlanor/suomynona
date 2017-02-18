# -*- coding: utf-8 -*-

'''
    Add-on
    Copyright (C) 2016

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urllib,urlparse,json

from resources.lib.scrapermods import cleantitle
from resources.lib.scrapermods import client
from resources.lib.scrapermods import directstream


class source:
    def __init__(self):
        self.domains = ['mvgee.com']
        self.base_link = 'http://mvgee.com'
        self.search_link = '/movies/watch-%s-online-free-%s'


    def movie(self, imdb, title, year):
        try:
            url = self.search_link % (cleantitle.geturl(title), year)
            url = urlparse.urljoin(self.base_link, url)

            url = client.request(url, output='geturl')

            url = re.findall('(?://.+?|)(/.+)', url)[0]
            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)

            h = {'User-Agent': client.agent()}

            r = client.request(url, headers=h, output='extended')

            try:
                u = client.parseDOM(r[0], 'form', ret='action', attrs = {'method': 'post'})[-1]
                u = urlparse.urljoin(self.base_link, u)

                p = zip(client.parseDOM(r[0], 'input', ret='name', attrs = {'type': 'hidden'}), client.parseDOM(r[0], 'input', ret='value', attrs = {'type': 'hidden'}))
                p = urllib.urlencode(dict(p))

                r = client.request(u, post=p, cookie=r[4], headers=h, output='extended')
            except:
                pass

            r = r[0]

            s = re.findall('"imdbId"\s*:\s*"(.+?)"\s*,\s*"season"\s*:\s*(\d+)\s*,\s*"provider"\s*:\s*"(.+?)"\s*,\s*"name"\s*:\s*"(.+?)"', r)

            for u in s:
                try:
                    url = '/io/1.0/stream?imdbId=%s&season=%s&provider=%s&name=%s' % (u[0], u[1], u[2], u[3])
                    url = urlparse.urljoin(self.base_link, url)

                    r = client.request(url)
                    r = json.loads(r)

                    url = [i['src'] for i in r['streams']]

                    for i in url:
                        try: sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'provider': 'Moviegee', 'url': i, 'direct': True, 'debridonly': False})
                        except: pass
                except:
                    pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            url = client.request(url, output='geturl')
            if 'requiressl=yes' in url: url = url.replace('http://', 'https://')
            else: url = url.replace('https://', 'http://')
            return url
        except:
            return


