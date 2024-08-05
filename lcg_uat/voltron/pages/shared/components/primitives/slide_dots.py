from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class SlideDot(ComponentBase):
    _button = 'xpath=.//*[@data-crlat="dotBtn"]'

    @property
    def button(self):
        return ButtonBase(selector=self._button, context=self._we)

    def click(self):
        return self.button.click()

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        if not name:
            name = '"%s" selected status is: %s' % (self.__class__.__name__, expected_result)
        result = wait_for_result(lambda: 'slide-active' in self.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result


class SlideDots(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="slideDotContainer"]'
    _list_item_type = SlideDot

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict({items_we.index(item_we): self._list_item_type(web_element=item_we)
                                          for item_we in items_we})
        return items_ordered_dict
