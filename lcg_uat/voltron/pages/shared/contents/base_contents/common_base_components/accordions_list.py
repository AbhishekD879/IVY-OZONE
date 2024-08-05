import string
from time import sleep

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup, EventGroupBigComptition
from voltron.pages.shared.contents.base_contents.common_base_components.sport_list_item import SportEventListItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class AccordionsList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="accordion"]'
    _virtual_banner = 'xpath=.//*[contains(@class,"virtual-Img-container")]'
    _list_item_type = EventGroup
    _fade_out_overlay = True
    _verify_spinner = True

    def _wait_all_items(self, poll_interval=1.0, timeout=10):
        prev_all_events_group = self._find_elements_by_selector(self._item, context=self._we, timeout=0)
        iteration = 0
        while True:
            self._spinner_wait()
            all_events_group = self._find_elements_by_selector(self._item, context=self._we, timeout=0)
            iteration += 1
            self._logger.debug(
                '*** Wait for all events to be rendered. Was %s now %s. Iteration %s/%s' %
                (
                    len(prev_all_events_group),
                    len(all_events_group),
                    iteration * poll_interval,
                    timeout
                )
            )
            if len(all_events_group) != len(prev_all_events_group):
                prev_all_events_group = all_events_group
            else:
                break
            if iteration >= int(timeout / poll_interval):
                self._logger.warning(f'Iteration limit met "{int(timeout / poll_interval)}" on get all events groups')
                break
            sleep(poll_interval)
        return all_events_group

    def wait_until_refreshed(self, timeout=5, poll_interval=0.5, item=None, name=None):
        item = item if item else self._item
        result = False
        self._logger.debug('*** Item xpath %s, list item type %s' % (self._item, self.__class__.__name__))
        a = self._find_elements_by_selector(selector=item, timeout=0)
        items_range = len(a) if len(a) <= 3 else 3
        # TODO: override for now as checking all events on page is too much, need to implement some better logic
        for i in range(0, items_range):
            result = wait_for_result(lambda: a[i] != self._find_elements_by_selector(selector=item, timeout=0)[i],
                                     name=f'Class "{self.__class__.__name__}" Item with xpath: "{item}" to refresh',
                                     timeout=timeout,
                                     poll_interval=poll_interval)
        return result

    def _wait_active(self, timeout=15):
        self._we = self._find_myself()
        self._wait_all_items(poll_interval=0.6, timeout=timeout)

    def get_event_from_league_by_event_id(self, league: str = None, event_id: (str, int) = None, raise_exceptions=True):
        """
        Method used to get event from page without initializing all events/sections
        :param league: League where event should be shown (accordion name)
        :param event_id: Openbet/SiteServe ID for event
        :return: SportEventListItem event object
        """
        event_selector = f'{self._list_item_type._item}[.//*[@data-eventid={event_id}]]'
        accordion_selector = f'{self._item}[.//header//*[translate(string(), "{string.ascii_uppercase}", "{string.ascii_lowercase}")="{league.lower()}"]]'

        event = self._find_element_by_selector(selector=event_selector, timeout=3)
        if not event and league:
            league_accordion_we = self._find_element_by_selector(selector=accordion_selector, timeout=1)
            if not league_accordion_we:
                raise VoltronException(f'"{league}" not found on page')
            league_accordion = self._list_item_type(web_element=league_accordion_we)
            league_accordion.expand()
            event = self._find_element_by_selector(selector=event_selector, timeout=3)

        if not event and raise_exceptions:
            raise VoltronException(f'Event {event_id} not found on page')
        elif not event and not raise_exceptions:
            return None
        event_ = SportEventListItem(web_element=event)
        return event_

    def has_virtual_banner_section(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._virtual_banner,
                                                   timeout=0) is not None,
            name=f'virtual banner section status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def virtual_banner_section(self):
        return VirtualBanner(selector=self._virtual_banner, context=self._we)


class AccordionsListForCompetitions(AccordionsList):
    _item = 'xpath=.//accordion'


class AccordionsListForBigCompetitions(AccordionsList):
    _item = 'xpath=.//accordion'
    _list_item_type = EventGroupBigComptition


class VirtualBanner(ComponentBase):
    _Play_now_button = 'xpath=.//*[@class="btn"]'

    @property
    def Play_now_button(self):
        return ButtonBase(selector=self._Play_now_button, context=self._we, timeout=1)
