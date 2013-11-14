#-------------------------------------------------------------------------------
# Name:        WebScrapperPT
# Purpose:     Make uploading, downloading via HTTP easy, storing cookies
#              and make next download sending the same cookie in headers
# Author:      John Kenedy
#
# Created:     11/11/2013
# Copyright:   (c) John Kenedy 2013
# Licence:     Free License
#-------------------------------------------------------------------------------
import cookielib
import urllib2
import urllib
import httplib
import StringOps
import mimetypes

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

class WebScrapperPT():
    UserAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11"
    CookieJar = None
    Cookies = None
    Opener = None
    ProxyUrl = ""
    ProxyUrlRaw = ""
    ProxyUrlPort = 80
    ProxyUsername = ""
    ProxyPassword = ""
    IsRedirect = 1
    SetAuth = None

    def Download(self, url, referer=""):
        self.SetOpener()
        req = urllib2.Request(url)
        if (referer):
            req.add_header('Referer', referer)
        response = self.Opener.open(req)
        html = response.read()
        return html

    def Unredirect(self):
        self.IsRedirect = 0

    def Redirect(self):
        self.IsRedirect = 1

    def UrlExist(host, path="/"):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path)
            return conn.getresponse().status
        except StandardError:
            return None
        return None

    def Post(self, host, url, nvc, referer=""):
        self.SetOpener()

        if(type(nvc) is dict):
            encoded_nvc = urllib.urlencode(nvc)
        else:
            encoded_nvc = nvc
        req = urllib2.Request(url, encoded_nvc, self.GetHeader(host))
        if (referer):
            req.add_header('Referer', referer)
        try:
            response = self.Opener.open(req)
            html = response.read()
        except Exception,e:
            html = str(e)
        return html

    def PostResponse(self, host, url, nvc, referer=""):
        self.SetOpener()

        if(type(nvc) is dict):
            encoded_nvc = urllib.urlencode(nvc)
        else:
            encoded_nvc = nvc
        req = urllib2.Request(url, encoded_nvc, self.GetHeader(host))
        if (referer):
            req.add_header('Referer', referer)
        try:
            response = self.Opener.open(req)
        except Exception,e:
            return None
        return response

    #proxyurl ProxyURL:ProxyPORT
    #proxyurlraw ProxyURLONLY
    #proxyurlport ProxyPORTONLY
    def Initialize(self, proxyurl="", proxyurlraw="", proxyurlport=8080, username="", password=""):
        self.ProxyUrl = proxyurl
        self.ProxyUrlRaw = proxyurlraw
        self.ProxyUrlPort = proxyurlport
        self.ProxyUsername = username
        self.ProxyPassword = password
        self.CookieJar = cookielib.CookieJar()
        self.Cookies = urllib2.HTTPCookieProcessor(self.CookieJar)

    def SetOpener(self):
        if (self.Cookies is None):
            self.CookieJar = cookielib.CookieJar()
            self.Cookies = urllib2.HTTPCookieProcessor(self.CookieJar)
        if (self.ProxyUrl):
            if (self.ProxyUsername is None or self.ProxyUsername == ""):
                auth = "http://" + self.ProxyUsername + ":" + self.ProxyPassword +"@" + self.ProxyUrl
            else:
                auth = "http://" + self.ProxyUsername + ":" + self.ProxyPassword +"@" + self.ProxyUrl

            handler = urllib2.ProxyHandler({'http' : auth})

            if (self.IsRedirect == 1):
                self.Opener = urllib2.build_opener(handler, urllib2.HTTPRedirectHandler(), urllib2.HTTPHandler(debuglevel=0), urllib2.HTTPSHandler(debuglevel=0), self.Cookies)
            else:
                self.Opener = urllib2.build_opener(handler, NoRedirectHandler(), self.Cookies)
        else:
            if (self.IsRedirect == 1):
                self.Opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPHandler(debuglevel=0), urllib2.HTTPSHandler(debuglevel=0), self.Cookies)
            else:
                self.Opener = urllib2.build_opener(NoRedirectHandler(), self.Cookies)

        if (self.UserAgent):
            self.Opener.addheaders = [('User-agent', self.UserAgent)]
        urllib2.install_opener(self.Opener)

    def GetHeader(self, host):
        http_header = {
                "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
                "Accept-Language" : "en-us,en;q=0.5",
                "Accept-Charset" : "ISO-8859-1",
                "Content-type": "application/x-www-form-urlencoded",
                "Host" : host
                }
        return http_header

    def GetCookieString(self):
        result = ""
        for cookie in self.CookieJar:
            if (result != ""):
                result = result +"; " + cookie.name + "=" + cookie.value
            else:
                result = cookie.name + "=" + cookie.value
        return result

    def encode_multipart_data(self, url, data, files, referer):
        boundary = StringOps.RandomChar(30)

        host = StringOps.TagMatch(url, "//", "/")[0]
        def get_content_type (filename):
        	return mimetypes.guess_type (filename)[0] or 'application/octet-stream'

        def encode_field (field_name):
        	return ('--' + boundary,
        	        'Content-Disposition: form-data; name="%s"' % field_name,
        	        '', str (data [field_name]))

        def encode_file (field_name):
        	filename = files[field_name]
        	return ('--' + boundary,
        	        'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
        	        'Content-Type: %s' % get_content_type(filename),
        	        '', open(filename, 'rb').read ())

        lines = []
        if (data):
            for name in data:
        	   lines.extend(encode_field(name))
        for name in files:
        	lines.extend(encode_file(name))
        lines.extend (('--%s--' % boundary, ''))
        body = '\r\n'.join(lines)

        cookie = self.GetCookieString()
        if (self.UserAgent is None):
            headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
                       'Cookie': cookie,
                       'Origin': referer,
                       'Referer': referer,
                       'Host' : host,
                       'content-length': str(len(body))}
        else:
            headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
                       'Cookie': cookie,
                       'Origin': referer,
                       'Referer': referer,
                       'Host' : host,
                       'User-agent': self.UserAgent,
                       'content-length': str(len(body))}

        return body, headers

    def UploadFile(self, url, filekey, filename, nvc, referer):
    	data = nvc
    	files = {filekey : filename}

        self.SetOpener()
        req = urllib2.Request(url)
        connection = httplib.HTTPConnection(req.get_host())
        connection.request('POST', req.get_selector(), *self.encode_multipart_data(url, data, files, referer))

        response = connection.getresponse()
        html = response.read()
        return html
