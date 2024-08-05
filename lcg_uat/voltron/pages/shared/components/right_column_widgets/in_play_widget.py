from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.right_column_widgets.right_column_item_widget import RightColumnItem
from voltron.utils.waiters import wait_for_result


class InPlayWidget(RightColumnItem):
    pass


class SlideHeader(ComponentBase):
    _header_title_selector = 'xpath=.//*[@data-crlat="inPlaySlideHeaderTitle"]'

    @property
    def header_title(self):
        return ComponentBase(selector=self._header_title_selector, context=self._we)


class InPlayScore(ComponentBase):
    _left_score = 'xpath=.//*[@data-crlat="inPlayScoresContainer"]'
    _game_status = 'xpath=.//*[@data-crlat="inPlayGameStatus.inPlayGameStatusBigger"]'
    _right_score = 'xpath=.//*[@data-crlat="inPlayScoresContainer.inPlayScoreReversed"]'

    @property
    def left_score(self):
        return ComponentBase(selector=self._left_score, context=self._we)

    @property
    def game_status(self):
        return ComponentBase(selector=self._game_status, context=self._we)

    @property
    def right_score(self):
        return ComponentBase(selector=self._right_score, context=self._we)


class InPlayCardBody(ComponentBase):
    _in_play_main_body_selector = 'xpath=.//*[@data-crlat="inPlayCardMainBody"]'
    _in_play_score_selector = 'xpath=.//*[@data-crlat="inPlayScore"]'
    _in_play_match_results_selector = 'xpath=.//*[@data-crlat="inPlayMatchResults"]'

    _in_play_first_participant = 'xpath=.//*[@data-crlat="inPlayParticipantContainer"]'
    _in_play_second_participant = 'xpath=.//*[@data-crlat="inPlayParticipantContainer.SecondParticipant"]'
    _in_play_live_icon = 'xpath=.//*[@class="in-play-game-status in-play-game-status__bigger"]'
    _in_play_favourites_icon = 'xpath=.//*[@class="in-play-icon in-play-fav-icon"]'
    _in_play_more_markets_link = 'xpath=.//*[@class="in-play-more-link-container"]'
    _in_play_outcome_name = 'xpath=.//*[@data-crlat="inPlayOutrightEventName"]'
    _left_score = 'xpath=.//*[@data-crlat="inPlayScoresContainer"]'
    _current_left_score = 'xpath=.//*[@data-crlat="inPlayScoresContainer"]/span[2]'
    _current_left_score_tn = 'xpath=.//*[@data-crlat="inPlayScore"]/div/span'
    _right_score = 'xpath=.//*[@data-crlat="inPlayScoresContainer.inPlayScoreReversed"]'
    _current_right_score = 'xpath=.//*[@data-crlat="inPlayScoresContainer.inPlayScoreReversed"]/span[2]'
    _current_right_score_tn = 'xpath=.//*[@data-crlat="inPlayScore"]/div[2]/span'

    @property
    def in_play_score(self):
        return InPlayScore(selector=self._in_play_score_selector, context=self._we)

    @property
    def match_results(self):
        return ComponentBase(selector=self._in_play_match_results_selector, context=self._we)

    @property
    def first_participant(self):
        return TextBase(selector=self._in_play_first_participant, context=self._we)

    @property
    def second_participant(self):
        return TextBase(selector=self._in_play_second_participant, context=self._we)

    @property
    def live_icon(self):
        return self._find_element_by_selector(selector=self._in_play_live_icon)

    @property
    def favourites_icon(self):
        return IconBase(selector=self._in_play_favourites_icon, context=self._we)

    @property
    def more_markets_link_inplay(self):
        return self._find_element_by_selector(selector=self._in_play_more_markets_link)

    @property
    def in_play_outcome_name(self):
        return TextBase(selector=self._in_play_outcome_name, context=self._we)

    @property
    def name(self):
        if self._find_element_by_selector(selector=self._in_play_first_participant, timeout=0):
            return self.first_participant.text + ' v ' + self.second_participant.text
        else:
            return self.in_play_outcome_name.text

    @property
    def left_score(self):
        return TextBase(selector=self._left_score, context=self._we).name

    @property
    def left_score_element(self):
        return self._find_element_by_selector(selector=self._left_score, context=self._we,
                                              timeout=2)

    @property
    def current_left_score(self):
        return TextBase(selector=self._current_left_score, context=self._we).name

    def current_left_score_element(self):
        return self._find_element_by_selector(selector=self._current_left_score, timeout=1)

    @property
    def current_left_score_tn(self):
        return TextBase(selector=self._current_left_score_tn, context=self._we).name

    def current_left_score_element_tn(self):
        return self._find_element_by_selector(selector=self._current_left_score_tn, timeout=1)

    @property
    def right_score(self):
        return TextBase(selector=self._right_score, context=self._we).name

    @property
    def right_score_element(self):
        return self._find_element_by_selector(selector=self._right_score, context=self._we,
                                              timeout=2)

    @property
    def current_right_score(self):
        return TextBase(selector=self._current_right_score, context=self._we).name

    def current_right_score_element(self):
        return self._find_element_by_selector(selector=self._current_right_score, timeout=1)

    @property
    def current_right_score_tn(self):
        return TextBase(selector=self._current_right_score_tn, context=self._we).name

    def current_right_score_element_tn(self):
        return self._find_element_by_selector(selector=self._current_right_score_tn, timeout=1)


