from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import ComponentContent
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.utils.waiters import wait_for_result


class FutureEventListItem(ComponentBase):
    _item_name = 'xpath=.//*[@data-crlat="racing.futureEventName"]'
    _item_time = 'xpath=.//*[@data-crlat="racing.futureEventTime"]'

    @property
    def name(self):
        return TextBase(selector=self._item_name, timeout=0, context=self._we)

    @property
    def time(self):
        return TextBase(selector=self._item_time, timeout=0, context=self._we)

    @property
    def event_name(self):
        return self.name.text


class FutureEventGroupListItem(EventGroup):
    _item = 'xpath=.//*[@data-crlat="racing.futureEvent"]'
    _list_item_type = FutureEventListItem
    _cash_out_mark = 'xpath=.//*[@data-crlat="labelCashout"]'

    def has_cash_out_mark(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cash_out_mark,
                                                   timeout=0) is not None,
            name=f'Cash out mark status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class FutureEventGroupList(AccordionsList, ComponentContent):
    _list_item_type = FutureEventGroupListItem
    _url_pattern = r'^http[s]?:\/\/.+\/.+\/future'
