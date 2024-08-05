from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.utils.waiters import wait_for_result


class InPlayModuleEventGroup(EventGroup):
    _header = 'xpath=.//*[@data-crlat="dateTitle"]'

    @property
    def sport_name(self):
        return self.name

    @property
    def name(self):
        return self._get_webelement_text(selector=self._header, context=self._we, timeout=0.5)


class InplayHeader(ComponentBase):
    _live_now_label = 'xpath=.//*[@data-crlat="inPlayLabel"]'
    _see_all_label = 'xpath=.//*[@data-crlat="seeAllLabel"]'
    count_label = 'xpath=.//*[@class="see-all-count"]'

    @property
    def text_label(self):
        return self._get_webelement_text(selector=self._live_now_label, context=self._we, timeout=3)

    @property
    def see_all_label(self):
        return self._get_webelement_text(selector=self._see_all_label, context=self._we, timeout=3)

    def has_see_all_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._see_all_label,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Button shown status to be {expected_result}')

    @property
    def see_all(self):
        return self._find_element_by_selector(selector=self._see_all_label, timeout=3)

    @property
    def events_count_label(self):
        events_count_label = self._get_webelement_text(selector=self.count_label, context=self._we, timeout=3)
        return events_count_label.upper().replace('SEE ALL (', '').replace(')', '') if events_count_label else '0'


class UpcomingHeader(ComponentBase):
    _upcoming_label = 'xpath=.//*[@data-crlat="inplay.upcoming"]'
    _count_label = 'xpath=.//*[@data-crlat="inplayCountLabel"]'
    _see_all_label = 'xpath=.//*[@class="see-all-link"]'

    @property
    def text_label(self):
        return self._get_webelement_text(selector=self._upcoming_label, context=self._we, timeout=3)

    @property
    def see_all_label(self):
        return self._get_webelement_text(selector=self._see_all_label, context=self._we, timeout=3)

    def has_see_all_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._see_all_label,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Button shown status to be {expected_result}')

    @property
    def see_all(self):
        return self._find_element_by_selector(selector=self._see_all_label, timeout=3)

    @property
    def events_count_label_text(self):
        return self._get_webelement_text(selector=self._count_label, context=self._we, timeout=3)

    @property
    def events_count_label(self):
        return self._find_element_by_selector(selector=self._count_label, context=self._we, timeout=3)

    @property
    def header_name(self):
        return f'{self.text_label} {self.events_count_label_text}'


class InPlayModule(ComponentBase):
    _see_all_link = 'xpath=.//*[@data-crlat="seeAllLink"]'
    _in_play_header_name = 'xpath=.//*[@data-crlat="inPlayLabel"]'
    _in_play_header = 'xpath=.//*[@data-crlat="inPlayHeader"]'
    _item = 'xpath=.//*[@data-crlat="inPlayGroupContainer"]'
    _list_item_type = InPlayModuleEventGroup
    _fade_out_overlay = True
    _verify_spinner = True

    def has_in_play_header(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._in_play_header, timeout=0) is not None,
                               name=f'In-Play shown status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def in_play_header(self):
        return InplayHeader(selector=self._in_play_header, context=self._we, timeout=1)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._in_play_header_name, context=self._we)

    def has_see_all_link(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._see_all_link, timeout=0) is not None,
                               name=f'See All link shown status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def see_all_link(self):
        return LinkBase(selector=self._see_all_link, context=self._we)
