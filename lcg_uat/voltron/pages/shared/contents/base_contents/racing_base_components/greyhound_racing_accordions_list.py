from collections import OrderedDict
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import Next4Section
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_accordions_list import RacingEventsAccordionsList
from voltron.pages.shared.contents.base_contents.racing_base_components.today_tomorrow_components import \
    TodayTomorrowEventGroupListItem


class GreyhoundRacingEventsAccordionsList(RacingEventsAccordionsList):
    _item = 'xpath=.//*[@data-crlat="outerAccordion"]/*[@data-crlat="accordion"]'
    _list_item_type = None

    # recognition of event group types
    _list_item_attribute_selector = 'xpath=.//racing-featured/*[not(@data-crlat="raceGrid")] | ' \
                                    './/*[contains(@data-crlat, "racing.futureEvents")] | ' \
                                    './/*[contains(@data-crlat, "racing.") or contains(@data-crlat, "tab.showNextRacesModule")][*]' # old and new xpaths are clubbed
    # _list_item_attribute_selector = 'xpath=.//racing-featured/*[not(@data-crlat="raceGrid")] | .//*[contains(@data-crlat, "racing.futureEvents")]'

    _list_item_attribute_types = {
        # 'racing.byMeeting': TodayTomorrowEventGroupListItem,
        # 'racing.todayTomorrow': TodayTomorrowByTimeGroupListItem,
        'tab.showNextRacesModule': Next4Section,
        'racing-events': TodayTomorrowEventGroupListItem,
        'next-races-module': Next4Section
    }

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_ordered_dict = OrderedDict()
        list_item_content_attr = self._find_elements_by_selector(selector=self._list_item_attribute_selector,
                                                                 timeout=1)
        for context in list_item_content_attr:
            attr = context.get_attribute('data-crlat')
            if attr is None:
                attr = context.tag_name
            known_racing_event_group = self._list_item_attribute_types.get(attr)
            if known_racing_event_group:
                list_item_content_type = known_racing_event_group
                self._logger.debug('*** Recognized "%s" type on %s' % (list_item_content_type.__name__, self.__class__.__name__))
            else:
                list_item_content_type = TodayTomorrowEventGroupListItem
                self._logger.warning(
                    '*** Racing section type "%s" is not known, assuming it is %s' % (attr, list_item_content_type.__name__))
            if not context.text == '':
                element = list_item_content_type(web_element=self._find_element_by_selector(selector=self._item, context=context))
                items_ordered_dict[element.name] = element
                self._logger.warning(f'*** Greyhound Racing accordion {list_item_content_type} is present in DOM but not shown on UI')
        return items_ordered_dict

    @property
    def racing_items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict(
            [self._get_item(web_element=item_we) for item_we in items_we if item_we.is_displayed()])
        return items_ordered_dict
