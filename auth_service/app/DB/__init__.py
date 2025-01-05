from auth_service.app.core import all_configs
from auth_service.app.DB.db import MongoDB

mongo_db_init = MongoDB(all_configs.mongo)
