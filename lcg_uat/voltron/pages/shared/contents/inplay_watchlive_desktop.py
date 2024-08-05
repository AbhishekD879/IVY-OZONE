from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import InPlayEventGroupHomePage, \
    InPlaySportGroupHomePage
from voltron.pages.shared.contents.inplay import InPlayAccordionList
from voltron.pages.shared.contents.inplay_desktop import InPlayDesktopTabContent


class WatchLiveEventGroupInPlayPageDesktop(InPlayEventGroupHomePage):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'


class WatchLiveSportGroupInPlayPage(InPlaySportGroupHomePage):
    _item = 'xpath=.//*[@data-crlat="accordion"][*]'
    _list_item_type = WatchLiveEventGroupInPlayPageDesktop


class InPlayWatchLiveAccordionList(InPlayAccordionList):
    _item = 'xpath=.//*[@data-crlat="accordion" and not(contains(@class, "page-inner-container"))]'
    _list_item_type = WatchLiveSportGroupInPlayPage


class InPlayWatchLiveDesktopTabContent(InPlayDesktopTabContent):
    _item = 'xpath=.//*[@data-crlat="accordionsList"]'
    _accordions_list = 'xpath=.//*[@data-crlat="tab.showWatchLiveContent"]'
    _accordions_list_type = InPlayWatchLiveAccordionList
