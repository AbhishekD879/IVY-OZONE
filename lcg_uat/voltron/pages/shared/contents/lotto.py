# -*- coding: utf-8 -*-
from collections import OrderedDict
from multidict import MultiDict
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.menu_carousel import MenuCarousel
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.contents.base_contents.base_sport_race_structure import SportRacingPageBase
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import mouse_event_click
from voltron.utils.waiters import wait_for_result


class InfoPanel(ComponentBase):
    _lottery_name = 'xpath=.//*[@data-crlat="currentLotto.name"]'
    _info_btn = 'xpath=.//*[@data-crlat="infoButton"]'
    _bet_until_time = 'xpath=.//*[@data-crlat="betUntillTime"]'

    @property
    def lottery_name(self):
        return self._get_webelement_text(selector=self._lottery_name)

    @property
    def info_btn(self):
        return self._find_element_by_selector(selector=self._info_btn)

    @property
    def bet_until_time(self):
        return self._get_webelement_text(selector=self._bet_until_time)

    @property
    def info_line(self):
        line = ' '.join(self.get_attribute('innerText').replace('\n', ' ').replace('&nbsp;', ' ').split())
        return line

    @property
    def info_line_as_list(self):
        lines = self.get_attribute('innerText').split('\n')
        return [line for line in lines if line != '']


class NumberSelector(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="typeButton"]'
    _list_item_type = ButtonBase

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({f'{items_we.index(item_we)} {list_item.name}': list_item})
        return items_ordered_dict


class LuckyButtons(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="luckyButton"]'
    _list_item_type = ButtonBase


class LottoOptions(EventGroup):
    pass


class DrawCheckBox(CheckBoxBase):
    _label = 'xpath=.//label[contains(@class, "check-title")]//strong'
    _draw_check_box = 'xpath=.//div[contains(@class,"check-styled")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._label)

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        if not isinstance(value, bool):
            raise VoltronException('CheckBox value should be BOOL type (True/False). Got: "%s"' % value)

        if self.value != value:
            if self.is_enabled():
                self._logger.debug(
                    f'*** User has set "{value}" on CheckBox. Call of "{self.__class__.__name__}"'
                )
                we = self._find_element_by_selector(selector=self._input)
                self.perform_click(we=we)
            else:
                raise VoltronException('CheckBox is disabled so can\'t be clicked')

    @property
    def draw_check_box(self):
        return ComponentBase(selector=self._draw_check_box, context=self._we, timeout=1)

    def perform_click(self, we=None):
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        we = we if we else self._we
        get_driver().implicitly_wait(0.7)
        mouse_event_click(we)
        get_driver().implicitly_wait(0)


class DrawCheckBoxes(ComponentBase):
    _item = 'xpath=.//div[contains(@class, "col-xs-6")]'
    _list_item_type = DrawCheckBox

    @property
    def items_as_ordered_dict(self) -> MultiDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = MultiDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.add(list_item.name, list_item)
        return items_ordered_dict


