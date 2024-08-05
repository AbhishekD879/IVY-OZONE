import re

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import SpinnerButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class Filter(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="filterName"]'

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class FindBetsSpinner(SpinnerButtonBase):
    _local_spinner = 'xpath=.//*[contains(@class, "cb-button--loading")]'


class BetFilterPage(BaseContent):
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _page_title = 'xpath=.//*[@data-crlat="topBarTitle"]'
    _refresh_icon = 'xpath=.//*[@data-crlat="refreshIcon"]'
    _reset_link = 'xpath=.//*[@data-crlat="reset"]'

    _title = 'xpath=.//*[contains(@data-crlat, "title") and @data-crlat != "titleText"]'
    _description = 'xpath=.//*[contains(@data-crlat, "text")]'

    _item = 'xpath=.//*[contains(@data-crlat, "FilterButtons")]'  # Filters

    _find_bets_button = 'xpath=.//*[@data-crlat="findBets"]'
    _save_selection_button = 'xpath=.//*[@data-crlat="saveSelection"]'
    _found_result_text = 'xpath=.//*[@data-crlat="foundResultText"]'
    _filter_gruops = 'xpath=.//*[contains(@class, "bf-form-title")]'

    def _wait_active(self, timeout=5):
        try:
            self._find_element_by_selector(selector=self._item, context=self._context,
                                           bypass_exceptions=(NoSuchElementException, ), timeout=timeout)
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=timeout)

    @property
    def page_title(self):
        return TextBase(selector=self._page_title)

    @property
    def reset_link(self):
        return LinkBase(selector=self._reset_link, context=self._we, timeout=2)

    @property
    def title(self):
        return TextBase(selector=self._title)

    @property
    def description(self):
        return TextBase(selector=self._description)

    @property
    def find_bets_button(self):
        return FindBetsSpinner(selector=self._find_bets_button, context=self._we)

    @property
    def save_selection_button(self):
        return ButtonBase(selector=self._save_selection_button, context=self._we)

    def is_filter_selected(self, filter, expected_result=True, timeout=3):
        filters = self.items_as_ordered_dict
        filter_element = filters.get(filter)
        if not filter_element:
            raise VoltronException(f'No filter "{filter}" found among filters "{filters}"')
        result = wait_for_result(lambda: 'selected' in filter_element.get_attribute('class') or
                                         'active' in filter_element.get_attribute('class'),
                                 name='Wait for selected filter',
                                 expected_result=expected_result,
                                 timeout=timeout)
        return result

    def read_number_of_bets(self):
        number_of_bets = self._get_webelement_text(selector=self._find_bets_button, timeout=1)
        search = re.search(r'\d+', number_of_bets)
        if not search:
            if vec.bet_finder.NO_SELECTION in number_of_bets:
                return 0
            else:
                raise VoltronException(f'Cannot get number of bets from string "{number_of_bets}"')
        return int(search.group())

    @property
    def filter_groups_names(self):
        return self._find_elements_by_selector(selector=self._filter_gruops, context=self._we)
