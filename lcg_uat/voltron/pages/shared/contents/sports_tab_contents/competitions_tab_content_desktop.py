from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import CompetitionsAccordionList
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import CompetitionsEventGroup
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import LeagueName
from voltron.pages.shared.contents.sports_tab_contents.sport_coupons_tab import CouponsTabContent


class LeagueNameDesktop(LeagueName):
    _name = 'xpath=.//*[@data-crlat="event.name"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)


class CompetitionsEventGroupDesktop(CompetitionsEventGroup):
    _item = 'xpath=.//*[@data-crlat="linkListItem"]'
    _list_item_type = LeagueNameDesktop


class CompetitionsAccordionListDesktop(CompetitionsAccordionList):
    _list_item_type = CompetitionsEventGroupDesktop


class CompetitionsCategoryTitle(ComponentBase):
    _name = 'xpath=.//*[@class="league-name"]'
    _league_origin = 'xpath=.//*[@class="league-origin"]'
    _league_country = 'xpath=.//*[@class="league-country"]'
    _go_icon = 'xpath=.//*[@class="go-icon"]'

    @property
    def go_icon(self):
        return self._find_element_by_selector(selector=self._go_icon, timeout=2)

    @property
    def league_country(self):
        return self._find_element_by_selector(selector=self._league_country, timeout=2)

    @property
    def league_origin(self):
        return self._find_element_by_selector(selector=self._league_origin, timeout=2)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)


class CompetitonsQuickLinksWrapper(ComponentBase):
    _item = 'xpath=.//*[@class="competition-category-tile-wrapper"]'
    _list_item_type = CompetitionsCategoryTitle


class CompetitionsTabContentDesktop(CouponsTabContent):
    _list_item_type = CompetitionsEventGroup
    _accordions_list = 'xpath=.//*[@data-crlat="categoriesList"]'
    _accordions_list_type = CompetitionsAccordionListDesktop
    _quick_link_container = 'xpath=.//*[@class="competition-category-tiles"]'
    _list_competitions_categories_locator = 'xpath=.//*[@data-crlat="accordionsList"]//parent::*[@class="sk-container"]'

    @property
    def quick_link_container(self):
        return ComponentBase(selector=self._quick_link_container, context=self._we)

    @property
    def quick_links_wrapper(self):
        return CompetitonsQuickLinksWrapper(selector=self._quick_link_container, context=self._we)

    @property
    def competitions_categories_list(self):
        return CompetitionsAccordionListDesktop(selector=self._list_competitions_categories_locator)

    @property
    def tt_competitions_categories_list(self):
        return AccordionsList(selector=self._list_competitions_categories_locator)