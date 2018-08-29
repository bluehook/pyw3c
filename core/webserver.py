import json
import os
import shutil

from config import Config
from string import Template
from web3 import Web3


# 创建aiohttp服务器
class WebServerMgr:

    # 生成合约的依赖JS文件
    @staticmethod
    def build_web():

        print('生成web目录..')

        # 清理旧文件
        if os.path.isdir(Config.getWebPath('app')):
            shutil.rmtree(Config.getWebPath('app'))
        os.mkdir(Config.getWebPath('app'))

        # 读取web3.min.js
        with open(Config.getWebTemplatePath('app/js/web3.min.js'),'r',encoding='utf-8') as f:
            web3js = f.read()

        # 模板js
        template_js = Template("""
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
  return new (P || (P = Promise))(function (resolve, reject) {
    function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
    function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
    function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
    step((generator = generator.apply(thisArg, _arguments || [])).next());
  });
};        

let _info = $info_dict
if (typeof web3 !== 'undefined') {
    window.web3 = new Web3(web3.currentProvider);
} else {
    window.web3 = new Web3(new Web3.providers.HttpProvider($provider_ip));
}
function getContract(name) {
    var abi = _info[name]['abi'];
    var address = _info[name]['addr'];
    return new web3.eth.Contract(abi,address);
}
$contlist
$sdk
        """)

        # 遍历合约部署目录,查找已经部署的合约
        if os.path.isdir(Config.getBuildPath()):
            contjs_list = []
            info_dict = {}
            for root, dirs, files in os.walk(Config.getBuildPath()):
                for d in dirs:
                    addrpath = root + d + '/address.s'
                    abipath = root + d + '/abi.json'
                    if os.path.exists(addrpath) and os.path.exists(abipath):
                        with open(abipath, 'r') as f:
                            abi = json.load(f)
                        if abi == []:
                            continue
                        with open(addrpath, 'r') as f:
                            addr = json.load(f)

                        info = {}
                        info["addr"] = addr
                        info["abi"] = abi
                        info_dict[d] = info

                        contjs_list.append('let '+d+' = getContract("'+d+'");')

                        print('  生成'+d+'调用参数..')

            # 读取sdk.js
            with open(Config.getWebTemplatePath('app/js/sdk.js'), 'r', encoding='utf-8') as f:
                sdkjs = f.read()

            outjs = template_js.substitute(info_dict=json.dumps(info_dict),
                                           provider_ip="'"+Config.getNodeIP()+"'",
                                           contlist='\n'.join(contjs_list),
                                           sdk=sdkjs)

            # 生成app.js
            os.mkdir(Config.getWebPath('app/js'))
            with open(Config.getWebPath('app/js/app.js'),'w',encoding='utf-8') as f:
                f.write(web3js)
                f.write('\n')
                f.write(outjs)

                print('  生成app.js')

            # 生成run.py
            shutil.copy(Config.getWebTemplatePath('run.py'), Config.getWebPath('app/'))
            print('  生成run.py')

        print('生成web目录完成')

