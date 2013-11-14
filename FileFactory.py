#-------------------------------------------------------------------------------
# Name:        FileFactory
# Purpose:     Uploading file to FileFactory.com
#
# Author:      John Kenedy
#
# Created:     13/11/2013
# Copyright:   (c) John Kenedy 2013
# Licence:     Free license
#-------------------------------------------------------------------------------
import StringOps
import WebScrapperPT
import urllib

def Upload(filename, username, password):
    wc = WebScrapperPT.WebScrapperPT()

    wc.Download("http://www.filefactory.com");
    wc.Unredirect()
    response = wc.PostResponse("www.filefactory.com", "http://www.filefactory.com/member/signin.php", {
            "loginEmail": username,
            "loginPassword": password,
            "Submit": "Sign In"}, "http://www.filefactory.com/member/signin.php")
    cookies = response.info().getheaders("Set-Cookie")[0]
    if (cookies is None):
        return "Invalid Login"

    cookies = cookies[0:StringOps.IndexOf(cookies, ";", 0)]
    cookies = cookies.replace("auth=", "")
    cookies = urllib.unquote(cookies)
    wc.Redirect()
    login = wc.Download("http://www.filefactory.com/account")
    if (StringOps.LastIndexOf(login, username) < 0):
        return "Invalid Login"

    result = wc.UploadFile("http://upload.filefactory.com/upload-beta.php", "Filedata", filename, { "cookie" : cookies }, "http://www.filefactory.com/upload/")
    result2 = wc.Download("http://www.filefactory.com/upload/results.php?files=" + result);

    search = "<tr id=\"row_" + result
    s = StringOps.IndexOf(result2, search, 0)
    e = StringOps.IndexOf(result2, "</tr>", s + len(search))
    NewUrls = []
    if (s != -1 and e != -1):
        link = result2[s + len(search) : (s + len(search)) + (e - s - len(search))]
        link = StringOps.TagMatch(link, 'href="', '"')
        if (len(link) > 0):
            NewUrls.append(link[0])

    return StringOps.StringJoin(",", NewUrls)