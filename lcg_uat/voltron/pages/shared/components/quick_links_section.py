from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.primitives.text_labels import TextBase


class QuickLinksSection(ComponentBase):
    _description = 'xpath=.//*[@data-crlat="description"]'
    _button = 'xpath=.//*[@data-crlat="button"]'
    _validate_message = 'xpath=.//div[contains(@class,"container")]/p'
    _quick_link = 'xpath=.//*[@class="quick-links-area"]'

    @property
    def quick_link_items(self):
        return QuickLinksItem(selector=self._quick_link, context=self._we)

    @property
    def message_validation(self):
        return TextBase(selector=self._validate_message, timeout=10)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description, timeout=1)

    @property
    def button(self):
        return ButtonBase(selector=self._button, context=self._we, timeout=3)

    def has_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._button,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class QuickLinks(ComponentBase):
    _name = 'xpath=./span'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)


class QuickLinksItem(ComponentBase):
    _item = 'xpath=./a'
    _list_item_type = QuickLinks
