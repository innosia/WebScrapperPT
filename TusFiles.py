#-------------------------------------------------------------------------------
# Name:        Tusfiles
# Purpose:     Uploading to tusfiles.net
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
    datax = {
            "op":"login",
            "redirect": "",
            "login":username,
            "password":password
            }
    login = wc.Post("tusfiles.net", "http://tusfiles.net", datax, "http://tusfiles.net");
    if (StringOps.IndexOf(login, "My Account", 0) <= 0):
        return "Invalid Login"
    login = wc.Download("http://tusfiles.net")
    uploadurl = StringOps.TagMatchSingle(login, "return StartUpload(this);", "action=\"", "\"");
    uid = StringOps.RandomDigit(12)
    uploadurl = uploadurl + uid + "&js_on=1&utype=reg&upload_type=file";
    sessionid = StringOps.TagMatchSingle(login, "name=\"sess_id\"", "value=\"", "\"");
    tmpurl = StringOps.TagMatchSingle(login, "name=\"srv_tmp_url\"", "value=\"", "\"");

    data = { "upload_type" : "file", "sess_id" : sessionid, "srv_tmp_url" : tmpurl, "tos" : "1" }
    result2 = wc.UploadFile(uploadurl, "file_1", filename, data, "http://tusfiles.net")
    search = "<textarea name='fn'>"
    start = StringOps.IndexOf(result2, search, 0);
    NewUrls = []
    while (start != -1):
        if (start == -1): break;
        if (start + len(search) >= len(result2)): break;
        end = StringOps.IndexOf(result2, "<", start + len(search));
        if (end == -1): break;
        url = result2[start + len(search): (start + len(search)) + (end - start - len(search))];
        url = "http://tusfiles.net/" + url;
        NewUrls.append(url);
        start = StringOps.IndexOf(result2, search, end + 1);

    return StringOps.StringJoin(",", NewUrls)