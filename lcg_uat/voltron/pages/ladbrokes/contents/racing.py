from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from voltron.pages.ladbrokes.contents.base_contents.racing_base import LadbrokesRacingPageBase
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.racing_tab_content import LadbrokesRacingEventsAccordionsList
from voltron.pages.ladbrokes.contents.sports_tab_contents.next_races_tab import LadbrokesNextRacesTabContent
from voltron.pages.shared import get_driver
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_tab_content import GreyhoundRacingTabContent
from voltron.pages.shared.contents.racing import GreyhoundRacing
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.next_races import LadbrokesNextRaces
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.racing_accordions_list import LadbrokesSpecials
from voltron.utils.waiters import wait_for_result


class LadbrokesGreyhoundRacingTabContent(GreyhoundRacingTabContent):
    _accordions_list_type = LadbrokesRacingEventsAccordionsList

    def _wait_active(self, timeout=0):
        self._find_element_by_selector(selector=self._selector, context=get_driver())
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._accordions_list_type._item,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()

    @property
    def accordions_list(self):
        return self._accordions_list_type(web_element=self._we, selector=self._selector)


class GreyhoundRacingLadbrokes(GreyhoundRacing):
    _url_pattern = r'^https?:\/\/.+\/greyhound-racing(\/)?(races|today|tomorrow|future|results|specials)?(\/)?(next|by-meeting|by-time|by-meetings|by-latest-results)?$'
    _tab_content_type = LadbrokesGreyhoundRacingTabContent
    _special_races = LadbrokesSpecials

    @property
    def tab_content(self):
        if vec.racing.RACING_NEXT_RACES_NAME.lower() in self.tabs_menu.current.lower():
            return LadbrokesNextRacesTabContent(selector=self._selector, web_element=self._we)
        return super().tab_content

    @property
    def special_races(self):
        return self._special_races(selector=self._selector, web_element=self._we)


class LadbrokesHorseracing(LadbrokesRacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/horse-racing(\/)?(?:featured|future|yourcall|results|specials|races/next)?(\/)?(by-meetings|by-latest-results)?$'
    _bet_filter_link = 'xpath=.//*[@data-crlat="betFinderTitle"]'
    _next_races = LadbrokesNextRaces
    _special_races = LadbrokesSpecials
    _my_stable_button = 'xpath=.//*[@data-crlat="myStableTitle"]'
    _my_stable_icon_link = 'xpath=.//*[@data-crlat="myStableIcon"]/*'
    _my_stable_icon = 'xpath=.//*[@data-crlat="myStableIcon"]'


    @property
    def my_stable_link(self):
        return LadbrokesHorseracing(selector=self._my_stable_button)

    @property
    def my_stable_icon(self):
        return self._find_element_by_selector(selector=self._my_stable_icon)

    def has_my_stable_icon(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_icon, context=self._we, timeout=0) is not None,
            name=f'"my stable" link presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


    @property
    def my_stable_icon_link(self):
        return self._find_element_by_selector(selector=self._my_stable_icon_link).get_attribute('href')

    @property
    def bet_filter_link(self):
        return LadbrokesHorseracing(selector=self._bet_filter_link)

    @property
    def next_races(self):
        return self._next_races(selector=self._selector, web_element=self._we)

    @property
    def special_races(self):
        return self._special_races(selector=self._selector, web_element=self._we)

    @property
    def tab_content(self):
        if vec.racing.RACING_NEXT_RACES_NAME.lower() in self.tabs_menu.current.lower():
            return LadbrokesNextRacesTabContent(selector=self._selector, web_element=self._we)
        return super().tab_content
