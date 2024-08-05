from voltron.pages.shared.components.home_page_components.desktop.base_desktop_module import BaseDesktopModule
from voltron.pages.shared.components.home_page_components.home_page_byb_tab import BYBTabContent


class BYBModule(BaseDesktopModule):
    _content = 'xpath=.//*[@data-crlat="tab.showBYB"]'
    _content_type = BYBTabContent
