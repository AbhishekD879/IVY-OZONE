from voltron.pages.shared.contents.bet_filter.football_bet_filter import FootballBetFilterPage
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result
from voltron.pages.ladbrokes.components.the_grid import GenerateBetFrame


class SavedFilterRadio(ComponentBase):
    _filter_name = 'xpath=.//*[@data-crlat="filterName"]'
    _remove_filter = 'xpath=.//*[@data-crlat="deleteFilter"]'
    _radio_button = 'xpath=.//*[contains(@class,"cb-radio__btn")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._filter_name)

    @property
    def remove_filter(self):
        return self._find_element_by_selector(selector=self._remove_filter)

    @property
    def radio_button(self):
        return self._find_element_by_selector(selector=self._radio_button)


class SavedFiltersTab(ComponentBase):
    _saved_filter_header = 'xpath=.//*[@data-crlat="saved-filters-text"]//*[@class="header"]'
    _saved_filter_text = 'xpath=.//*[@data-crlat="saved-filters-text"]//p[2]'
    _show_more_link = 'xpath=.//*[contains(@class, "showMore")]'
    _apply = 'xpath=//*[@data-crlat="applyButton"]'
    _item = 'xpath=.//*[@class="cb-radio"]'
    _list_item_type = SavedFilterRadio

    @property
    def saved_filter_header(self):
        return self._find_element_by_selector(selector=self._saved_filter_header)

    @property
    def saved_filter_text(self):
        return self._find_element_by_selector(selector=self._saved_filter_text)

    @property
    def show_more_link(self):
        return self._find_element_by_selector(selector=self._show_more_link)

    @property
    def apply_button(self):
        return ButtonBase(selector=self._apply, context=self._we)


class SaveFilter(ComponentBase):
    _popup_header = 'xpath=.//*[@data-crlat="modalHeader"]'
    _popup_desc = 'xpath=.//*[@class="cb-modal__desc"]'
    _enter_name = 'xpath=.//*[@data-crlat="filterName"]'
    _cancel_button = 'xpath=.//*[@data-crlat="saveButton"]'
    _save_button = 'xpath=.//*[@data-crlat="cancelButton"]'

    @property
    def pop_up_header(self):
        return self._get_webelement_text(selector=self._popup_header)

    @property
    def pop_up_description(self):
        return self._get_webelement_text(selector=self._popup_desc)

    def enter_name(self, value):
        return self._find_element_by_selector(selector=self._enter_name).send_keys(value)

    def get_filter_name(self):
        return self._find_element_by_selector(selector=self._enter_name).get_attribute("value")

    @property
    def save_button(self):
        return ButtonBase(selector=self._save_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)


class LadbrokesFootballBetFilterPage(FootballBetFilterPage):
    _header_line = 'xpath=.//*[@class="header"]'
    _sub_header = 'xpath=.//*[@data-crlat="cbHeader"]'
    _saved_bet_codes_icon = 'xpath=.//*[@class="wallet-icon"]'
    _save_filter_popup = "xpath=.//*[@data-crlat='modalBody']"
    _saved_filter_tab = "xpath=.//*[@id='static']"
    _generate_bet_frame = 'xpath=.//*[@class="cb-accumulator-wrap cb-accumulator-grid "] | .//*[@class="cb-accumulator-wrap cb-accumulator-grid cb-accumalator-center-align"]'
    _footer_sticky = 'xpath=.//*[@id="fixedFooter"]'
    _header_sticky = 'xpath=.//*[@id="fixedHeader"]'

    @property
    def saved_bet_codes_icon(self):
        return self._find_element_by_selector(selector=self._saved_bet_codes_icon, timeout=1)

    @property
    def save_filter_popup(self):
        return SaveFilter(selector=self._save_filter_popup)

    @property
    def has_save_filter_popup(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._save_filter_popup, timeout=0) is not None,
                               name=f'save filter popup displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def saved_filters_tab(self):
        return SavedFiltersTab(selector=self._saved_filter_tab)

    @property
    def generate_bet_frame(self):
        return GenerateBetFrame(selector=self._generate_bet_frame, context=self._we)

    @property
    def is_footer_sticky(self):
        we = self._find_element_by_selector(selector=self._footer_sticky, timeout=0)
        if we.get_attribute('style'):
            sticky = 'fixed' in we.get_attribute('style')
            return sticky
        return False

    @property
    def is_header_sticky(self):
        we = self._find_element_by_selector(selector=self._header_sticky, timeout=0)
        if we.get_attribute('style'):
            sticky = 'position' not in we.get_attribute('style')
            return sticky
        return False
