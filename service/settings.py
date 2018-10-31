DATABASE_URI = "postgresql://amoveo:password@localhost:5432/amoveo-explorer"

NODE_INT_URL = "http://localhost:8081"
NODE_EXT_URL = "http://localhost:8080"


try:
    from service.settings_local import *
except ImportError:
    pass
