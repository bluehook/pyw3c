import sys
sys.path.append('../')

from aiohttp import web
from config import Config

# 全局路由表
routes = web.RouteTableDef()


# 首页
@routes.get('/')
async def index(request):
    return web.FileResponse('index.html')


"""启动服务器"""
app = web.Application()
app.router.add_static('/app/',
                      path='app',
                      name='app')
app.add_routes(routes)
web.run_app(app, host=Config.getWebIP(), port=Config.getWebPort())