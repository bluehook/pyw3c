import os
import sys

from core.deploy import ContractMgr
from core.webserver import WebServerMgr
from core.apitest import apitest
from core.init_contract import init_contract


##
if __name__ == '__main__':

    if 'compile' in sys.argv:
        # 部署合约
        os.chdir("./core/")
        ContractMgr.compile()
    elif 'migrate' in sys.argv:
        # 部署合约
        os.chdir("./core/")
        ContractMgr.deploy()
        print('初始化合约..')
        init_contract()
        print('初始化完成')
    elif 'test' in sys.argv:
        os.chdir("./core/")
        apitest()
    elif 'webc' in sys.argv:
        # 生成web页面
        os.chdir("./core/")
        WebServerMgr.build_web()
    elif 'run' in sys.argv:
        # 启动web服务器
        print('\n启动web服务器..')
        os.chdir("./web/")
        os.system("run.py")
    else:
        help = '''
        usage: python pyw3c.py [option] [arg] 
        Options and arguments (and corresponding environment variables):
        help h -h   : help text
        compile     : only compile
        migrate     : compile and deploy contracts
        test        : test contracts
        webc        : build web webdir
        run         : run webserver
        '''
        print(help)
