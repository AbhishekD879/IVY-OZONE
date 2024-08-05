import re
from selenium.common.exceptions import WebDriverException
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase, SpinnerButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem, TabsMenu
from voltron.pages.shared.contents.bet_filter.bet_filter_page import BetFilterPage, Filter
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class SubHeader(BetFilterPage):
    _title = 'xpath=.//*[@data-crlat="headerText"]'
    _refresh_icon = 'xpath=.//*[@data-crlat="refreshIcon"]'
    _refresh_button = 'xpath=.//*[@data-crlat="reset"]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=0.3)

    def has_refresh_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._refresh_icon,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Refresh Icon status to be "{expected_result}"')

    @property
    def refresh_button(self):
        return ButtonBase(selector=self._refresh_button, context=self._we)


class BetFilterMenuItem(TabsMenuItem):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)

    def click(self):
        self.scroll_to_we()
        try:
            self._we.click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')


class InfoAccordionDetails(ComponentBase):
    _info_icon = 'xpath=.//*[@data-crlat="infoIcon"]'
    _info_text = 'xpath=.//*[@data-crlat="your-teams-text" or @data-crlat="opposition-text"]'
    _info_text_details = 'xpath=.//*[contains(@class, "accordion__accordion--show")]'
    _show_more = 'xpath=.//*[@class="cb-info-accordion__showmore showMore"]'
    _show_less = 'xpath=.//*[@class="cb-info-accordion__showmore showLess"]'

    @property
    def info_icon(self):
        return ButtonBase(selector=self._info_icon, context=self._we)

    @property
    def show_more(self):
        return self._find_element_by_selector(selector=self._show_more, timeout=1)

    @property
    def show_less(self):
        return self._find_element_by_selector(selector=self._show_less, timeout=1)

    @property
    def info_text(self):
        return self._get_webelement_text(selector=self._info_text)

    @property
    def info_text_details(self):
        return self._get_webelement_text(selector=self._info_text_details, timeout=4)


class BetFilterTabsMenu(TabsMenu):
    _item = 'xpath=.//*[@data-crlat="tab"]'
    _list_item_type = BetFilterMenuItem


