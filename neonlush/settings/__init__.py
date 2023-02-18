from neonlush.settings.base import *

if env("ENV_NAM") == 'prod':
    from .prod import *
else:
    from .local import *
