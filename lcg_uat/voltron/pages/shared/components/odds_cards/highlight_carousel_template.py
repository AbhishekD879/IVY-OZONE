from collections import OrderedDict
from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from voltron.utils.waiters import wait_for_result


class HighlightCarouselTemplate(SportTemplate):
    _bet_button = 'xpath=.//*[@data-crlat="betButton"] | .//*[@data-crlat="oddsBtnContent"]'
    _one_button_section = 'xpath=.//*[@data-crlat="event"]'
    _odds_head = 'xpath= .//*[@class="odds-head"]'
    _see_all_link = 'xpath=.//*[@data-crlat="oddsHeader"]'
    _team_names = 'xpath= .//*[@data-crlat="oddsContent"]'
    _live_button = 'xpath= .//*[@data-crlat="liveLabel"]'
    _watch_live_button = 'xpath= .//*[@data-crlat="watchLive"]'
    _first_team_kit = 'xpath=(.//*[@class="odds-name"]/preceding-sibling::*)[1]'  # change after build to 'xpath=.//*[@data-crlat="firstTeamKit"]'
    _second_team_kit = 'xpath=(.//*[@class="odds-name"]/preceding-sibling::*)[2]'  # change after build to 'xpath=.//*[@data-crlat="secondTeamKit"]'
    _first_player_name = 'xpath=.//*[@class="odds-name-row"][1]'
    _second_player_name = 'xpath=.//*[@class="odds-name-row"][2]'
    _column_header = 'xpath=//*[@data-crlat="scoreTable"]//*[contains(@class,"sgp-tennis-header")]'  # only applicable for tennis
    _market_sign_post = 'xpath=.//*[@data-crlat="promotionIcon.two-up"]'  # only applicable for 2up markets

    @property
    def event_name(self):
        first_player_we = self._find_element_by_selector(selector=self._first_player_name, timeout=1)
        first = first_player_we.text if first_player_we.text else first_player_we.get_attribute('innerHTML')
        second_player_we = self._find_element_by_selector(selector=self._second_player_name, timeout=1)
        second = second_player_we.text if second_player_we.text else second_player_we.get_attribute('innerHTML')
        if first != '' and second != '':
            return f'{first} {self.draw_label} {second}'
        elif self._get_single_event_name() != '':
            return self._get_single_event_name()
        else:
            return ''

    @property
    def has_team_kits(self):
        first_team_kit = self._find_element_by_selector(selector=self._first_team_kit, timeout=1)
        second_team_kit = self._find_element_by_selector(selector=self._second_team_kit, timeout=1)
        if first_team_kit is None or second_team_kit is None:
            return False
        if first_team_kit.tag_name in ['svg', 'img'] and second_team_kit.tag_name in ['svg', 'img']:
            if first_team_kit.get_attribute('class') in ['crest-logo', 'teams-image'] and second_team_kit.get_attribute(
                    'class') in ['crest-logo', 'teams-image']:
                return True
        return False

    @property
    def see_all(self):
        return self._find_element_by_selector(selector=self._see_all_link, timeout=1)

    @property
    def bet_button(self):
        return self._find_element_by_selector(selector=self._bet_button, timeout=1)

    @property
    def odds_head(self):
        return self._find_element_by_selector(selector=self._odds_head, timeout=1)

    @property
    def live_button(self):
        return self._find_element_by_selector(selector=self._live_button, timeout=1)

    @property
    def watch_live_button(self):
        return self._find_element_by_selector(selector=self._watch_live_button, timeout=1)

    @property
    def team_names(self):
        return self._find_element_by_selector(selector=self._team_names, timeout=1)

    @property
    def score_column_headers(self):
        items_we = self._find_elements_by_selector(selector=self._column_header, context=self._we)
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            items_ordered_dict[self._get_webelement_text(we=item_we)] = item_we
        return items_ordered_dict

    def is_displayed(self, expected_result=True, timeout=1, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" displayed status is: {expected_result}'
        self.scroll_to_we() if scroll_to else None
        result = wait_for_result(lambda: self._we.is_displayed(),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=bypass_exceptions,
                                 name=name)
        return result

    @property
    def market_sign_post(self):
        return self._find_element_by_selector(selector=self._market_sign_post, timeout=1)

    def has_market_sign_post(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._market_sign_post, timeout=0) is not None,
            name=f'two up market sign post status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)