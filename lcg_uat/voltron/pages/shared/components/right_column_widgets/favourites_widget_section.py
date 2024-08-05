from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.right_column_widgets.right_column_item_widget import RightColumnItem
from voltron.utils.waiters import wait_for_result


class FavoritesWidgetSection(RightColumnItem, ComponentBase):
    _widget_not_logged_text = 'xpath=.//*[@data-crlat="textMsg"]'
    _widget_logged_text = 'xpath=.//*[@data-crlat="widgetLoggedText"]'
    _widget_buttons = 'xpath=.//*[contains(@data-crlat, "Button")]'
    _login_button = 'xpath=.//*[@data-crlat="signInButton"]'
    _item = 'xpath=.//*[@data-crlat="oddsCard.sportTemplate"]'
    _list_item_type = SportTemplate
    _show_all_button = 'xpath=.//*[text()="Show All"]'
    _show_less_button = 'xpath=.//*[text()="Show Less"]'
    _fixture_header = 'xpath=.//*[@data-crlat="eventOddsHeader"]'
    _fixture_header_type = FixtureHeader
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def widget_text_not_logged(self):
        return self._get_webelement_text(selector=self._widget_not_logged_text, timeout=2)

    @property
    def widget_text_logged(self):
        return self._get_webelement_text(selector=self._widget_logged_text, timeout=2)

    @property
    def widget_buttons(self):
        return self.get_elements_name(element_selector=self._widget_buttons)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we)

    def get_elements_name(self, element_selector):
        elements = self._find_elements_by_selector(selector=element_selector, timeout=0)
        element_names = []
        if len(elements) == 0:
            self._logger.warning('*** There is no one widget button')
        else:
            for element in elements:
                self.scroll_to_we(element)
                element_names.append(self._get_webelement_text(we=element))
        return '\n'.join(element_names)

    @property
    def widget_button(self):
        return ButtonBase(selector=self._widget_buttons, context=self._we)

    @property
    def show_all_button(self):
        return ButtonBase(selector=self._show_all_button, context=self._we, timeout=2)

    @property
    def show_less_button(self):
        return ButtonBase(selector=self._show_less_button, context=self._we, timeout=2)

    def has_fixture_header(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._fixture_header, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Fixture header presence status in {self.__class__.__name__} to be {expected_result}')

    @property
    def fixture_header(self):
        return self._fixture_header_type(selector=self._fixture_header, context=self._we)