class WidgetEventGroupSlide(ComponentBase):
    def __init__(self, *args, **kwargs):
        super(WidgetEventGroupSlide, self).__init__(*args, **kwargs)
        self.scroll_to_we(web_element=self._we)

    _fixture_header = 'xpath=.//*[@data-crlat="eventOddsHeader"]'
    _fixture_header_type = FixtureHeader
    _header_title_selector = 'xpath=.//*[@data-crlat="inPlaySlideHeader"]'
    _in_play_card_body_selector = 'xpath=.//*[@data-crlat="inPlayCardBody"]'
    _odds_buttons = 'xpath=.//*[@data-crlat="oddsButtons"]'
    _in_play_cash_out = 'xpath=.//*[@class="cashout-label"]'
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def slider_header(self):
        return SlideHeader(selector=self._header_title_selector, context=self._we)

    @property
    def in_play_card(self):
        return InPlayCardBody(selector=self._in_play_card_body_selector, context=self._we)

    @property
    def cashout_inplay_icon(self):
        return IconBase(selector=self._in_play_cash_out, context=self._we)

    def has_cashout_icon(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._in_play_cash_out, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Fixture header presence status in {self.__class__.__name__} to be {expected_result}')

    def has_fixture_header(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._fixture_header, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Fixture header presence status in {self.__class__.__name__} to be {expected_result}')

    @property
    def fixture_header(self):
        return self._fixture_header_type(selector=self._fixture_header, context=self._we)

    @property
    def name(self):
        return self.in_play_card.name

    @property
    def odds_buttons(self):
        return WidgetOddsButtons(selector=self._odds_buttons, context=self._we)


class WidgetAccordionContent(ComponentBase):
    _list_item_type = WidgetEventGroupSlide
    _item = 'xpath=.//*[@data-crlat="slideInPlayWidgetSlide"] | .//*[@class="slide in-play-widget-slide single-event"]'


class WidgetEventGroup(EventGroup):
    _content_type = WidgetAccordionContent
    _game_status = 'xpath=.//*[@data-crlat="inPlayGameStatus"]'
    _name = 'xpath=.//*[@data-crlat="containerHeader"]'
    _view_all_inplay_events = 'xpath=.//a[@data-crlat="showMore"]'
    _right_arrow = 'xpath=.//*[contains(@class, "action-arrow right")]'
    _left_arrow = 'xpath=.//*[contains(@class, "action-arrow left")]'

    @property
    def name(self):
        raw_name = self._get_webelement_text(selector=self._name, timeout=0.5)
        name = raw_name.replace('\n', ' ').replace('In-Play', 'In-Play ').replace('  ', ' ')
        return name

    @property
    def game_status(self):
        return EventGroup(selector=self._game_status, context=self._we)

    @property
    def view_all_inplay_events(self):
        return self._find_element_by_selector(selector=self._view_all_inplay_events, context=self._we)

    @property
    def right_arrow(self):
        return self._find_element_by_selector(selector=self._right_arrow, context=self._we)

    @property
    def left_arrow(self):
        return self._find_element_by_selector(selector=self._left_arrow, context=self._we)


class WidgetAccordionList(AccordionsList):
    _list_item_type = WidgetEventGroup


class WidgetTabContent(TabContent):
    _accordions_list_type = WidgetAccordionList


class WidgetBetButton(BetButton):

    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" enabled status is: {expected_result}'

        def _is_enabled(we):
            if we.get_attribute('disabled') is not None:
                return any([False for status in ('true', 'disabled') if status in we.get_attribute('disabled')])
            else:
                return True

        result = wait_for_result(lambda: _is_enabled(we=self),
                                 expected_result=expected_result,
                                 poll_interval=poll_interval,
                                 name=name,
                                 timeout=timeout,
                                 bypass_exceptions=bypass_exceptions)
        return result


class WidgetOddsButtons(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="betButton"]'
    _list_item_type = WidgetBetButton
