from voltron.pages.shared.components.base import ComponentBase


class NextRacesFiltersContainer(ComponentBase):
    _name = 'xpath=.//*[@class="filter"]'

    @property
    def name(self):
        self.scroll_to()
        return self._get_webelement_text(selector=self._name, context=self._we)


class NextRacesFilters(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"filter-wrapper")]'
    _list_item_type = NextRacesFiltersContainer
