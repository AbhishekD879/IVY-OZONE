from voltron.pages.shared.components.market_selector_drop_down_desktop import MarketSelectorDesktopDropDown
from voltron.pages.shared.contents.sports_tab_contents.matches_tab_content import MatchesTabContent


class MatchesTabContentDesktop(MatchesTabContent):
    _market_selector_module = 'xpath=.//*[@data-crlat="dropdown"]'
    _dropdown_market_selector_type = MarketSelectorDesktopDropDown
