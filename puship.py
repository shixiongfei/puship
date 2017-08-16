#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  Copyright (c) 2017 Xiongfei Shi <jenson.shixf@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
  
        http://shixf.com/
'''

import subprocess

try:
    # for py3
    from urllib.request import urlopen, Request, HTTPError, URLError
except:
    # for py2
    from urllib2 import urlopen, Request, HTTPError, URLError

try:
    # for py3
    from urllib.parse import urlencode
except:
    # for py2
    from urllib import urlencode


pushover_token = 'APP_TOKEN'
pushover_user = 'USER_KEY'


def _url_read(url, postdata=None, method=None):
    result = None

    if not postdata is None:
        postdata = urlencode(postdata).encode()

    try:
        req = Request(url, data=postdata)

        req.add_header('User-Agent', 'PushIP/1.0 (jenson.shixf@gmail.com)')
        req.add_header('Content-type', 'application/x-www-form-urlencoded')

        if not method is None:
            req.get_method = lambda: method
        
        urlItem = urlopen(req, timeout=10)
        result = urlItem.read()
        urlItem.close()
    except URLError as e:
        print('URLError: {0}'.format(e.reason))
    except HTTPError as e:
        print('HTTPError: {0}'.format(e.reason))
    except Exception as e:
        print('FetchError: HTTP data fetch error: {0}'.format(e))

    return result

def _command(cmd_str):
    child = subprocess.Popen(cmd_str, stdout = subprocess.PIPE, shell = True)
    return child.communicate()[0]

def _get_hostname():
    return _command('cat /etc/hostname').replace('\n', '')

def _get_lanip():
    return _command('hostname -I').replace('\n', '')

def _get_wanip():
    myip = _url_read('http://shixf.com/api/getip')
    if myip is None:
        return '0.0.0.0'
    return myip

def get_message():
    hostname = _get_hostname()
    lanip = _get_lanip()
    wanip = _get_wanip()

    return ('Hostname: {0}\n'
            'LanIP: {1}\n'
            'WanIP: {2}').format(hostname, lanip, wanip)

def pushover(msg):
    return _url_read('https://api.pushover.net/1/messages.json',
                     postdata = {
                        'token': pushover_token,
                        'user': pushover_user,
                        'message': msg
                     })

if __name__ == '__main__':
    pushover(get_message())
