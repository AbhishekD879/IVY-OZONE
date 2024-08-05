from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class QuickLink(ComponentBase):
    _link = 'xpath=.//*[@data-crlat="offerLink"]'
    _name = 'xpath=.//*[@data-crlat="couponName"]'
    _svg_icon = 'xpath=.//*[@class="quick-link-icon"]/*'

    @property
    def svg_icon(self):
        wait_for_result(lambda: self._find_element_by_selector(selector=self._svg_icon, context=self._we) is not None, name='svg icon is not displayed')
        return self._find_element_by_selector(selector=self._svg_icon, context=self._we, timeout=0).get_attribute('xlink:href')

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._name, context=self._we, timeout=0).get_attribute('innerHTML')


class QuickLinksSportPages(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="quickLinkItem"]'
    _list_item_type = QuickLink
