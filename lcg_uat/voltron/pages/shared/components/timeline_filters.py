from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from collections import OrderedDict


class TimelineFilter(ComponentBase):
    _name = 'xpath=.//*[contains(@class,"filter-wrapper")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)


class TimelineFilters(ComponentBase):
    _item = 'xpath=.//competition-filter'
    _list_item_type = TimelineFilter
    _selected_filters = 'xpath=.//*[@class="filter-wrapper active"]'

    @property
    def selected_filters(self):
        items_we = self._find_elements_by_selector(selector=self._selected_filters, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        selected_filters = OrderedDict()
        for item_we in items_we:
            selected_filters.update({item_we.text: item_we})
        if len(selected_filters) is 0:
            return None
        else:
            return selected_filters

    @property
    def selected_filter(self):
        return ButtonBase(selector=self._selected_filters, context=self._we)
