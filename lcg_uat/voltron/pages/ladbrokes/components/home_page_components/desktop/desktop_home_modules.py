from voltron.pages.ladbrokes.components.home_page_components.desktop.byb_module import LadbrokesBYBModule
from voltron.pages.ladbrokes.components.home_page_components.desktop.private_markets_module import \
    LadbrokesPrivateMarketsModuleDesktop
from voltron.pages.shared.components.home_page_components.desktop.desktop_home_modules import DesktopHomeModules


class LadbrokesDesktopHomeModules(DesktopHomeModules):
    """Designed to behave in a similar way as tabs on mobile"""

    _byb_module_type = LadbrokesBYBModule
    _private_markets_type = LadbrokesPrivateMarketsModuleDesktop
