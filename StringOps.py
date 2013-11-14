#-------------------------------------------------------------------------------
# Name:        StringOps
# Purpose:     String manipulations
#
# Author:      John Kenedy
#
# Created:     11/11/2013
# Copyright:   (c) John Kenedy 2013
# Licence:     Free License
#-------------------------------------------------------------------------------
import string
import random
import ntpath

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def GetFilename(path):
    head, tail = ntpath.split(path)
    result = tail or ntpath.basename(head)
    return result

def StripHTML(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def IndexOf(webContent, tagStart, startPos):
    webContent = webContent.upper()
    tagStart = tagStart.upper()
    try:
        start = webContent.index(tagStart, startPos)
    except ValueError:
        start = -1
    return start

def LastIndexOf(webContent, tagStart):
    webContent = webContent.upper()
    tagStart = tagStart.upper()
    try:
        start = webContent.rindex(tagStart)
    except ValueError:
        start = -1
    return start

def TagMatch(webContent, tagStart, tagEnd):
    rs = []
    search = tagStart
    start = IndexOf(webContent, tagStart, 0)
    end = 0
    while (start != -1):
        if (start == -1):
            break
        if (start + len(search) >= len(webContent)):
            break
        end = IndexOf(webContent, tagEnd, start + len(search))
        if (end == -1):
            break
        temp = webContent[start + len(search): (start + len(search)) + (end-start-len(search))]
        rs.append(temp)
        start = IndexOf(webContent, search, end + len(tagEnd))
    return rs

def TagMatchSkip(webContent, tagStart, tagEnd, skipStart):
    rs = []
    search = tagStart
    start = IndexOf(webContent, tagStart, 0)
    end = 0
    skip = 0
    while (start != -1):
        if (start == -1):
            break
        if (start + len(search) >= len(webContent)):
            break
        end = IndexOf(webContent, tagEnd, start + len(search))
        if (end == -1):
            break

        skip = IndexOf(webContent, skipStart, start + len(search))
        tempStart = skip
        skipcount = 0
        while (skip != -1):
            if (skip < end):
                print tempStart
                inbetween = webContent[tempStart : (tempStart) + (end - tempStart)]
                counts = inbetween.split(skipStart)
                if (len(counts) != 0 and len(counts) > 1):
                    skipcount = skipcount + len(counts) - 2
                tempStart = end + len(tagEnd)
                end = IndexOf(webContent, tagEnd, tempStart)
                skip = IndexOf(webContent, skipStart, tempStart)
            else:
                break
        if (end == -1):
            break
        for i in xrange(skipcount):
            end = IndexOf(webContent, tagEnd, end + len(tagEnd))
            if(end == -1):
                break
        if (end == -1):
            break

        temp = webContent[start + len(search) : (start + len(search)) + (end - start - len(search))]
        rs.append(temp)

        start = IndexOf(webContent, search, end + len(tagEnd))
    return rs


def TagMatchFromBehind(webContent, tagStart, tagEnd):
    endPost = -1
    endPost = LastIndexOf(webContent, tagEnd)
    result = []
    data = webContent
    while (endPost >= 0):
        data = data[0:0 + endPost]
        startPos = LastIndexOf(data, tagStart)
        if (startPos == -1):
            break
        dt = ""
        if (startPos + len(tagStart) + (endPost - (startPos + len(tagStart))) <= len(data)):
            dt = data[startPos + len(tagStart) : (startPos + len(tagStart)) + (endPost - (startPos + len(tagStart)))]
            result.insert(0, dt)
            if (startPos > 0):
                data = data[0:0 + startPos]
            else:
                break
        endPost = LastIndexOf(data, tagEnd)
    return result

def GetTag(content, index):
    if (index < 0): return ""
    s = 0
    e = 0
    tag = ""
    for i in xrange(index,-1,-1):
        if (content[i] == "<"):
            s=i
            break

    for i in xrange(index,len(content)):
        if(content[i] == ">"):
            e = i
            break

    str = content[s:s + (e - s) + 1]
    return str;

def SingleTagMatch(content, search, endsearch):
    s = IndexOf(content, search, 0)
    if (s == -1): return ""
    e = IndexOf(content, endsearch, s + len(search))
    if (e == -1): return ""
    return content[s + len(search): (s + len(search)) + (e - s - len(search))]

def RandomDigit(size=12):
    return ''.join(random.choice(string.digits) for x in range(size))

def RandomChar(size=12):
    return ''.join(random.choice(string.ascii_uppercase) for x in range(size))

def RandomDigitHex(size=12):
    return ''.join(random.choice(string.digits + "abcdef") for x in range(size))

def TagMatchSingle(content, containing, attributestart, attributeend):
    s = IndexOf(content, containing, 0)
    if (s == -1): return ""
    tag = GetTag(content, s)
    result = SingleTagMatch(tag, attributestart, attributeend)
    return result

def StringJoin(delimiter, strings):
    return string.join(strings, delimiter)
