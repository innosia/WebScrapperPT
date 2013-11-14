#-------------------------------------------------------------------------------
# Name:        RapidGator
# Purpose:     Uploading file to RapidGator.net
#
# Author:      John Kenedy
#
# Created:     13/11/2013
# Copyright:   (c) John Kenedy 2013
# Licence:     Free License
#-------------------------------------------------------------------------------
import WebScrapperPT
import StringOps
import time

def Upload(filename, username, password):
    wc = WebScrapperPT.WebScrapperPT()
    datax = {
            "LoginForm[email]":username,
            "LoginForm[password]":password,
            "LoginForm[rememberMe]":"0",
            "LoginForm[rememberMe]":"1",
            "LoginForm[verifyCode]":""
            }
    test = wc.Download("http://rapidgator.net/")
    login = wc.Post("rapidgator.net", "https://rapidgator.net/auth/login", datax, "https://rapidgator.net/");
    if (StringOps.IndexOf(login, "Account:", 0) <= 0):
        return "Invalid Login"

    urls = StringOps.TagMatch(login, "var form_url = \"", "\"");
    if (len(urls) <= 0):
        return "Invalid Login Url"

    uid = StringOps.RandomDigitHex(32)
    uploadurl = urls[0] + uid + "&folder_id=0"
    NewUrls = []
    result2 = wc.UploadFile(uploadurl, "file", filename, None, "")
    unixTime = str(int(time.mktime(time.gmtime())))
    checkurl = urls[0].replace("&X-Progress-ID=","") + "/jsonprogress&data%5B0%5D%5Buuid%5D=" + uid + "&data%5B0%5D%5Bstart_time%5D=" + unixTime
    w2 = wc.Download(checkurl, "")
    dlurl = StringOps.TagMatch(w2, "download_url\":\"", "\"")
    if (len(dlurl) > 0):
        NewUrls.append(dlurl[0].replace("\\", ""))

    return StringOps.StringJoin(",", NewUrls)