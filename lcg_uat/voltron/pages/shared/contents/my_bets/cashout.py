import re
from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from voltron.pages.shared import get_device, get_driver
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.bet_receipt_info import BetReceiptInfo
from voltron.pages.shared.components.primitives.amount_field import AmountField
from voltron.pages.shared.components.primitives.buttons import BetNowButton
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.buttons import SpinnerButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.contents.edp.racing_edp_market_section import MyStableBookMark, MyBetsMyStableBookMark
from voltron.pages.shared.contents.my_stable.my_stable_page import MyStableNotes
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


class BetLegIcon(ComponentBase):
    _status = 'xpath=.//*[contains(@data-crlat, "leg.status.")]'

    @property
    def status(self):
        status_icon = self._find_element_by_selector(selector=self._status, timeout=1)
        status_icon_name = status_icon.get_attribute('data-crlat')
        match = re.match(r'^leg.status.(\w+)$', status_icon_name)
        if not match:
            raise VoltronException('Cannot get BetLeg status from "%s"' % status_icon_name)
        return match.group(1)


class Silk(ComponentBase):
    _silk_presence = 'xpath=.//*[contains(@data-crlat, "silk.")]'
    _generic_silk = 'xpath=.//*[@data-crlat="silk.generic"]'
    _image_silk = 'xpath=.//*[@data-crlat="silk.image"]'
    _silk_style = 'xpath=.//*[@data-crlat="silk.image.style"]'

    @property
    def is_shown(self):
        return self._find_element_by_selector(selector=self._silk_presence, timeout=1) is not None

    @property
    def is_generic(self):
        return self._find_element_by_selector(selector=self._generic_silk, timeout=1) is not None

    @property
    def is_image(self):
        return self._find_element_by_selector(selector=self._image_silk, timeout=1) is not None

    @property
    def style(self):
        we = ComponentBase(selector=self._silk_style, context=self._we, timeout=1)
        return we.get_attribute('style')


class BetLegOutcome(ComponentBase):
    _outcome_name = 'xpath=.//*[@data-crlat="selectionName"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._outcome_name).replace('(', '').replace(')', '')


class BybOutcome(ComponentBase):
    _outcome_title = 'xpath=.//*[@data-crlat="outcomeTitle"] | .//*[@class="outcome-title"]'
    _outcome_desc = 'xpath=.//*[@data-crlat="outcomeDesc"]'

    @property
    def name(self):
        outcome_title = self._get_webelement_text(selector=self._outcome_title)
        outcome_desc = self._get_webelement_text(selector=self._outcome_desc)
        return f"{outcome_desc} {outcome_title}"


class BybSelections(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="bybOutcome"]'
    _list_item_type = BybOutcome


class Signposting(ComponentBase):
    _value = 'xpath=./*'

    @property
    def value(self):
        return self._find_element_by_selector(selector=self._value, context=self._we).get_attribute('xlink:href')