class FootballSectionItem(ButtonBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5,
                    name='Football Bet Filter item to become selected') -> bool:
        result = wait_for_result(lambda: 'selected' in self.get_attribute('class'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result


class FootballSections(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="sectionTitle"]'
    _item = 'xpath=.//*[contains(@data-crlat, "FilterButtons")]'
    _list_item_type = FootballSectionItem

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2)


class FootballTabContent(ComponentBase):
    _item = 'xpath=.//*[@class="cb-filters__filter"]'
    _list_item_type = FootballSections


class FootballBetFilterPage(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/bet-filter'
    _sub_header = 'xpath=.//*[@class="cb-header"]'
    _tabs_menu = 'xpath=.//*[@data-crlat="tab.tpTabs"]'
    _info_accordion = 'xpath=.//*[@class="cb-info-accordion"]'
    _tab_content = 'xpath=.//*[@data-crlat="tabContent"]'
    _tab_content_type = FootballTabContent
    _save_filters_button = 'xpath=.//*[@data-crlat="saveSelection"]'
    _find_bets_button = 'xpath=.//*[@data-crlat="findBets"]'

    _save_filters_dialog = 'css=div.cb-modal-dialog'
    _list_item_type = Filter

    @property
    def sub_header(self):
        return SubHeader(selector=self._sub_header)

    @property
    def tab_menu(self):
        return BetFilterTabsMenu(selector=self._tabs_menu, context=self._we)

    @property
    def info_accordion(self):
        return InfoAccordionDetails(selector=self._info_accordion, context=self._we)

    @property
    def save_filters_button(self):
        return ButtonBase(selector=self._save_filters_button, context=self._we)

    @property
    def find_bets_button(self):
        self.scroll_to_bottom()
        return SpinnerButtonBase(selector=self._find_bets_button, context=self._we, timeout=10)

    def read_number_of_bets(self):
        if not self.find_bets_button.has_spinner_icon(expected_result=False, timeout=10):
            number_of_bets = self.find_bets_button.name
            return 0 if number_of_bets == '(0)' else int(re.search(r'\d+', number_of_bets).group())
        else:
            raise VoltronException('Spinner has not disappeared from Find Bets button')


class FootballMatch(ComponentBase):
    _checkbox = 'xpath=.//*[contains(@class, "cb-results-item__check-box")]'
    _title = 'xpath=.//*[@class="cb-results-item__title"]'
    _event = 'xpath=.//*[@class="cb-results-item__event"]'
    _match_date = 'xpath=.//*[@class="cb-results-item__date"]'
    _odds = 'xpath=.//*[@class="cb-results-item__odds"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def checkbox(self):
        return CheckBoxBase(selector=self._checkbox, context=self._we)

    @property
    def title(self):
        return TextBase(selector=self._title, context=self._we)

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event, context=self._we)

    @property
    def event(self):
        return TextBase(selector=self._event, context=self._we)

    @property
    def match_date(self):
        return TextBase(selector=self._match_date, context=self._we)

    @property
    def odds(self):
        return TextBase(selector=self._odds, context=self._we)


class FootballBetFilterResultsPage(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/bet-filter/results/all'
    _number_of_results = 'xpath=.//*[contains(text(),"Results")] | //a[@data-crlat="tab" and contains(text(),"(")] | //*[@class="results-block"]/p'
    _item = 'xpath=.//*[@class="cb-results-item"]'
    _list_item_type = FootballMatch
    _accumulator_bet_type = 'xpath=.//*[contains(@class, "cb-accumulator__text")][1]'
    _accumulator_quantity = 'xpath=.//*[contains(@class, "cb-accumulator__text")][2]'
    _accumulator_bet_pays = 'xpath=.//*[contains(@class, "cb-accumulator__text")][3]'
    _accumulator_estimated_returns = 'xpath=.//*[contains(@class, "cb-accumulator__text")][4]'
    _accumulator_warning = 'xpath=.//*[contains(@class, "cb-accumulator__warning")]'
    _accumulator_info = 'xpath=.//*[contains(@class, "cb-accumulator__info")]'
    _button = 'xpath=.//*[contains(@class, "cb-button")] | .//*[contains(@class,"button btn btn-primary")]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _coupon_results = 'xpath=.//*[@class="results-block"]/p | .//*[contains(text(),"Results")]'
    _coupon_name = 'xpath=.//*[@data-crlat="tab"]'

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=10)

    @property
    def number_of_results(self):
        number_of_results = self._get_webelement_text(selector=self._number_of_results, context=self._we)
        return int(re.search(r'\d+', number_of_results).group())

    @property
    def accumulator_bet_type(self):
        return self._get_webelement_text(selector=self._accumulator_bet_type, context=self._we)

    @property
    def accumulator_quantity(self):
        return self._get_webelement_text(selector=self._accumulator_quantity, context=self._we)

    @property
    def accumulator_bet_pays(self):
        return TextBase(selector=self._accumulator_bet_pays, context=self._we)

    @property
    def accumulator_estimated_returns(self):
        return self._get_webelement_text(selector=self._accumulator_estimated_returns, context=self._we)

    @property
    def accumulator_warning(self):
        return self._get_webelement_text(selector=self._accumulator_warning, context=self._we)

    @property
    def accumulator_info(self):
        return self._get_webelement_text(selector=self._accumulator_info, context=self._we)

    @property
    def get_odds(self):
        odds = []
        for item in self.items:
            odds.append(item.odds.name)
        return odds

    @property
    def button(self):
        return ButtonBase(selector=self._button, context=self._we, timeout=3)

    @property
    def coupon_results(self):
        coupon_results = self._get_webelement_text(selector=self._coupon_results, context=self._we)
        return int(re.search(r'\d+', coupon_results).group())

    @property
    def coupon_name(self):
        return self._get_webelement_text(selector=self._coupon_name, context=self._we)
