import json
import os
import shutil
import re

from web3 import Web3
from solc import compile_files

from config import Config


# 合约管理
class ContractMgr:

    # 编译合约
    @staticmethod
    def compile():

        # 清除旧文件
        if os.path.isdir(Config.getBuildPath()):
            shutil.rmtree(Config.getBuildPath())
        os.mkdir(Config.getBuildPath())

        # 遍历合约文件夹,查找所有sol
        filepaths = []
        if os.path.isdir(Config.getContractPath()):
            for root, dirs, files in os.walk(Config.getContractPath()):
                for d in dirs:
                    pass
                for f in files:
                    if os.path.splitext(f)[-1] == '.sol':
                        if root == Config.getContractPath():
                            fpath = root + f
                        else:
                            fpath = ''.join([root,'/',f])
                        filepaths.append(fpath)

        print('开始编译合约..')

        compiled_sol = compile_files(filepaths,optimize=True,optimize_runs=200)

        for k,v in compiled_sol.items():

            contract_interface = compiled_sol[k]

            if len(contract_interface['bin']) == 0:
                continue

            solname = str(k).split(':')[1]
            savepath = Config.getBuildPath(solname)

            if os.path.isdir(Config.getBuildPath()) == False:
                os.mkdir(Config.getBuildPath())

            if os.path.isdir(savepath):
                shutil.rmtree(savepath)
            os.mkdir(savepath)

            # 生成全接口文件
            interfacepath = savepath + '/' + solname + '.json'
            with open(interfacepath, 'w') as outfile:
                json.dump(contract_interface, outfile)

            print('  生成合约' + solname + '的interface文件:', interfacepath, '..')

            # 生成abi,bytecode文件
            abipath = savepath + '/abi.json'
            with open(abipath, 'w') as outfile:
                json.dump(contract_interface['abi'], outfile)

            print('  生成合约' + solname + '的abi文件:', abipath, '..')

            bytecodepath = savepath + '/bytecode.s'
            with open(bytecodepath, 'w') as outfile:
                outfile.write(contract_interface['bin'])

            print('  生成合约' + solname + '的bytecode文件:', bytecodepath, '..')

        print('合约编译完成.')


    # 部署合约
    @staticmethod
    def deploy():

        # 链接表
        from core.linkcode import linkcode

        print('部署合约..')

        filelist = []
        if os.path.isdir(Config.getBuildPath()):
            for dirname in os.listdir(Config.getBuildPath()):
                filelist.append(dirname)


        for dirname in filelist:
            if dirname not in linkcode.keys():
                ContractMgr.deploy_one(dirname)

        for dirname in filelist:
            if dirname in linkcode.keys():
                links = linkcode[dirname]

                # 获取自己的bytecode
                with open(Config.getBuildPath(dirname + '/bytecode.s')) as f:
                    bytedata = f.read()

                if len(links) > 0:

                    for link in links:
                        # 获取依赖合约的部署地址
                        with open(Config.getBuildPath(link + '/address.s')) as f:
                            addr = json.load(f).replace('0x','')

                        bytedata = re.sub(r"_.+?[_]+", addr, bytedata)

                    bytecodepath = Config.getBuildPath(dirname) + '/bytecode.s'
                    with open(bytecodepath, 'w') as outfile:
                        outfile.write(bytedata)

                    ContractMgr.deploy_one(dirname)

        print('部署完成..')


    # 部署一个合约
    @staticmethod
    def deploy_one(dirname):

        # 读取abi,bytecode
        with open(Config.getBuildPath(dirname + '/abi.json')) as f:
            abi = json.load(f)

        with open(Config.getBuildPath(dirname + '/bytecode.s')) as f:
            bytedata = f.read()

        # 尝试部署
        web3 = Web3(Web3.HTTPProvider(Config.getNodeIP()))

        # 设置默认账户
        web3.eth.defaultAccount = web3.eth.accounts[0]

        # 实例化合约
        contract = web3.eth.contract(abi=abi, bytecode=bytedata)

        # 提交部署合约事务
        tx_hash = contract.constructor().transact()

        # 等待事务挖矿结束并获取交易收据
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

        # 生成地址文件
        addr = Config.getBuildPath(dirname + '/address.s')
        with open(addr, 'w') as outfile:
            json.dump(tx_receipt['contractAddress'], outfile)
        print('  合约' + dirname + '部署地址:', tx_receipt['contractAddress'], '..',
              '使用gas数量:',tx_receipt['gasUsed'],
              '块地址:',tx_receipt['blockNumber'])

        return contract

    # 获取已经部署合约实例
    @staticmethod
    def deployed(name):

        def load_contract_params(name):
            addrpath = Config.getBuildPath(name + '/address.s')
            abipath = Config.getBuildPath(name + '/abi.json')
            with open(addrpath, 'r') as f:
                addr = json.load(f)
            with open(abipath, 'r') as f:
                abi = json.load(f)

            return (addr, abi)

        web3 = Web3(Web3.HTTPProvider(Config.getNodeIP()))
        web3.eth.defaultAccount = web3.eth.accounts[0]

        # 创建合约实例
        addr,abi = load_contract_params(name)
        contract = web3.eth.contract(address=addr,abi=abi)

        return contract
