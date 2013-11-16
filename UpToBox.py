#-------------------------------------------------------------------------------
# Name:        UptoBox
# Purpose:     Uploading file to UptoBox.com
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
            "op":"login",
            "redirect":"",
            "login":username,
            "password":password,
            }
    test = wc.Download("http://uptobox.com/login.html")
    login = wc.Post("uptobox.com", "http://uptobox.com/", datax, "http://uptobox.com/login.html");
    if (StringOps.IndexOf(login, "Check my reports downloads", 0) <= 0):
        return "Invalid Login"

    login = wc.Download("http://uptobox.com")
    urls = StringOps.TagMatchFromBehind(login, "\"", ".uptobox.com/cgi-bin/upload.cgi?upload_id=");
    if (len(urls) <= 0):
        return "Invalid Login Url"

    uid = StringOps.RandomDigit(12)
    uploadurl = urls[0] + ".uptobox.com/cgi-bin/upload.cgi?upload_id=" + uid + "&js_on=1&utype=reg&upload_type=file"
    tmpurl = StringOps.TagMatchSingle(login, "\"srv_tmp_url\"", "value=\"", "\"")
    sessid  = StringOps.TagMatchSingle(login, "\"sess_id\"", "value=\"", "\"")

    NewUrls = []
    nvc = {
        "upload_type":"file",
        "sess_id":sessid,
        "srv_tmp_url":tmpurl,
        "tos":"checked"
    }
    print nvc
    print uploadurl
    result2 = wc.UploadFile(uploadurl, "file_0", filename, nvc, "")

    search = "<textarea name='fn'>"
    start = StringOps.IndexOf(result2, search, 0);
    NewUrls = []
    while (start != -1):
        if (start == -1): break;
        if (start + len(search) >= len(result2)): break;
        end = StringOps.IndexOf(result2, "<", start + len(search));
        if (end == -1): break;
        url = result2[start + len(search): (start + len(search)) + (end - start - len(search))];
        url = "http://www.uptobox.com/" + url;
        NewUrls.append(url);
        start = StringOps.IndexOf(result2, search, end + 1);

    return StringOps.StringJoin(",", NewUrls)