class LineSummary(ComponentBase):
    _header_line = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _current_lotto_name = 'xpath=.//*[@data-crlat="currentLottoname"]'
    _next_draw = 'xpath=.//*[@data-crlat="infoButton"]/following-sibling::span'
    _info_button = 'xpath=.//*[@data-crlat="infoButton"]'
    _line_section = 'xpath=.//*[@class="top-section"] | .//*[@data-crlat="linesummary"]/*[position() = 1]'
    _choose_your_draws_section = 'xpath=.//div[contains(@class, "draws-header")]/..'
    _how_many_weeks_section = 'xpath=.//div[contains(@class, "howManyWeeks")]'
    _add_to_betslip = 'xpath=.//div[contains(@class, "addToBetslip")]/*[@data-crlat="buttonGroup"]'

    @property
    def header_line(self):
        return self._get_webelement_text(selector=self._header_line)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)

    @property
    def current_lotto_name(self):
        return self._get_webelement_text(selector=self._current_lotto_name)

    @property
    def next_draw(self):
        items_we = self._find_elements_by_selector(selector=self._next_draw, context=self._we, timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_array = ''
        for item_we in items_we:
            if item_we.is_displayed():
                item_component = self._get_webelement_text(we=item_we)
                items_array = items_array + ' ' + item_component
        return items_array

    @property
    def info_button(self):
        return ButtonBase(selector=self._info_button, context=self._we)

    @property
    def line_section(self):
        return LineSection(selector=self._line_section, context=self._we)

    @property
    def choose_your_draws_section(self):
        return DrawsSelections(selector=self._choose_your_draws_section, context=self._we)

    @property
    def how_many_weeks_section(self):
        return WeeksSelection(selector=self._how_many_weeks_section, context=self._we)

    @property
    def add_to_betslip(self):
        return ButtonBase(selector=self._add_to_betslip, context=self._we)


class WeeksSelection(ComponentBase):
    _header_title = 'xpath=.//*[@class="group-btn"]'
    _week_selection = 'xpath=.//*[@ata-crlat="luckyButton"] | .//*[@data-crlat="luckyButton"]'

    @property
    def header_title(self):
        return self._get_webelement_text(selector=self._header_title)



    @property
    def week_selections_items(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._week_selection, context=self._we,
                                                   timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = ButtonBase(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class DrawsSelectionsItem(ComponentBase):
    _draw_date = 'xpath=.//*[@class="draw-date"]'
    _name = 'xpath=.//*[@class="draw-date"]'
    _item = 'xpath=.//*[@data-crlat="luckyButton"]'
    _list_item_type = ButtonBase

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)
    @property
    def draw_date(self):
        return self._get_webelement_text(selector=self._draw_date)


class DrawsSelections(ComponentBase):
    _header_title = 'xpath=.//*[contains(@class, "draws-header")]//span'
    _select_all = 'xpath=.//*[contains(@class, "draws-header")]//a[contains(@class, "edit-link")]'
    _item = 'xpath=.//*[@data-crlat="selectDrawRow"]'
    _list_item_type = DrawsSelectionsItem

    @property
    def header_title(self):
        return self._get_webelement_text(selector=self._header_title)

    @property
    def select_all(self):
        return ButtonBase(selector=self._select_all, context=self._we)


class EachLine(ComponentBase):
    _line_header = 'xpath=.//div[contains(@class, "line-header")]//strong'
    _edit_line = 'xpath=.//a[contains(@class, "edit-link")]'
    _delete_line = 'xpath=.//div[contains(@class, "bs-stake-delete-button")]'
    _selected_numbers = 'xpath=.//div[contains(@class,"numbercol")]'
    _bonus_ball_check_box = 'xpath=.//input[@data-crlat="chkBox"]'
    _bonus_ball_text = 'xpath=.//div[contains(@class, "col-xs-6")]/label[@data-crlat="label"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._line_header)

    @property
    def edit_line(self):
        return ButtonBase(selector=self._edit_line, context=self._we)

    @property
    def delete_line(self):
        return ButtonBase(selector=self._delete_line, context=self._we)

    @property
    def selected_numbers(self):
        items_we = self._find_elements_by_selector(selector=self._selected_numbers, context=self._we,
                                                   timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_array = []
        for item_we in items_we:
            if item_we.is_displayed():
                item_component = self._get_webelement_text(we=item_we)
                items_array.append(item_component)
        return items_array

    @property
    def bonus_ball_check_box(self):
        return CheckBoxBase(selector=self._bonus_ball_check_box, context=self._we)

    @property
    def bonus_ball_name(self):
        return self._get_webelement_text(selector=self._bonus_ball_text)


class LineSection(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"btm-margin")]'
    _list_item_type = EachLine
    _create_a_new_line = 'xpath=.//*[@data-crlat="buttonGroup"]'

    @property
    def create_a_new_line(self):
        return ButtonBase(selector=self._create_a_new_line, context=self._we)


class BallsAndReturns(ComponentBase):
    _balls = 'xpath=.//*[contains(@class,"retuns-price")]'
    _winning_amount = 'xpath=.//*[contains(@class,"retuns-price")]/../*[2]'

    @property
    def balls(self):
        return int(self._get_webelement_text(selector=self._balls, context=self._we).split()[0])

    @property
    def winning_amount(self):
        return int(self._get_webelement_text(selector=self._winning_amount, context=self._we))


class PotentialReturns(ComponentBase):
    _item = 'xpath=.//*[@class="lotto-odds center-text"] | .//*[@class="lotto-odds center-text ng-star-inserted"]'
    _list_item_type = BallsAndReturns

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.balls: list_item.winning_amount})
        return items_ordered_dict


