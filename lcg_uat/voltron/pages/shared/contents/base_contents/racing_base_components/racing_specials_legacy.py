
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup


class RacingSpecialsEventListItem(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class RacingSpecialsEventGroupLegacy(EventGroup):
    _name = 'xpath=.//*[@data-crlat="racing.specialName"]'
    _ew_terms = 'xpath=.//*[@data-crlat="racing.specialEw"]'
    _date = 'xpath=.//*[@data-crlat="racing.specialTime"]'
    _item = 'xpath=.//*[@data-crlat="racing.specialOutcome"]'
    _list_item_type = RacingSpecialsEventListItem

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def each_way_terms(self):
        return self._get_webelement_text(selector=self._ew_terms)

    @property
    def date(self):
        return self._get_webelement_text(selector=self._date)


class SpecialsLegacy(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="racing.specialEvents"]'
    _list_item_type = RacingSpecialsEventGroupLegacy
