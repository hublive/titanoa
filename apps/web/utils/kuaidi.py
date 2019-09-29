import ssl
import string
import urllib.request
from urllib.parse import quote


def kuadi(no):
    host = 'https://wuliu.market.alicloudapi.com'
    path = '/kdi'
    method = 'GET'
    appcode = '48ad0b999580443e80bcfa9be0ebfc63'
    querys = 'no={}'.format(no)
    bodys = {}
    url = host + path + '?' + querys
    newurl = quote(url, safe=string.printable)
    request = urllib.request.Request(newurl)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(request, context=ctx)
    content = response.read()
    if content:
        return content.decode('UTF-8')
    
