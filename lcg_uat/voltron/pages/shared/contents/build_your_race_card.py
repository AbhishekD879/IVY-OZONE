from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.edp.racing_edp_market_section import Outcome
from voltron.pages.shared.contents.edp.racing_event_details import EventMarketsList, RaceDetailsContainer, \
    RacingEventDetails
from voltron.utils.waiters import wait_for_result


class BuildYourRaceCardMarketTabs(ComponentBase):
    _menu_items = 'xpath=.//li[./*[@data-crlat="tab.tpTabs"]]'
    _item = _menu_items
    _list_item_type = TextBase
    _selected_item = 'xpath=.//*[contains(@class, "active")]'
    _item_name = 'xpath=.//*[@data-crlat="tab"]'

    @property
    def selected_tab(self):
        return self._get_webelement_text(selector=self._selected_item)


class RaceEvent(ComponentBase):
    _race_details_container = 'xpath=.//*[@data-crlat="raceDetailsContainer"]'
    _tabs_menu = 'xpath=.//*[@data-crlat="panel.tabs"]'
    _race_name = 'xpath=.//*[@data-crlat="raceName"]'
    _event_markets_list = 'xpath=.//*[@data-crlat="racingEventModel"]'
    _countdown_container = 'xpath=.//*[@data-crlat="raceCountdown"]'

    @property
    def race_event_detail(self):
        return RaceDetailsContainer(selector=self._race_details_container, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._race_name, context=self._we).replace('/n', ' ')

    @property
    def tabs_menu(self):
        return BuildYourRaceCardMarketTabs(selector=self._tabs_menu, context=self._we)

    @property
    def event_markets_list(self):
        return EventMarketsList(web_element=self._we)

    @property
    def countdown_timer(self):
        return TextBase(selector=self._countdown_container, context=self._we)

    def has_countdown_timer(self, timeout=3, expected=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._countdown_container, timeout=0),
            name=f'Countdown timer to be displayed',
            expected_result=expected,
            timeout=timeout)
        return result


class BuildYourCardAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="racingEventModel"]'
    _list_item_type = RaceEvent


class BuildYourCardTabContent(TabContent):
    _accordions_list_type = BuildYourCardAccordionsList


class BuildYourRaceCard(BaseContent):
    _tab_content_type = BuildYourCardTabContent
    _title = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    # _url_pattern = r'^http[s]?:\/\/.+\/(horse-racing)\/[\w-]+\/[\w-]+\/[\w-]+\/[0-9]+\/[\w-]+'

    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _breadcrumbs_type = Breadcrumbs

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)


class BuildYourOwnCardAccordionsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="raceCard.odds"]'
    _list_item_type = Outcome


class BuildYourOwnCardTabContent(TabContent):
    _accordions_list_type = BuildYourOwnCardAccordionsList


class BuildYourOwnRaceCard(RacingEventDetails):
    _tab_content_type = BuildYourOwnCardTabContent
    _title = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _url_pattern = r'^https?:\/\/.+\/horse-racing\/build-your-own-race-card\/\d+$'
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _breadcrumbs_type = Breadcrumbs

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)