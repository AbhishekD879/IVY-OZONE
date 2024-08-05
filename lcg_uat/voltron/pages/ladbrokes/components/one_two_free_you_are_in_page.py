from voltron.pages.shared.contents.base_content import ComponentContent
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from collections import OrderedDict


class TeamsList(ComponentContent):
    _name = 'xpath=.//*[contains(@class,"teamsName")]'
    _result = 'xpath=.//*[contains(@class,"result")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def result(self):
        return self._find_element_by_selector(selector=self._result, timeout=5)


class UpCellMarketItemContainer(ComponentContent):
    _market_header = 'xpath=.//*[contains(@class,"slideHeader")]'
    _add_to_betslip_button = 'xpath=.//*[contains(@class,"btnCta")]'
    _item = 'xpath=.//*[contains(@class,"teamsList")]'
    _list_item_type = TeamsList

    @property
    def market_header(self):
        return self._get_webelement_text(selector=self._market_header, timeout=5)

    @property
    def add_to_betslip_button(self):
        return ButtonBase(selector=self._add_to_betslip_button, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)} {list_item.name}': list_item})
        return items_ordered_dict
