import json

from web3 import Web3
from config import Config
from core.deploy import ContractMgr


# 测试合约调用
def apitest():

    roundInfoNames = ['ICO投入','回合ID','总钥匙数','结束时间','开始时间','当前奖池','领先队伍和玩家ID','领先玩家地址','领先玩家名称','鲸队eth','熊队eth','蛇队eth','牛队eth','当前空投概率']
    def getCurrentRoundInfo(c):
        data = dict(zip(roundInfoNames,c.functions.getCurrentRoundInfo().call()))
        data['总钥匙数'] = round(data['总钥匙数'] / (10 ** 18), 4)
        data['鲸队eth'] = round(data['鲸队eth'] / (10 ** 18), 4)
        data['熊队eth'] = round(data['熊队eth'] / (10 ** 18), 4)
        data['蛇队eth'] = round(data['蛇队eth'] / (10 ** 18), 4)
        data['牛队eth'] = round(data['牛队eth'] / (10 ** 18), 4)
        data['当前奖池'] = round(data['当前奖池'] / (10 ** 18), 4)
        data['当前空投概率'] = round(data['当前空投概率'] / (10 ** 21), 4)
        data['领先玩家地址'] = ''
        data['领先玩家名称'] = ''

        return data

    playerInfoNames = ['玩家ID', '玩家姓名', '钥匙数', '金库', '获利', '推广', '回合投入']
    def getPlayerInfo(c):
        data = dict(zip(playerInfoNames, c.functions.getPlayerInfoByAddress(
            '0x68521dfDfC5b5Cb739700d815498DE7f74eD6fCa').call()))
        data['钥匙数'] = round(data['钥匙数'] / (10 ** 18), 4)
        data['金库'] = round(data['金库'] / (10 ** 18), 4)
        data['获利'] = round(data['获利'] / (10 ** 18), 4)
        data['推广'] = round(data['推广'] / (10 ** 18), 4)
        data['回合投入'] = round(data['回合投入'] / (10 ** 18), 4)
        data['玩家姓名'] = ''

        return data

    def init(c):
        print('添加一个玩家:',
              Web3.toHex(c.functions.registerNameXID('bluehook', 0, True).transact({'value': '100000000000000'})), '\n')

    def lisp(c):
        print('回合数据:', getCurrentRoundInfo(c), '\n')

        print('  玩家信息:', getPlayerInfo(c),'\n')

        buy = Web3.toWei(0.1,'ether')
        print('  购买钥匙:', Web3.toHex(c.functions.buyXid(0, 1).transact({'value': buy})),'\n')

        print('  玩家信息:', getPlayerInfo(c),'\n')

        print('回合数据:', getCurrentRoundInfo(c), '\n')

        buy = Web3.toWei(0.1,'ether')
        print('  购买钥匙:', Web3.toHex(c.functions.buyXid(0, 1).transact({'value': buy})),'\n')

        print('  玩家信息:', getPlayerInfo(c),'\n')

        print('回合数据:', getCurrentRoundInfo(c), '\n')


    isF3D = False
    if isF3D:
        fomo = ContractMgr.deployed('FoMo3Dlong')
        init(fomo)
        lisp(fomo)
    else:
        tiny = ContractMgr.deployed('TinyF3D')
        init(tiny)
        lisp(tiny)

