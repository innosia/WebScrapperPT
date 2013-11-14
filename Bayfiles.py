#-------------------------------------------------------------------------------
# Name:        Bayfiles
# Purpose:     Uploading to Bayfiles.net
#
# Author:      John Kenedy
#
# Created:     13/11/2013
# Copyright:   (c) John Kenedy 2013
# Licence:     Free license
#-------------------------------------------------------------------------------
import WebScrapperPT
import StringOps

def Upload(filename, username, password):
    wc = WebScrapperPT.WebScrapperPT()
    login = wc.Download("http://www.bayfiles.net")
    login = wc.Download("http://api.bayfiles.net/v1/account/login/" + username + "/" + password);
    login = wc.Download("http://bayfiles.net/account/files")
    if (StringOps.IndexOf(login, "Your files", 0) <= 0):
        return "Invalid Login"

    login = wc.Download("http://tusfiles.net")
    sessionid = ""
    for ck in wc.CookieJar:
        if (ck.name == "SESSID"):
            sessionid = ck.value
    r = wc.Download("http://api.bayfiles.net/v1/file/uploadUrl?session=" + sessionid);
    uploadurls = StringOps.TagMatch(r, "\"uploadUrl\":\"", "\"")
    if (len(uploadurls) <= 0):
        return "Invalid upload url"
    uploadurl = uploadurls[0].replace("\\", "")
    result2 = wc.UploadFile(uploadurl, "file", filename, None, "")
    downloadurls = StringOps.TagMatch(result2, "\"downloadUrl\":\"", "\"")

    return StringOps.StringJoin(",", downloadurls).replace("\\", "")