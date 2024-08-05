import re
from urllib import parse

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.components.content_header import HeaderLine
from voltron.pages.shared.components.free_bets_notification import FreeBetsNotification
from voltron.pages.shared.components.quick_links_section import QuickLinksSection
from voltron.pages.shared.components.super_button_section import SuperButtonSection
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class ComponentContent(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/?'
    _url_matcher_timeout = 5

    @property
    def page_url(self):
        return get_driver().current_url.replace('?automationtest=true', '')

    def url_matcher(self):
        if not self._url_pattern:
            raise VoltronException('Expected URL pattern was not specified, please set _url_pattern variable')
        result = wait_for_result(lambda: re.match(self._url_pattern, parse.unquote(self.page_url)) is not None,
                                 name=f'Browser url: {parse.unquote(self.page_url)} match with expected pattern: {self._url_pattern}',
                                 timeout=self._url_matcher_timeout)
        if not result:
            raise VoltronException('Current browser url: %s does not match with expected pattern: %s'
                                   % (parse.unquote(self.page_url), self._url_pattern))
        return result

    def _load_complete(self, timeout=15):
        result = self.url_matcher()
        return result


class BaseContent(ComponentContent):
    # used tag name because there are other tags with the same content
    _header_line = 'xpath=.//*[@data-crlat="topBar"] | .//*[@data-crlat="bsTab" and contains(text(),"My Bets")] | ' \
                   './/*[contains(@data-crlat,"topBar")] | .//top-bar[@class="ng-star-inserted"]' \
                   ' | .//*[contains(@data-crlat,"topBar")] /ancestor::top-bar'
    _header_line_type = HeaderLine
    _tab_content = 'xpath=.//*[@data-crlat="tabContent"]'
    _tab_content_type = TabContent
    _quick_link_section = 'xpath=.//*[@data-crlat="quickLink.section" or  contains(@class,"quick-links-container")]'
    _free_bets_notification = 'xpath=.//oxygen-notification//*[@data-crlat="freeBetsNotification" or @data-crlat="fbNtf"] | //*[@data-crlat="fbNtf"]'
    _free_bets_notification_type = FreeBetsNotification
    _surface_bet_section = 'xpath=.//super-button'

    @property
    def quick_link_section(self):
        return QuickLinksSection(selector=self._quick_link_section, context=self._we, timeout=3)

    def has_quick_link_section(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._quick_link_section,
                                                   timeout=0) is not None,
            name=f'Quick link section status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def super_button_section(self):
        return SuperButtonSection(selector=self._surface_bet_section, context=self._we, timeout=3)

    def has_super_button_section(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._surface_bet_section,
                                                   timeout=0) is not None,
            name=f'Quick link section status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def free_bets_notification(self):
        return self._free_bets_notification_type(selector=self._free_bets_notification, context=get_driver())

    def has_free_bets_notification(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bets_notification,
                                                   timeout=0,
                                                   context=get_driver()) is not None and
            self._free_bets_notification_type(selector=self._free_bets_notification,
                                              timeout=0,
                                              context=get_driver()).is_displayed(),
            name=f'"{self.__class__.__name__}" Free Bets Notification status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def header_line(self):
        return self._header_line_type(selector=self._header_line)

    @property
    def content_title_text(self):
        return self.header_line.page_title.title

    def back_button_click(self):
        self.header_line.back_button.click()

    def is_back_button_displayed(self):
        return self.header_line.has_back_button

    def go_to_content_home(self):
        self.header_line.page_title.click()

    @property
    def tab_content(self):
        return self._tab_content_type(selector=self._tab_content)


class BaseDesktopContent(BaseContent):
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _breadcrumbs_type = Breadcrumbs

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)
