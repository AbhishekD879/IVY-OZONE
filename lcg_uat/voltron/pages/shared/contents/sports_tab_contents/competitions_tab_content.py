from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class LeagueName(ComponentBase):
    _your_call_icon = 'xpath=.//*[@data-crlat="yourcallIcon"]'
    _name = 'xpath=.//*[@data-crlat="couponName" or @data-crlat="event.name"]'

    def has_your_call_icon(self, timeout=3, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._your_call_icon, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'"{self.__class__.__name__}" YourCall icon status to be {expected_result}')

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, timeout=0.5)

    @property
    def event_name(self):
        return self.name


class CompetitionsEventGroup(EventGroup):
    _item = 'xpath=.//*[@data-crlat="linkListItem"]'
    _list_item_type = LeagueName


class CompetitionsAccordionList(AccordionsList):
    _list_item_type = CompetitionsEventGroup


class TennisCompetitionsAccordionList(CompetitionsAccordionList):
    _item = 'xpath=.//*[@data-crlat="linkListItem"]'
    _list_item_type = LeagueName


class CompetitionsTabContent(TabContent):
    _competitions_categories_locator = 'xpath=.//*[@data-crlat="compCats"]'
    _all_competitions_categories_locator = 'xpath=.//*[@data-crlat="azCompCats"]'
    _a_z_competition_label = 'xpath=.//*[@class="inter"] | .//*[@class="split-header"]'
    _list_competitions_categories_locator = 'xpath=.//*[@class="heuristic-container"]'

    @property
    def competitions_categories(self):
        return CompetitionsAccordionList(selector=self._competitions_categories_locator)

    @property
    def all_competitions_categories(self):
        return CompetitionsAccordionList(selector=self._all_competitions_categories_locator)

    @property
    def competitions_categories_list(self):
        return CompetitionsAccordionList(selector=self._list_competitions_categories_locator)

    @property
    def a_z_competition_label(self):
        return A_Z_Competition_Label(selector=self._a_z_competition_label)

    @property
    def tt_competitions_categories_list(self):
        return AccordionsList(selector=self._list_competitions_categories_locator)

    @property
    def accordions_list(self):
        raise NotImplementedError('accordions_list property cannot be used at this level. '
                                  'Please use "tab_content.all_competitions_categories.items_as_ordered_dict" or '
                                  '"tab_content.competitions_categories.items_as_ordered_dict"')


class TennisCompetitionsTabContent(CompetitionsTabContent):

    @property
    def competitions_categories(self):
        return TennisCompetitionsAccordionList(selector=self._competitions_categories_locator)

    @property
    def all_competitions_categories(self):
        return TennisCompetitionsAccordionList(selector=self._all_competitions_categories_locator)


class TennisCompetitionsTabContentDesktop(TennisCompetitionsAccordionList):
    pass


class A_Z_Competition_Label(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)
