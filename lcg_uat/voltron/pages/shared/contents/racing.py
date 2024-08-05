from voltron.pages.shared.contents.base_contents.racing_base import RacingPageBase, GreyhoundPageBase
from voltron.utils.waiters import wait_for_result


class Horseracing(RacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/horse-racing(\/)?(?:featured|future|yourcall|results|specials)?(\/)?(by-meetings|by-latest-results)?$'
    _bet_filter_link = 'xpath=.//*[@data-crlat="betFinderTitle"]'
    _my_stable_button = 'xpath=.//*[@data-crlat="myStableTitle"]'
    _my_stable_icon_link = 'xpath=.//*[@data-crlat="myStableIcon"]/*'
    _my_stable_icon = 'xpath=.//*[@data-crlat="myStableIcon"]'

    @property
    def bet_filter_link(self):
        return Horseracing(selector=self._bet_filter_link)

    @property
    def my_stable_link(self):
        return Horseracing(selector=self._my_stable_button)

    @property
    def my_stable_icon(self):
        return self._find_element_by_selector(selector=self._my_stable_icon)

    @property
    def my_stable_icon_link(self):
        return self._find_element_by_selector(selector=self._my_stable_icon_link).get_attribute('href')

    def has_my_stable_icon(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_icon, context=self._we,
                                                   timeout=0) is not None,
            name=f'"my stable" link presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class GreyhoundRacing(GreyhoundPageBase):
    _url_pattern = r'^https?:\/\/.+\/greyhound-racing(\/)?(today|tomorrow|future|results|specials)?(\/)?(by-meeting|by-time|by-meetings|by-latest-results)?$'
