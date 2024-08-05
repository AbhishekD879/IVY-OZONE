from voltron.pages.shared.components.home_page_components.home_page_private_markets_tab import \
    PrivateMarketsAccordionsList, PrivateMarketsTabContentDesktop
from voltron.pages.shared.components.home_page_components.home_page_private_markets_tab import PrivateMarketsTabContent


class LadbrokesPrivateMarketsAccordionsList(PrivateMarketsAccordionsList):
    _item = 'xpath=.//*[@data-crlat="pmAccordion"]'


class LadbrokesPrivateMarketsTabContent(PrivateMarketsTabContent):
    _accordions_list_type = LadbrokesPrivateMarketsAccordionsList


class LadbrokesPrivateMarketsTabContentDesktop(PrivateMarketsTabContentDesktop, LadbrokesPrivateMarketsTabContent):
    pass
