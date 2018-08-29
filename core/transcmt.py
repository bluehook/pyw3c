import os
import re
import time
import shutil
import json

from copy import deepcopy
from googletrans import Translator
from config import Config


# 代理
import socket
import socks
import requests

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9090)
socket.socket = socks.socksocket

#print(requests.get('http://ifconfig.me/ip').text)


# 翻译solidity的英文注释为中文
def transSolCmt(paths):#filepath=Config.getContractPath('FoMo3Dlong.sol')):

    for path in paths:
        p,name = path
        filepath = p + name

        with open(filepath,'r',encoding='utf-8') as f:
            text = f.read()

        copytext = deepcopy(text)

        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )

        if os.path.isdir(Config.getBuildPath('TransSolCmt')) == False:
            os.mkdir(Config.getBuildPath('TransSolCmt'))

        translate = Translator()
        lines = re.findall(pattern, text)
        for t in lines:
            if (t[0] != '"' and t[0] != "'"):
                print(t)
                result = translate.translate(t, dest='zh-CN')
                clrstr = result.text.replace('\xa0','').\
                                    replace('\u301c','').\
                                    replace('\u2122','').\
                                    replace('\xa9',''). \
                                    replace('\u200b', ''). \
                                    replace('\xf6', '').\
                                    replace('\u0134','')
                copytext = copytext.replace(t, clrstr)

                print(result.text)

        with open(Config.getBuildPath('TransSolCmt/' + name),'w',encoding='utf-8') as f:
            f.write(copytext)

transSolCmt([[Config.getContractPath('library/'),'MSFun.sol']])
             #[Config.getContractPath('library/'),'NameFilter.sol'],
             #[Config.getContractPath('library/'),'SafeMath.sol']])


