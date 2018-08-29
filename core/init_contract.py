from core.deploy import ContractMgr


# 合约部署后初始化需要引用的合约地址
def init_contract():
    team = ContractMgr.deployed('TeamJust')
    player = ContractMgr.deployed('PlayerBook')
    fomo = ContractMgr.deployed('FoMo3Dlong')

    player.functions.setTeam(team.address).transact()
    fomo.functions.setPlayerBook(player.address).transact()
    fomo.functions.activate().transact()
    player.functions.addGame(fomo.address,b'fomo').transact()

    tiny = ContractMgr.deployed('TinyF3D')
    tiny.functions.activate().transact()
