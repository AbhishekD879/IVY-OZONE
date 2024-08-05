# flake8: noqa

import tests
from voltron.utils.exceptions.voltron_exception import VoltronException

brand = tests.settings.brand
if brand == 'bma':
    from voltron.utils.content_manager.bma_content_manager import BMAContentManager as ContentManager
elif brand == 'ladbrokes':
    from voltron.utils.content_manager.ladbrokes_content_manager import LadbrokesContentManager as ContentManager
elif brand == 'vanilla':
    from voltron.utils.content_manager.vanilla_content_manager import VanillaContentManager as ContentManager
else:
    raise VoltronException(f'Unrecognized brand {brand}')
