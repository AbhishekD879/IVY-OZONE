from selenium.common.exceptions import StaleElementReferenceException

import tests
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content_desktop import MatchesTabContentDesktop
from voltron.pages.shared import get_driver, get_device_properties
from voltron.pages.shared.contents.base_contents.base_sport_race_structure import SportRacingPageBase
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content import CompetitionsTabContent
from voltron.pages.shared.contents.sports_tab_contents.jackpot import JackpotTabContent
from voltron.pages.shared.contents.sports_tab_contents.football_results import ResultsTabContent
from voltron.pages.shared.contents.sports_tab_contents.matches_tab_content import MatchesTabContent
from voltron.pages.shared.contents.sports_tab_contents.outrights_tab_content import OutrightsTabContent
from voltron.pages.shared.contents.sports_tab_contents.popular_bets_tab_content import PopularBetsTabContent
from voltron.pages.shared.contents.sports_tab_contents.specials import SpecialsTabContent
from voltron.pages.shared.contents.sports_tab_contents.sport_coupons_tab import CouponsTabContent
from voltron.pages.shared.contents.sports_tab_contents.sports_coupons_tab_desktop import CouponsTabContentDesktop
from voltron.pages.shared.contents.sports_tab_contents.competitions_tab_content_desktop import CompetitionsTabContentDesktop
from voltron.pages.shared.components.right_column_widgets.in_play_widget import WidgetAccordionList
from voltron.utils.waiters import wait_for_result


class SportPageBase(SportRacingPageBase):
    _tab_content = 'xpath=.//sport-matches-page | .//sport-tabs-page | .//*[@data-crlat="tabContent"] | .//insights-main'
    _in_play_widget = 'xpath=.//*[@data-uat="widgetColumn"]'
    _seo_static_block_section = 'xpath=.//seo-static-block/*[@data-crlat="accordion"]'
    _outrights_tab = OutrightsTabContent
    _jackpot_tab = JackpotTabContent
    _specials_tab = SpecialsTabContent
    _results_tab = ResultsTabContent
    _events_tab = MatchesTabContent
    _popular_bets_tab = PopularBetsTabContent
    _fade_out_overlay = True

    @property
    def _coupons_tab(self):
        return CouponsTabContent if get_device_properties()['type'] != 'desktop' else CouponsTabContentDesktop

    @property
    def _competitions_tab(self):
        return CompetitionsTabContent if get_device_properties()['type'] != 'desktop' else CompetitionsTabContentDesktop

    @property
    def _live_tab(self):
        from voltron.pages.shared.contents.sports_tab_contents.live import \
            LiveTabContent  # have to do this because of cross import error
        from voltron.pages.shared.contents.sports_tab_contents.live_desktop import LiveTabContentDesktop

        return LiveTabContent if get_device_properties()['type'] != 'desktop' else LiveTabContentDesktop

    @property
    def _matches_tab(self):
        return MatchesTabContent if get_device_properties()['type'] != 'desktop' else MatchesTabContentDesktop

    def _get_tabs(self):
        dict_ = {
            'live': self._live_tab,
            'matches': self._matches_tab,
            'competitions': self._competitions_tab,
            'coupons': self._coupons_tab,
            'outrights': self._outrights_tab,
            'jackpot': self._jackpot_tab,
            'specials': self._specials_tab,
            'results': self._results_tab,
            'events': self._events_tab,
            'popularbets': self._popular_bets_tab
        }
        return dict_

    @property
    def tab_content(self):
        url = get_driver().current_url.split('/')
        dict_ = self._get_tabs()
        try:
            if len(url)==5:
                self._tab_content_type = dict_[self.tabs_menu.current.lower()]
            else:
                tab_content_url = url[5].replace('?automationtest=true', '')
                self._tab_content_type = dict_[tab_content_url]
        except (KeyError, IndexError):
            pass
        self._logger.debug('*** Recognized Tab Content type: %s' % self._tab_content_type.__name__)
        return self._tab_content_type(selector=self._tab_content)

    @property
    def in_play_widget(self):
        return WidgetAccordionList(selector=self._in_play_widget, context=self._we)

    @property
    def seo_static_block_section(self):
        return SeoAccordion(selector=self._seo_static_block_section, context=self._we, timeout=10)

class SeoAccordion(Accordion):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _content = 'xpath=.//*[@data-crlat="seoBlockContent"]'
    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)
    @property
    def content(self):
        return self._get_webelement_text(selector=self._content, context=self._we)

    @property
    def has_content(self):
        if self._find_element_by_selector(selector=self._content, context=self._we) == None:
            return False
        return True

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException),brand=None):
        if tests.settings.device_type == 'desktop' and brand == 'bma':
            selector = 'xpath=./section[@data-crlat="accordion"]'
            element = self._find_element_by_selector(selector)
            result = wait_for_result(lambda: 'is-expanded' in element.get_attribute('class'),
                                     name=f'"{self.__class__.__name__}" Accordion to expand',
                                     expected_result=expected_result,
                                     bypass_exceptions=bypass_exceptions,
                                     timeout=timeout)
            result = result if result else False
            self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
            return result


        result = wait_for_result(lambda: 'is-expanded' in self.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result