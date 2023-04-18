import uvicorn
from Server.settings import setting

uvicorn.run('Server.app:app',
            host=setting.server_host,
            port=setting.server_port)