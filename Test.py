#-------------------------------------------------------------------------------
# Name:        Test.py
# Purpose:     Main purpose for testing scripts
#
# Author:      John Kenedy
#
# Created:     11/11/2013
# Copyright:   (c) John Kenedy 2013
# Licence:     Free License
#-------------------------------------------------------------------------------
import StringOps
import WebScrapperPT
import socks
import socket
import TusFiles
import FileFactory
import RapidGator
import Bayfiles

def create_connection(address, timeout=None, source_address=None):
    sock = socks.socksocket()
    sock.connect(address)
    return sock

def main():
    #--------------------------------------------------------------------------------------------------
    # USE SOCKS library (must install SocksiPy)
    #socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, "127.0.0.1", 1080)
    #socket.socket = socks.socksocket
    #socket.create_connection = create_connection
    #--------------------------------------------------------------------------------------------------

    result = Bayfiles.Upload("F:\\makan.zip", "user id", "password")
    #result = RapidGator.Upload("F:\\makan.zip", "user id", "password")
    #result = FileFactory.Upload("F:\\makan.txt", user id", "password")
    print result
    raw_input()

if __name__ == '__main__':
    main()

#--------------------------------------------------------------------------------------------------
# USE PROXY
#wc.Initialize("URL:PORT", "URLONLY", 8080, "username", "password")
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# GET / POST
#--------------------------------------------------------------------------------------------------
#str = wc.Download("http://tokyoinsider.net/login")
#print str
#str2 = wc.Post("tokyoinsider.net", "http://tokyoinsider.net/login",
#               {
#                    "username" : "User ID",
#                    "password" : "Password",
#                    "remember" : "on",
#                    "login" : "Log+In",
#                    "n" : ""
#               }, "http://tokyoinsider.net/login/")
#str3 = wc.Download("http://tokyoinsider.net/account")
#print StringOps.TagMatch(str2, '<div style="padding-top: 2px; font-size: 12px;">', "</div>")
#print StringOps.TagMatch(str3, '<div style="padding-top: 2px; font-size: 12px;">', "</div>")

#--------------------------------------------------------------------------------------------------
# TagMatchSingle
#--------------------------------------------------------------------------------------------------
# test = '<div value="123" id="test"></div>'
#res = StringOps.TagMatchSingle(test, 'id="test"', 'value="', '"')
#print res