class BetLeg(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="outcomeInfo"]'
    _list_item_type = BetLegOutcome
    _byb_selections = 'xpath=.//*[@data-crlat="bybSections"] | .//byb-selections'
    _bet_tracking_icon = 'xpath=.//*[contains(@class, "leg-indicator")]/*/*'
    _outcome_name = 'xpath=.//*[@data-crlat="selectionName"]'
    _market_name = 'xpath=.//*[@data-crlat="marketName"]'
    _each_way_terms = 'xpath=.//*[@class="each-way-terms"]'
    _event_name = 'xpath=.//*[@data-crlat="eventName"]'
    _edit_my_acca_remove_icon = 'xpath=.//*[@data-crlat = "removeIcon"]'
    _edit_my_acca_undo_icon = 'xpath=.//*[@data-crlat = "undoButton"]'
    _leg_remove_marker = 'xpath=.//*[@data-crlat = "legRemoveMarker"]'
    _event_start_time = 'xpath=.//*[@data-uat="eventStartTime" or @data-crlat="cashout.eventDate"]'
    _odds_value = 'xpath=.//*[@data-crlat="oddsValue"]'
    _event_time = 'xpath=.//*[@data-crlat="timerLabel"]'
    _live_label = 'xpath=.//*[@data-crlat="liveLabel"]'
    _stream_icon = 'xpath=.//*[@data-crlat="watchLive"]'
    _leg_status_icon = 'xpath=.//*[@data-crlat="legStatusContainer"]'
    _silk = 'xpath=.//*[@data-crlat="silks"][*]'
    _race = 'xpath=.//*[@data-crlat="raceNumber"]'
    _promo_icon = 'xpath=.//*[@data-crlat="promo.icon"]'
    _promo_label = 'xpath=.//*[@data-crlat="promo.label"]'
    _share_button = 'xpath=.//*[@data-crlat="shareBtn"]'
    _my_stable_bookmark = 'xpath=.//*[@data-crlat="bsMystableBookmark"]'
    _my_stable_signposting = 'xpath=.//*[@data-crlat="myStableSignpostingSvg"]'
    _my_stable_notes_signposting = 'xpath=.//*[@data-crlat="myStableNotesSignpostingSvg"]'
    _my_stable_notes = 'xpath=.//*[@data-crlat="myStableNotes"]'
    _my_stable_bookmark_state = 'xpath=.//*[@data-crlat="bsMystableBookmark"]/*/*'
    _extra_place_icon = 'xpath=.//*[@class="extra-place-sp-container"]'
    _draw_number = 'xpath=.//*[@data-crlat="outcomeDraw"]'
    _extra_place_icon_text = 'xpath=.//*[@class="extraplacesignpostOffer openbets_lads bet-leg-item-bet"]|.//*[@class="extraplacesignpostOffer openbets_coral bet-leg-item-bet"]'
    _open_bet_promotions = 'xpath=.//*[@class="bet-promotions"]'
    _open_bet_promotion_icon_text = 'xpath=.//*[@class="icon-text"]'
    _watch_live_icon = 'xpath=.//*[@class="btn-icon video-stream-icon"]'
    _insights_label = 'xpath=.//*[contains(text(), "Insights")]'
    _video_stream = 'xpath=.//*[data-crlat="eventVideoStreamArea"]'
    _home_team = 'xpath=(.//*[@data-crlat="eventName"])[1]'
    _away_team = 'xpath=(.//*[@data-crlat="eventName"])[2]'
    _score = 'xpath=.//live-scores'
    _home_team_score = 'xpath=.//*[@data-crlat="home.team.score"]'
    _away_team_score = 'xpath=.//*[@data-crlat="away.team.score"]'

    def has_my_stable_notes_sign_posting(self, expected_result=True, poll_interval=0.5, timeout=5) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_notes_signposting, context=self._we,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – My Stable  Notes Sign Posting status to be {expected_result}',
            expected_result=expected_result,
            poll_interval=poll_interval,
            timeout=timeout)

    def has_video_stream(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._video_stream,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Video stream displayed status to be {expected_result}')

    @property
    def watch_live_icon(self):
        return ButtonBase(selector=self._watch_live_icon, context=self._we)

    def has_watch_live_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._watch_live_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Watch Live icon displayed status to be {expected_result}')

    def has_my_stable_sign_posting(self, expected_result=True, poll_interval=0.5, timeout=5) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._my_stable_signposting, context=self._we,
                                                   timeout=0) is not None,
            name=f'{self.__class__.__name__} – My Stable shown status to be {expected_result}',
            expected_result=expected_result,
            poll_interval=poll_interval,
            timeout=timeout)

    @property
    def my_stable_signposting(self):
        return Signposting(selector=self._my_stable_signposting, context=self._we)

    @property
    def my_stable_notes(self):
        return MyStableNotes(selector=self._my_stable_notes, context=self._we)

    @property
    def my_stable_bookmark(self):
        return MyBetsMyStableBookMark(selector=self._my_stable_bookmark, context=self._we)

    @property
    def home_team_score(self):
        return ComponentBase(selector=self._home_team_score, context=self._we)

    @property
    def away_team_score(self):
        return ComponentBase(selector=self._away_team_score, context=self._we)

    @property
    def event_start_time(self):
        return TextBase(selector=self._event_start_time, context=self._we)

    @property
    def home_team(self):
        return ComponentBase(selector=self._home_team, context=self._we)

    @property
    def away_team(self):
        return ComponentBase(selector=self._away_team, context=self._we)

    @property
    def score(self):
        return ComponentBase(selector=self._score, context=self._we)

    @property
    def bet_promotion(self):
        return self._find_element_by_selector(selector=self._open_bet_promotions, context=self._we, timeout=1)

    def has_bet_promotion(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._open_bet_promotions,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet Promotion status to be {expected_result}')

    @property
    def bet_promotion_icon_text(self):
        return self._get_webelement_text(selector=self._open_bet_promotion_icon_text, context=self._we)

    def has_my_stable_bookmark(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._my_stable_bookmark,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'my stable bookmark status to be {expected_result}')

    @property
    def bet_share_button(self):
        return ButtonBase(selector=self._share_button, timeout=0.5)

    def has_bet_share_button(self, expected_result=True):
        return wait_for_result(lambda: ButtonBase(selector=self._share_button, timeout=0) is not None,
                               bypass_exceptions=(
                               NoSuchElementException, StaleElementReferenceException, VoltronException),
                               name=f'Close button shown status to be "{expected_result}"'
                               )

    @property
    def draw_number(self):
        return self._get_webelement_text(selector=self._draw_number, context=self._we)

    @property
    def byb_selections(self):
        return BybSelections(selector=self._byb_selections, context=self._we)

    @property
    def bet_tracking_icon(self):
        return self._find_element_by_selector(selector=self._bet_tracking_icon).get_attribute('xlink:href')

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name, timeout=0.5).replace('\n', ' ').replace('(',
                                                                                                              '').replace(
            ')', '')

    @property
    def outcome_names(self):
        elements = self._find_elements_by_selector(self._outcome_name, timeout=0)
        return [self._get_webelement_text(we=element).replace('(', '').replace(')', '') for element in elements]

    def is_outcome_name_truncated(self):
        return self.is_truncated(selector=self._outcome_name)

    def is_outcome_name_wrapped(self):
        return self.is_wrapped(selector=self._outcome_name)

    @property
    def market_name(self):
        market_name = self._get_webelement_text(selector=self._market_name)
        if market_name.upper() == "WIN OR EACH WAY":
            market_name = market_name+" "+self._get_webelement_text(selector=self._each_way_terms)
        return market_name

    @property
    def has_market_name(self):
        return self._find_element_by_selector(selector=self._market_name, timeout=0)

    def is_market_name_truncated(self):
        return self.is_truncated(selector=self._market_name)

    def is_market_name_wrapped(self):
        return self.is_wrapped(selector=self._market_name)

    @property
    def event_name(self):
        initial_elements = self._find_elements_by_selector(selector=self._event_name, timeout=0.6)
        initial_string = ' v '.join([self._get_webelement_text(we=element) for element in initial_elements])
        event_name = normalize_name(initial_string)
        return event_name

    @property
    def event_start_time(self):
        return TextBase(selector=self._event_start_time, context=self._we)

    def click_event_name(self):
        we = self._find_element_by_selector(selector=self._event_name)
        if we:
            event_name = ButtonBase(web_element=we)
            event_name.click()
        else:
            raise VoltronException('No event name found')

    def is_event_name_truncated(self):
        return self.is_truncated(selector=self._event_name)

    def is_event_name_wrapped(self):
        return self.is_wrapped(selector=self._event_name)

    @property
    def edit_my_acca_remove_icon(self):
        return ComponentBase(selector=self._edit_my_acca_remove_icon, context=self._we)

    def has_edit_my_acca_remove_icon(self, timeout=1, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._edit_my_acca_remove_icon, timeout=0) is not None,
            name=f'Remove icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def edit_my_acca_undo_icon(self):
        return ComponentBase(selector=self._edit_my_acca_undo_icon, context=self._we)

    @property
    def leg_remove_marker(self):
        return ComponentBase(selector=self._leg_remove_marker, context=self._we)

    @property
    def has_link(self):
        return LinkBase(selector=self._event_name, context=self._we).get_link() is not None

    @property
    def odds_value(self):
        return self._get_webelement_text(selector=self._odds_value, timeout=0.4)

    @property
    def odds_sign(self):
        return self.before_element(selector=self._odds_value, context=self._we)

    @property
    def event_time(self):
        return self._get_webelement_text(selector=self._event_time, timeout=0.3)

    @property
    def has_live_label(self):
        return self._find_element_by_selector(selector=self._live_label, timeout=2) is not None

    @property
    def has_stream_icon(self):
        return self._find_element_by_selector(selector=self._stream_icon, timeout=2) is not None

    @property
    def name(self):
        return f'{self.outcome_name} - {self.event_name} {self.event_time}' if self.event_time else \
            f'{self.outcome_name} - {self.event_name}'

    @property
    def event_id(self):
        return self.get_attribute('data-eventid')

    @property
    def icon(self):
        return BetLegIcon(selector=self._leg_status_icon, context=self._we)

    def has_icon_status(self, timeout=1, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._leg_status_icon, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def silk(self):
        return Silk(selector=self._silk, context=self._we)

    def has_silk(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._silk, timeout=0) is not None,
                               name=f'Silk to be displayed: "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def race_number(self):
        return self._get_webelement_text(selector=self._race, context=self._we)

    def has_promo_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._promo_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')

    @property
    def promo_icon(self):
        return self._find_element_by_selector(selector=self._promo_icon, timeout=10, context=self._we)

    @property
    def promo_label_text(self):
        return self._get_webelement_text(selector=self._promo_label)

    def has_extra_place_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._extra_place_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')

    @property
    def extra_place_icon_text(self):
        return self._get_webelement_text(selector=self._extra_place_icon_text)
    @property
    def extra_place_icon(self):
        return self._find_element_by_selector(selector=self._extra_place_icon,timeout=0)

    @property
    def selection(self):
        return ComponentBase(selector=self._outcome_name, context=self._we)

    @property
    def market(self):
        return ComponentBase(selector=self._market_name, context=self._we)

    @property
    def event(self):
        return ComponentBase(selector=self._event_name, context=self._we)

    @property
    def odds(self):
        return ComponentBase(selector=self._odds_value, context=self._we)


class CashoutButton(SpinnerButtonBase):
    _button_label = 'xpath=.//*[@data-crlat="cashOutButton.label"]'
    _button_value = 'xpath=.//*[@data-crlat="cashOutButton.value"]'
    _context_timeout = 2

    @property
    def label(self):
        return self._get_webelement_text(selector=self._button_label)

    @property
    def amount(self):
        return AmountField(selector=self._button_value, context=self._we)

    @property
    def name(self):
        return f'{self.label} {self.amount.currency}{self.amount.value}'

    def wait_amount_to_change(self, initial_amount):
        return wait_for_result(lambda: str(initial_amount) != str(self.amount.value),
                               name='Amount to change',
                               timeout=10)

    def click(self):
        self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')


class PartialCashoutButtonAmount(AmountField):
    _integer_part_value = 'xpath=.//*[@data-crlat="partCashout.intPart"]/.//*[contains(@data-crlat, "scoreDigit-")]'
    _decimal_part_value = 'xpath=.//*[@data-crlat="partCashout.decPart"]/.//*[contains(@data-crlat, "scoreDigit-")]'
    _currency_symbol = 'xpath=.//*[@data-crlat="currencySymbol"]'

    def _get_amount_value(self):
        integer_part_value = self._find_elements_by_selector(selector=self._integer_part_value, timeout=0)
        decimal_part_value = self._find_elements_by_selector(selector=self._decimal_part_value, timeout=0)
        integer_part = integer_part_value[0].get_attribute("data-crlat").split('-')[1]
        decimal_part = decimal_part_value[0].get_attribute("data-crlat").split('-')[1]
        if integer_part is None or decimal_part is None:
            raise VoltronException(f'Cannot get text from web element "{integer_part}" "{decimal_part}"')
        decimal_part_value = decimal_part.split('\n')[-1]
        integer_part = 0 if not integer_part else integer_part
        decimal_part_value = 0 if not decimal_part_value else decimal_part_value
        amount = f'{int(integer_part)}.{int(decimal_part_value)}'
        return amount

    def _wait_for_amount_value(self):
        wait_for_amount = wait_for_result(lambda: self._get_amount_value() != '0.00',
                                          name=f'Partial Cashout amount value to render, '
                                               f'current value is: "{self._get_amount_value()}"',
                                          bypass_exceptions=(ValueError, NoSuchElementException,
                                                             StaleElementReferenceException),
                                          timeout=3)
        if not wait_for_amount:
            raise VoltronException('Cannot get Partial Cashout amount value')

    @property
    def value(self):
        self._wait_for_amount_value()
        return self._get_amount_value()

    @property
    def currency(self):
        return self._get_webelement_text(selector=self._currency_symbol)


class PartialCashoutButton(CashoutButton):
    _amount = 'xpath=.//*[@data-crlat="partialCashoutAmount"]'

    def _wait_active(self, timeout=0):
        self._we = self._find_myself()
        wait_for_result(
            lambda: 'animating' not in self.get_attribute('class'),
            timeout=2,
            name=f'Cash out button to become clickable')

    @property
    def amount(self):
        return PartialCashoutButtonAmount(selector=self._amount, context=self._we)


class CashoutMessage(TextBase):
    _label = 'xpath=.//*[@data-crlat="cashOutButton.label"]'
    _text = 'xpath=.//*[@data-crlat="cashOutButton.value"]'

    @property
    def text(self):
        return self._get_webelement_text(selector=self._text, timeout=1)


class ButtonsPanel(BetNowButton):
    _full_cashout_button = 'xpath=.//*[@data-crlat="button.doFullCashOut"]'
    _partial_cashout_button = 'xpath=.//*[@data-crlat="button.doPartialCashOut"]'
    _cashout_button = 'xpath=.//*[@data-crlat="cashOutButton"]'
    _partial_cashout_slider = 'xpath=.//*[@data-crlat="panel.showSlider"]'
    _partial_cashout_close_button = 'xpath=.//*[@data-crlat="button.doFullCashOut"][.//*[@data-crlat="closePartialCashOut"]]'
    _message = 'xpath=.//*[@data-crlat="panel.showButton"]'
    _message_type = CashoutMessage
    _timer = 'xpath=.//*[@data-crlat="timer"]'
    _spinner = 'xpath=.//*[@data-crlat="spinner.loader"]'
    _pre_cashout_button = None

    @property
    def cashout_message(self):
        return self._message_type(selector=self._message, context=self._we, timeout=3)

    @property
    def full_cashout_button(self):
        full_cashout = CashoutButton(selector=self._full_cashout_button, context=self._we)
        if full_cashout:
            self.__class__._pre_cashout_button = 'FULL_CASHOUT_BUTTON'
        return full_cashout

    @property
    def partial_cashout_button(self):
        partail_cashout = PartialCashoutButton(selector=self._partial_cashout_button, context=self._we, timeout=2)
        if partail_cashout:
            self.__class__._pre_cashout_button = 'PARTIAL_CASHOUT_BUTTON'
        return partail_cashout

    def has_partial_cashout_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._partial_cashout_button,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet button shown status to be {expected_result}')

    def has_full_cashout_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._full_cashout_button,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Cashout button shown status to be {expected_result}')

    def has_confirm_cashout_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cashout_button,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Confirm Cashout button shown status to be {expected_result}')

    @property
    def has_partial_cashout_slider(self):
        return self._find_element_by_selector(selector=self._partial_cashout_slider, context=self._we,
                                              timeout=0) is not None

    def move_partial_cashout_slider(self, direction='right'):
        we = self._find_element_by_selector(self._partial_cashout_slider, context=self._we, timeout=3)
        self.scroll_to()
        actions = ActionChains(get_driver())
        actions.move_to_element(we)
        actions.click_and_hold(we)
        if 'right' in direction:
            actions.send_keys(Keys.PAGE_UP)
        else:
            actions.send_keys(Keys.PAGE_DOWN)
        actions.release().perform()

    @property
    def partial_cashout_close_button(self):
        return CashoutButton(selector=self._partial_cashout_close_button, context=self._we)

    @property
    def cashout_button(self):
        if self._pre_cashout_button == "FULL_CASHOUT_BUTTON":
            get_driver().execute_script(f"""
                         const interval = setInterval(()=>arguments[0].dispatchEvent(new Event('click')),3000);
                         setTimeout(()=>clearInterval(interval),8000);
                        """, self.full_cashout_button._we)
        elif self._pre_cashout_button == "PARTIAL_CASHOUT_BUTTON":
            get_driver().execute_script(f"""
                        const interval = setInterval(()=>arguments[0].dispatchEvent(new Event('click')),3000);
                        setTimeout(()=>clearInterval(interval),8000);
                        """, self.partial_cashout_button._we)
        try:
            return CashoutButton(selector=self._cashout_button, context=self._we, timeout=5)
        except Exception:
            return CashoutButton(selector=self._cashout_button, context=self._we, timeout=5)

    def has_cashout_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cashout_button,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet button shown status to be {expected_result}')

    @property
    def timer(self):
        return TextBase(selector=self._timer, context=self._we, timeout=3)

    def has_timer(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._timer,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Timer shown status to be {expected_result}')

    def wait_for_message(self,
                         message,
                         expected_result=True,
                         timeout=10,
                         bypass_exceptions=(NoSuchElementException,
                                            StaleElementReferenceException,
                                            VoltronException)):
        raise VoltronException(
            'Now messages will not appear on button panel, but will appear below it, please update test case')

    def wait_for_cashout_slider(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self.has_partial_cashout_slider,
                               expected_result=expected_result,
                               name='Cashout slider to be displayed',
                               timeout=timeout)

    def wait_for_value_change(self, initial_value, timeout=5):
        return wait_for_result(lambda: float(self.full_cashout_button.amount.value) != initial_value, timeout=timeout,
                               name='Cashout value was not changed')

    def wait_for_cashout_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cashout_button,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Cashout button shown status to be {expected_result}')


class NavigationDot(ComponentBase):
    pass


class NavigationDots(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="navigationDot"]'
    _list_item_type = NavigationDot

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict(
            [
                (items_we.index(item_we),
                 self._list_item_type(web_element=item_we)) for item_we in items_we
            ]
        )
        return items_ordered_dict


class TextBaseStake(TextBase):

    @property
    def _parsed_string(self):
        text = self.value
        matched = re.match(u'^(£|\$|€|Kr)([0-9.,]+)$', text, re.U)
        if matched is not None and matched.group(2) is not None:
            currency_symbol = matched.group(1)
            amount = matched.group(2)
            return currency_symbol, amount
        else:
            self._logger.error('*** Failed parsing string: "%s"' % text)
            return '', text

    @property
    def currency(self):
        return self._parsed_string[0]

    @property
    def stake_value(self):
        return self._parsed_string[1]


class BetDetails(ComponentBase):
    _share_button = 'xpath=.//*[@data-crlat="shareBtn"]'
    _bet_details_chevron_arrow = 'xpath=.//*[@data-crlat="chevronArrow"]'
    _bet_date_time = 'xpath=.//*[@class="bet-receipt bet-recipt-date"]'
    _bet_type = 'xpath=.//*[@class="bet-details-info bet-type"]'
    _bet_number_of_lines = 'xpath=.//*[@class="bet-details-info bet-num-lines"]'
    _bet_stake_per_line = 'xpath=.//*[@class="bet-details-info bet-stake--per-line"]'
    _bet_total_stake = 'xpath=.//*[@class="bet-details-info total-stake"]'
    _bet_potential_returns = 'xpath=.//*[@class="bet-details-info potential-returns"]'
    _bet_settled = 'xpath=(.//*[@class="bet-details-info total-stake"])[2]'
    _bet_number_of_winning_lines = 'xpath=.//*[@class="bet-details-info winning-lines"]'
    _bet_number_of_losing_lines = 'xpath=.//*[@class="bet-details-info losing-lines"]'
    _date = 'xpath=.//*[@data-crlat="displayDate"]'
    _bet_receipt = 'xpath=.//*[@class="bet-receipt bet-receipt-info"]'
    _bet_id = 'xpath=.//*[@data-uat="betId"]'

    def has_share_button(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._share_button, timeout=timeout, context=self._we),
            name=f'Share button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_share_dialog(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._share_dialog, timeout=timeout, context=self._we),
            name=f'Share dialog shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def share_button(self):
        return ButtonBase(selector=self._share_button, context=self._we)

    @property
    def chevron_arrow(self):
        return ButtonBase(selector=self._bet_details_chevron_arrow, context=self._we)

    def is_expanded(self, timeout=1, expected_result=True):
        result = wait_for_result(lambda: 'is-expanded' in self.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    @property
    def bet_id(self):
        return self._get_webelement_text(selector=self._bet_id, context=self._we)

    @property
    def bet_date_time(self):
        return self._get_webelement_text(selector=self._bet_date_time, context=self._we)

    @property
    def bet_type(self):
        return self._get_webelement_text(selector=self._bet_type, context=self._we)

    @property
    def bet_number_of_lines(self):
        return self._get_webelement_text(selector=self._bet_number_of_lines, context=self._we)

    @property
    def bet_stake_per_line(self):
        return self._get_webelement_text(selector=self._bet_stake_per_line, context=self._we)

    @property
    def bet_total_stake(self):
        return self._get_webelement_text(selector=self._bet_total_stake, context=self._we)

    @property
    def bet_potential_returns(self):
        return self._get_webelement_text(selector=self._bet_potential_returns, context=self._we)

    @property
    def bet_settled(self):
        return self._get_webelement_text(selector=self._bet_settled, context=self._we)

    @property
    def bet_number_of_winning_lines(self):
        return self._get_webelement_text(selector=self._bet_number_of_winning_lines, context=self._we)

    @property
    def bet_number_of_losing_lines(self):
        return self._get_webelement_text(selector=self._bet_number_of_losing_lines, context=self._we)

    @property
    def date(self):
        return TextBase(selector=self._date, context=self._we)

    @property
    def bet_receipt(self):
        return TextBase(selector=self._bet_receipt, context=self._we)


class Bet(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="cashout.betLeg" and not(contains(@class, "carousel-slide-copy"))]'
    _list_item_type = BetLeg
    _bet_status = 'xpath=.//*[@data-crlat="leg.status.cashed out" or @data-crlat="cashout.totalStatus"]'
    _header = 'xpath=.//*[@data-crlat="cashout.item.header"]'
    _edit_my_acca_button = 'xpath=.//*[@data-crlat="editMyAccaButton"]'
    _confirm_button = 'xpath=.//*[@data-crlat="confirmButton"]'
    _show_edit_history_button = 'xpath=.//*[@data-crlat="buttonShowHistory"]'
    _edit_my_acca_warning_message = 'xpath=.//*[@data-crlat="warningMessage"]'
    _stake = 'xpath=.//*[@data-crlat="stake"]'
    _unit_stake = 'xpath=.//*[@data-crlat="unit_stake"]'
    _est_returns = 'xpath=.//*[@data-crlat="estimatedReturns"]'
    _buttons_panel = 'xpath=.//*[@data-crlat="cashoutPanel"]'
    _buttons_panel_type = ButtonsPanel
    _navigation_dots = 'xpath=.//*[@data-crlat="section.navigationDots"]'
    _cashed_out_mark = 'xpath=.//*[@data-crlat="cashedOutMark"]'
    _cash_out_error_message = 'xpath=.//*[@data-crlat="cashoutErrorMessage"]'
    _cash_out_successful_message = 'xpath=.//*[@data-crlat="emaText"]'
    _cash_out_successful_icon = 'xpath=.//*[@data-crlat="emaIcon"]'
    _cashed_out_label = 'xpath=.//*[@data-crlat="cashedOutLabel"]'
    _cashed_out_value = 'xpath=.//*[@data-crlat="cashedOutValue"]'
    _odds_boost_signpost = 'xpath=.//*[@id="boost-icon"] | .//*[contains(@class,"boosted")]'
    _odds_boost_text = 'xpath=.//*[@class="icon-text"]'
    _acca_insurance_icon = 'xpath=.//div[contains(@class,"acca-insurance")]'
    _verify_spinner = True
    _bog_icon = 'xpath=.//*[@class="bog-icon"] | .//*[@data-crlat="bogIcon"]'
    _odds_bog = 'xpath=.//*[contains(@class,"single-selection-odds-bog")]'
    _acca_tooltip = 'xpath=.//*[contains(@class, "tooltip tooltip-container")]'
    _partial_cash_out_history = 'xpath=.//*[contains(@data-crlat, "panel.cashOutHistory")]'
    _moneyback_icon = 'xpath=.//*[contains(@class,"money-back")]'
    _odds = 'xpath=.//*[@data-crlat="oddsValue"]'
    _potential_returns_label = 'xpath=.//*[@data-crlat="estimatedReturns"]//*[@data-crlat="label"]'
    _potential_returns_value = 'xpath=.//*[@data-crlat="estimatedReturns"]//*[@data-crlat="value"]'
    _chevron_arrow = 'xpath=.//*[@data-crlat="chevronArrow"]'
    _bet_details = 'xpath=.//*[contains(@class,"betDetailsAccordion-lads")] | .//*[contains(@class,"betDetailsAccordion-coral")]/*[@data-crlat="accordion"]'
    _free_bet_icon = 'xpath=.//*[@data-crlat="fbIcon"]'
    _free_bet_value = 'xpath=.//*[@data-crlat="fbValue"]'
    _you_cashed_out_message = 'xpath=.//*[contains(@class,"top-success-message")]'
    _max_payout_msg = 'xpath=.//*[@data-crlat="maxPayoutMsg"]'
    _max_payout_link = 'xpath=.//*[@data-crlat="maxPayOutLink"]'
    _potential_returns = 'xpath=.//*[@data-crlat="estimatedReturns"]/..'
    _insights_label = 'xpath=.//*[contains(text(), "Insights")]'

    def has_insights_label(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._insights_label,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet Promotion status to be {expected_result}')

    @property
    def odds_boost_text(self):
        return self._get_webelement_text(selector=self._odds_boost_text, timeout=0.5)

    def has_odds_boost_text(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._odds_boost_text,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Odds boost text status to be {expected_result}')

    def has_navigation_dots(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._navigation_dots,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Dots status to be {expected_result}')

    @property
    def navigation_dots(self):
        return NavigationDots(selector=self._navigation_dots, context=self._we, timeout=3)

    @property
    def bet_type(self):
        return ' '.join(
            self._get_webelement_text(selector=self._header, timeout=0.5).replace('\n', ' ').split()).rstrip()

    def has_header(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._header,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Header shown status to be {expected_result}')

    @property
    def edit_my_acca_button(self):
        return ButtonBase(selector=self._edit_my_acca_button, context=self._we)

    def has_edit_my_acca_button(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._edit_my_acca_button,
                                                                      timeout=0,
                                                                      bypass_exceptions=NoSuchElementException) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name='"Edit My Bet" button to be displayed')

    def has_odds_boost_signpost(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._odds_boost_signpost, timeout=1) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Odds boost sign post status to be "{expected_result}"')

    def has_acca_insurance_icon(self, expected_result=True, timeout=15):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._acca_insurance_icon, timeout=15) is not None,
            timeout=timeout,
            name=f'"Acca Insurance Icon" presence to be {expected_result}',
            expected_result=expected_result)

    @property
    def confirm_button(self):
        return SpinnerButtonBase(selector=self._confirm_button, context=self._we)

    @property
    def show_edit_history_button(self):
        return ButtonBase(selector=self._show_edit_history_button, context=self._we)

    @property
    def edit_my_acca_warning_message(self):
        return self._get_webelement_text(selector=self._edit_my_acca_warning_message, context=self._we)

    @property
    def name(self):
        """
        :return name in format:
        "{bet type} - [{all_event_names}]", e.g. 'TRIPLE - [Diana v Christine, North v Michael, Liverpool v Stengel]'
        """
        return '%s - [%s]' % (self.bet_type, ', '.join(
            ['%s %s' % (bet_leg.event_name, bet_leg.event_time) if bet_leg.event_time else bet_leg.event_name
             for (bet_leg_name, bet_leg) in self.items_as_ordered_dict.items()]))

    @property
    def stake(self):
        return TextBaseStake(selector=self._stake, context=self._we, timeout=1)

    @property
    def unit_stake(self):
        return TextBaseStake(selector=self._unit_stake, context=self._we)

    @property
    def bet_status(self):
        return self._get_webelement_text(selector=self._bet_status, context=self._we, timeout=1)

    @property
    def est_returns(self):
        return TextBaseStake(selector=self._est_returns, context=self._we)

    @property
    def buttons_panel(self):
        return self._buttons_panel_type(selector=self._buttons_panel, context=self._we, timeout=2)

    def has_buttons_panel(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._buttons_panel,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'"Button Panel" to be displayed')

    def has_cashed_out_mark(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cashed_out_label,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name='"Cashed out message" to be displayed') # Cashout mark no longer available. Only message will be there

    def has_cash_out_error_message(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cash_out_error_message,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name='Cash Out error message to be displayed')

    @property
    def cash_out_error_message(self):
        return self._get_webelement_text(selector=self._cash_out_error_message, context=self._we)

    @property
    def cash_out_successful_message(self):
        return self._get_webelement_text(selector=self._cash_out_successful_message, context=self._we, timeout=11)

    @property
    def cash_out_successful_icon(self):
        return IconBase(selector=self._cash_out_successful_icon, context=self._we)

    @property
    def cashed_out_message(self):
        return TextBase(selector=self._cashed_out_label, context=self._we)

    @property
    def cashed_out_value(self):
        return TextBase(selector=self._cashed_out_value, context=self._we)

    def wait_for_message(self,
                         message,
                         expected_result=True,
                         timeout=10,
                         bypass_exceptions=(NoSuchElementException,
                                            StaleElementReferenceException,
                                            VoltronException)):
        return wait_for_result(lambda: message in self.cash_out_successful_message,
                               name=f'Message "{message}" shown status in status field to be "{expected_result}"',
                               bypass_exceptions=bypass_exceptions,
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def bog_icon(self):
        return self._find_element_by_selector(selector=self._bog_icon, context=self._we)

    @property
    def has_bog_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bog_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet Promotion status to be {expected_result}')

    @property
    def odds_bog(self):
        return self._get_webelement_text(selector=self._odds_bog, context=self._we, timeout=11)

    def has_acca_tooltip(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._acca_tooltip, timeout=0) is not None,
            name=f'acca tooltip status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def acca_tooltip_text(self):
        return TextBase(selector=self._acca_tooltip, context=self._we)

    @property
    def partial_cash_out_history(self):
        return PartialCashOutHistory(selector=self._partial_cash_out_history, context=self._we)

    @property
    def moneyback_icon(self):
        return self._find_element_by_selector(selector=self._moneyback_icon, context=self._we)

    @property
    def odds(self):
        return ComponentBase(selector=self._odds, context=self._we)

    @property
    def potential_returns(self):
        return ComponentBase(selector=self._potential_returns, context=self._we)

    @property
    def potential_returns_label(self):
        return ComponentBase(selector=self._potential_returns_label, context=self._we)

    @property
    def potential_returns_value(self):
        return ComponentBase(selector=self._potential_returns_value, context=self._we)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        section = self._find_element_by_selector(
            selector="xpath=.//*[contains(@class,'myBetsAccordion-lads')] | .//*[contains(@class,'myBetsAccordion')]/*[@data-crlat='accordion']",
            context=self._we)
        result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    def has_free_bet_icon(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bet_icon, timeout=timeout, context=self._we),
            name=f'Free Bet icon shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_free_bet_value(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bet_value, timeout=timeout, context=self._we),
            name=f'Free Bet value shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def chevron_arrow(self):
        return ButtonBase(selector=self._chevron_arrow, context=self._we)

    @property
    def you_cashed_out_message(self):
        return TextBase(selector=self._you_cashed_out_message, context=self._we)

    def has_max_payout_msg(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._max_payout_msg, timeout=0) is not None,
            name=f'max payout info to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_max_payout_link(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._max_payout_link, timeout=0) is not None,
            name=f'max payout link to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_stake(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._stake, timeout=timeout, context=self._we),
            name=f'Stake shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_potential_returns(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._est_returns, timeout=timeout, context=self._we),
            name=f'Stake shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    def has_bet_details(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bet_details, timeout=timeout, context=self._we),
            name=f'Bet Details section shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def bet_details(self):
        return BetDetails(selector=self._bet_details, context=self._we)


class PartialCashOutHistoryHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="title"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=1)


class PartialCashOutHistoryTableItem(ComponentBase):
    _stake_used = 'xpath=.//*[@data-crlat="stakeUsed"]'
    _cash_out_amount = 'xpath=.//*[@data-crlat="cashoutValue"]'
    _data_time = 'xpath=.//*[@data-crlat="cashoutDate"]'

    @property
    def stake_used(self):
        return AmountField(selector=self._stake_used, context=self._we)

    @property
    def cash_out_amount(self):
        return AmountField(selector=self._cash_out_amount, context=self._we)

    @property
    def data_time(self):
        return TextBase(selector=self._data_time, context=self._we)

    @property
    def name(self):
        return 'Cashed Out: %s at %s' % (self.cash_out_amount._text, self.data_time.name)


class PartialCashOutHistoryTable(ComponentBase):
    _stake_used_label = 'xpath=.//*[@data-crlat="labelStakeUsed"]'
    _cash_out_amount_label = 'xpath=.//*[@data-crlat="labelCashOutAmount"]'
    _data_time_label = 'xpath=.//*[@data-crlat="labelDataTime"]'
    _item = 'xpath=.//*[@data-crlat="cashoutType"]'
    _list_item_type = PartialCashOutHistoryTableItem

    @property
    def stake_used_label(self):
        return TextBase(selector=self._stake_used_label, context=self._we)

    @property
    def data_time_label(self):
        return TextBase(selector=self._data_time_label, context=self._we)

    @property
    def cash_out_amount_label(self):
        return TextBase(selector=self._cash_out_amount_label, context=self._we)


class PartialCashOutHistoryContent(ComponentBase):
    _remaining_stake = 'xpath=.//*[@data-crlat="remainingStake"]'
    _total_cash_out = 'xpath=.//*[@data-crlat="totalCashOut"]'
    _total_cash_out_stake = 'xpath=.//*[@data-crlat="totalCashOutStake"]'
    _table = 'xpath=.//*[@data-crlat="tablePanel"]'

    @property
    def table(self):
        return PartialCashOutHistoryTable(selector=self._table, context=self._we)


class PartialCashOutHistory(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="panelHeader"]'
    _content = 'xpath=.//*[@data-crlat="panelBody"]'

    @property
    def header(self):
        return PartialCashOutHistoryHeader(selector=self._header, context=self._we)

    @property
    def content(self):
        return PartialCashOutHistoryContent(selector=self._content, context=self._we)

    def has_content(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._content,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Content shown status to be {expected_result}')


class CashOutHeader(ComponentBase):
    _what_is_cashout = 'xpath=.//*[@data-crlat="cashout.whatIsCashout"]'

    @property
    def what_is_cashout(self):
        return ButtonBase(selector=self._what_is_cashout, context=self._we)


class CashoutEventsList(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="cashout.betItems"]'
    _list_item_type = Bet
    _no_bets_text = 'xpath=.//*[@data-crlat="textMsg"]'
    _header = 'xpath=.//*[@data-crlat="cashout.header"]'
    _start_betting_button = 'xpath=.//*[@data-crlat="startBetting"]'
    _context_timeout = 5

    def _wait_active(self, timeout=_context_timeout):
        self._we = self._find_myself(timeout=timeout)
        try:
            self._find_element_by_selector(selector=self._item,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=2)
        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)

    def wait_till_bet_disappear(self, outcome_name, timeout=3):
        def check_refreshed(we):
            try:
                we.get_attribute('data')
            except StaleElementReferenceException:
                return True
            except NoSuchElementException:
                return True
            return False

        wait_for_result(lambda: check_refreshed(self._we), timeout=3,
                        name=f'{self.__class__.__name__} refreshed')
        self._find_myself(timeout=3)
        return wait_for_result(lambda: outcome_name not in self.items_as_ordered_dict,
                               timeout=timeout,
                               name='Wait for bet disappear',
                               bypass_exceptions=(
                               NoSuchElementException, StaleElementReferenceException, VoltronException))

    @property
    def header(self):
        return CashOutHeader(selector=self._header, context=self._we)

    @property
    def no_bets_text(self):
        return self._get_webelement_text(selector=self._no_bets_text, timeout=0.5)

    @property
    def start_betting_button(self):
        return ButtonBase(selector=self._start_betting_button, context=self._we)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            '*** Found %s %s items' % (len(items_we), self.__class__.__name__ + ' - ' + self._list_item_type.__name__))
        items = OrderedDict()
        for item_we in items_we:
            item_type = self._list_item_type(web_element=item_we)
            item_name = item_type.name
            item_name_in_dict = item_name if item_name not in items else '%s %s' % (items_we.index(item_we), item_name)
            items.update({item_name_in_dict: item_type})
        return items

    def verify_cashout_bet_layout_elements(self, number_of_events):
        bets = self.items_as_ordered_dict
        if not bets:
            raise VoltronException(message='No bets found on Cashout page')
        for bet_name, bet in list(bets.items())[:number_of_events]:
            bet.scroll_to()
            bet_type = bet.bet_type
            if not bet_type:
                raise VoltronException(message='Bet: "%s" type is not displayed' % bet_name)
            if not bet.stake.label:
                raise VoltronException(message='Bet: "%s" stake label is not displayed' % bet_name)
            if not bet.stake.value:
                raise VoltronException(message='Bet: "%s" stake value is not displayed' % bet_name)
            if not bet.est_returns.label:
                raise VoltronException(message='Bet: "%s" est returns label is not displayed' % bet_name)
            if not bet.est_returns.value:
                raise VoltronException(message='Bet: "%s" est returns value is not displayed' % bet_name)
            bet_legs = bet.items_as_ordered_dict
            if not bet_legs:
                raise VoltronException(message='No one bet leg was found in section: "%s"' % bet_name)
            for bet_leg_name, bet_leg in bet_legs.items():
                if not bet_leg.outcome_name:
                    raise VoltronException(message='Bet: "%s" outcome name is not displayed' % bet_leg_name)
                if not bet_leg.market_name:
                    raise VoltronException(message='Bet: "%s" market name is not displayed' % bet_leg_name)
                if not bet_leg.event_name:
                    raise VoltronException(message='Bet: "%s" event name is not displayed' % bet_leg_name)
                if not bet_leg.odds_value:
                    raise VoltronException(message='Bet: "%s" odd value is not displayed' % bet_leg_name)
            if not bet.buttons_panel.full_cashout_button.is_displayed():
                raise VoltronException(message='Bet: "%s" full cashout button is not displayed' % bet_name)

    def get_bet(self, event_names: (str, list) = None, bet_type: str = 'DOUBLE', raise_exceptions: bool = True,
                timeout: (float, int) = 20, **kwargs):
        """
        Method used to get bet on cashout page. Method will return first bet if event_names=None.
        Mostly used for Multiples as we don't know ordering of BetLegs
        :param raise_exceptions: True/False. False for cases when it's needed to check bet absence
        :param event_names: list of event names (or string with only one event name)
        :param bet_type: type of bet. SINGLE, DOUBLE, TRIPLE, etc.
        :param kwargs: number_of_bets: num, if specified, only n webelements will be the scope of search, if not specified - scope will be all
        :param timeout: seconds before we give up in waiting for bet list to load
        :return: tuple: bet name and bet webelement (None if bet is not found and raise_exceptions=False)
        """
        cashout_bet_details = []
        number_of_bets = kwargs.get('number_of_bets')
        if self.no_bets_text == '' or self.no_bets_text.__contains__('gambling history over longer periods'):
            bets = wait_for_result(
                lambda: self.get_items(number=number_of_bets) if number_of_bets else self.items_as_ordered_dict,
                name='Bets to be loaded',
                bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                timeout=timeout)
            if not bets and raise_exceptions:
                raise VoltronException(message=f'{number_of_bets} bets not found on "{get_device().get_current_url()}"')
            self._logger.info(f'*** Found bets {", ".join(bets.keys())}')
        else:
            if raise_exceptions:
                raise VoltronException(message=f'No bets found on "{get_device().get_current_url()}"')
            else:
                bets = {}
                self._logger.info(f'*** No bets found on "{get_device().get_current_url()}"')
        if event_names:
            if isinstance(event_names, str):
                event_names = [event_names]
            cashout_bet_details = event_names
        bet = next(((bet_name, bet) for (bet_name, bet) in bets.items() if
                    all(bet_detail in re.sub(r' (H|F)T$', '', bet_name)
                        for bet_detail in cashout_bet_details) and bet_type == bet.bet_type),
                   ('', None))
        if not all(bet) and raise_exceptions:
            raise VoltronException(f'Cannot find bet with type "{bet_type}" and events "{event_names}" '
                                   f'among bets: "{", ".join(bets.keys())}"')
        return bet

    def has_start_betting_button(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._start_betting_button, timeout=0) is not None,
            name=f'"Start Betting" button shown status to be "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)


class TermsPill(TextBase):
    _info_icon = 'xpath=.//*[@class="info-icon"]/*'

    def has_info_icon(self, icon='#info-icon'):
        info_icon = wait_for_result(lambda: self._find_element_by_selector(selector=self._info_icon, context=self._we),
                                    name=f'Waiting for info icon displaying',
                                    bypass_exceptions=(NoSuchElementException, StaleElementReferenceException,
                                                       VoltronException))

        return False if not info_icon else info_icon.get_attribute('xlink:href') == icon


class TermsAndConditions(ComponentBase):
    _item = 'xpath=.//*[@class="container-content terms-links-container"]/*'
    _list_item_type = TermsPill
    _in_play_disclaimer = 'xpath=.//*[@class="info-container"]'

    @property
    def has_in_play_disclaimer(self):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._in_play_disclaimer,
                                                                      context=self._we) is not None,
                               name='searching for in play disclaimer')

    @property
    def in_play_disclaimer(self):
        return TextBase(selector=self._in_play_disclaimer, context=self._we)

    @property
    def terms(self):
        return self.items_as_ordered_dict


class CashoutTabContent(TabContent):
    _accordions_list_type = CashoutEventsList
    _login_button = 'xpath=.//*[@data-crlat="signInButton"]'
    _please_login_text = 'xpath=.//*[@data-crlat="textMsg"]'
    _no_selections = 'xpath=.//*[@data-crlat="noSelectionsMsg" or @data-crlat="textMsg"]'
    _context_timeout = 2
    _terms_and_conditions_container = 'xpath=.//*[@class="terms-and-conditions-container"]'
    _terms_and_conditions_container_type = TermsAndConditions
    _profit_or_loss_link = 'xpath=.//*[@data-crlat="profitLossLink"]'
    _bet_filter = 'xpath=.//*[@data-crlat="bet-filter-section"]'

    @property
    def bet_filter(self):
        return ComponentBase(selector=self._bet_filter, context=self._we)

    def has_profit_or_loss_link(self, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._profit_or_loss_link,
                                                                      context=self._we) is not None,
                               name='searching for in play disclaimer',
                               expected_result=expected_result)

    @property
    def profit_or_loss_link(self):
        return ButtonBase(selector=self._profit_or_loss_link, context=self._we)

    def has_terms_and_conditions(self, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._terms_and_conditions_container,
                                                                      context=self._we) is not None,
                               name='searching for terms and conditions container',
                               expected_result=expected_result)

    @property
    def terms_and_conditions(self):
        return self._terms_and_conditions_container_type(selector=self._terms_and_conditions_container,
                                                         context=self._we)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we)

    def has_login_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._login_button,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Login button status to be {expected_result}')

    @property
    def please_login_text(self):
        return self._get_webelement_text(selector=self._please_login_text, timeout=2)

    @property
    def no_selections_message(self):
        return self._get_webelement_text(selector=self._no_selections, timeout=2)


