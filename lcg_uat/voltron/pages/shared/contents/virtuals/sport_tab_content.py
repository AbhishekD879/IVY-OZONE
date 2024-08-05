from voltron.pages.shared.components.edp.sport_event_details import MarketsSectionsList
from voltron.pages.shared.contents.virtuals.base_tab_content import BaseVirtualsTabContent


class VirtualMarketsSectionsList(MarketsSectionsList):
    _market_name = 'xpath=.//*[@data-crlat="headerTitle.leftMessage"]'


class VirtualSportTabContent(BaseVirtualsTabContent):
    _accordions_list_type = VirtualMarketsSectionsList
