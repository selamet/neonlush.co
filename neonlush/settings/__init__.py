from neonlush.settings.base import *

if env("ENV_NAME", None) == 'prod':
    from .prod import *
else:
    from .local import *