class Cashout(SportRacingPageBase):
    _url_pattern = r'^http[s]?:\/\/.+\/(cashout|open-bets)'
    _tab_content_type = CashoutTabContent
    _context_timeout = 2
    _tabs_menu = 'xpath=.//*[contains(@data-crlat, "panel.tabs") and not(contains(@class, "ng-hide"))]'
    _tabs_menu_type = TabsMenu
    _fade_out_overlay = True


class CashoutDesktop(Accordion, Cashout):
    _url_pattern = r'^http[s]?:\/\/.+\/'
    _tab_content = 'xpath=.//*[@data-crlat="bsTabsContainer"]'
    _context_timeout = 2


class BetWithReceipt(Bet):
    # _bet_receipt_info = 'xpath=.//*[@data-crlat="betReceiptInfo"]'
    _bet_receipt_info = 'xpath=.//*[contains(@class,"betDetailsAccordion-lads")] | .//*[contains(@class,"betDetailsAccordion-coral")]/*[@data-crlat="accordion"]'

    @property
    def bet_receipt_info(self):
        if not self.bet_details.is_expanded():
            self.bet_details.chevron_arrow.click()
            wait_for_result(lambda: self.bet_details.is_expanded is True,
                            name='Bet Details Expanded',
                            expected_result=True,
                            timeout=10)
        return BetDetails(selector=self._bet_receipt_info, context=self._we)
        # return BetReceiptInfo(selector=self._bet_receipt_info, context=self._we)