class LottoTabContent(ComponentBase):
    _info_panel = 'xpath=.//*[@data-crlat="containerHeader"][.//*[contains(@data-crlat,"currentLotto")]]'
    _info_panel_type = InfoPanel
    _number_selectors = 'xpath=.//*[@data-crlat="numberSelector"]'
    _number_selectors_type = NumberSelector
    _choose_numbers = 'xpath=.//*[@data-crlat="luckyButton"]'
    _lucky_buttons = 'xpath=.//*[@data-crlat="lotto.luckyDip"]'
    _lucky_buttons_type = LuckyButtons
    # _odd = 'xpath=.//*[@data-crlat="odd"]'
    # _bet_amount = 'xpath=.//*[@data-crlat="betAmount"]'
    # _bet_input = 'xpath=.//*[@data-crlat="betInput"]'
    # _options = 'xpath=.//*[contains(@data-crlat,"lotto.options")]'
    # _options_type = LottoOptions
    # _place_bet_button = 'xpath=.//*[@data-crlat="placeBetButton"]'
    # _confirm_button = 'xpath=.//*[@data-crlat="confirmButton"]'
    # _reset_numbers_button = 'xpath=.//*[@data-crlat="resetNumberButton"]'
    # _include_bonus_ball = 'xpath=.//*[@data-crlat="lotto.bonusBallLabel"]'
    _draw_checkboxes = 'xpath=.//*[@data-crlat="selectDrawRow"]'
    _draw_checkboxes_type = DrawCheckBoxes
    # _currency = 'xpath=.//span[contains(@class, "currency")]'
    # _include_bonus_ball_check = 'xpath=.//*[@data-crlat="checkbox.bonusBall"]'
    # _select_draw = 'xpath=.//p[text()="Select Draw"]'
    _potential_returns = 'xpath=.//*[contains(@class,"p-returns-container")]'
    _potential_returns_type = PotentialReturns

    @property
    def potential_returns(self):
        return PotentialReturns(selector=self._potential_returns, context=self._we)

    @property
    def info_panel(self):
        return self._info_panel_type(selector=self._info_panel, context=self._we)

    @property
    def number_selectors(self):
        return self._number_selectors_type(selector=self._number_selectors, context=self._we)

    @property
    def choose_numbers(self):
        choose_numbers = self._lucky_buttons_type(selector=self._choose_numbers, context=self._we)
        choose_numbers.scroll_to()
        return choose_numbers

    @property
    def lucky_buttons(self):
        lucky_buttons = self._lucky_buttons_type(selector=self._lucky_buttons, context=self._we)
        lucky_buttons.scroll_to()
        return lucky_buttons

    # @property
    # def odd_value(self):
    #     return self._get_webelement_text(selector=self._odd)

    # @property
    # def bet_input(self):
    #     return ComponentBase(selector=self._bet_input, context=self._we)

    # @property
    # def bet_amount(self):
    #     return InputBase(selector=self._bet_amount, context=self._we)

    # @bet_amount.setter
    # def bet_amount(self, value):
    #     if not isinstance(value, str):
    #         value = str(value)
    #     self._find_element_by_selector(selector=self._bet_amount).send_keys(value)

    # @property
    # def options(self):
    #     return self._options_type(selector=self._options, context=self._we)

    # @property
    # def place_bet(self):
    #     return ButtonBase(selector=self._place_bet_button, context=self._we)

    # @property
    # def confirm_bet(self):
    #     return ButtonBase(selector=self._confirm_button, context=self._we)

    # @property
    # def confirm_bet_text(self):
    #     return self._get_webelement_text(selector=self._confirm_button)

    # def has_confirm_bet_button(self, expected_result=True, timeout=1):
    #     return wait_for_result(
    #         lambda: self._find_element_by_selector(selector=self._confirm_button, context=self._we, timeout=0) is not None,
    #         expected_result=expected_result,
    #         timeout=timeout,
    #         name=f'Confirm bet Button status to be "{expected_result}"')

    # @property
    # def reset_numbers(self):
    #     return ButtonBase(selector=self._reset_numbers_button, context=self._we)

    # @property
    # def include_bonus_ball(self):
    #     return ComponentBase(selector=self._include_bonus_ball, context=self._we)

    # def has_include_bonus_ball(self, expected_result=True, timeout=1):
    #     return wait_for_result(
    #         lambda: self._find_element_by_selector(selector=self._include_bonus_ball, context=self._we, timeout=0) is not None,
    #         expected_result=expected_result,
    #         timeout=timeout,
    #         name=f'Include Bonus Ball to be "{expected_result}"')

    @property
    def odds(self):
        return ComponentBase(selector=self._odd, context=self._we)

    @property
    def draw_checkboxes(self):
        return self._draw_checkboxes_type(selector=self._draw_checkboxes, context=self._we)

    # @property
    # def currency(self):
    #     return self._get_webelement_text(selector=self._currency, timeout=1)

    # @property
    # def include_bonus_ball_check(self):
    #     return self._find_element_by_selector(selector=self._include_bonus_ball_check)

    # @property
    # def select_draw(self):
    #     return self._find_element_by_selector(selector=self._select_draw)


class Lotto(SportRacingPageBase):
    _url_pattern = r'^https?:\/\/.+\/lotto'
    _carousel = 'xpath=.//*[@data-uat="mainNav"]'
    _tab_content_type = LottoTabContent

    @property
    def lotto_carousel(self):
        return MenuCarousel(context=self._we, selector=self._carousel, timeout=2)

    @property
    def line_summary(self):
        return LineSummary(selector=self._tab_content)
