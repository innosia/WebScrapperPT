#-------------------------------------------------------------------------------
# Name:        UppIt
# Purpose:     Uploading file to UppIt.com
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
            "redirect":"/?op=my_files",
            "login":username,
            "password":password,
            }
    login = wc.Post("Uppit.com", "http://Uppit.com", datax, "");
    if (StringOps.IndexOf(login, "Account Settings", 0) <= 0):
        return "Invalid Login"

    login = wc.Download("http://Uppit.com")
    urls = StringOps.TagMatchSingle(login, "return StartUpload(this);", "action=\"", "\"");
    if (urls == False):
        return "Invalid Login Url"

    uid = StringOps.RandomDigit(12)
    uploadurl = urls + uid + "&js_on=1&utype=reg&upload_type=file"
    tmpurl = StringOps.TagMatchSingle(login, "\"srv_tmp_url\"", "value=\"", "\"")
    sessid  = StringOps.TagMatchSingle(login, "\"sess_id\"", "value=\"", "\"")

    NewUrls = []
    nvc = {
        "upload_type":"file",
        "sess_id":sessid,
        "srv_tmp_url":tmpurl,
        "tos":"1"
    }
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
        url = "http:///Uppit.com/" + url;
        NewUrls.append(url);
        start = StringOps.IndexOf(result2, search, end + 1);

    return StringOps.StringJoin(",", NewUrls)