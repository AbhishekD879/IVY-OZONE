import re

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class BuildCard(ButtonBase):
    _close_icon = 'xpath=.//*[@data-crlat="closeIcon"]'
    _build_card_button = 'xpath=.//*[@data-crlat="buildRacecardButton"]'
    _build_card_exit_button = 'xpath=.//*[@data-crlat="exitBuilderButton"]'
    _build_card_description = 'xpath=.//*[@data-crlat="buildCardTextBlock"]'
    _clear_all_selections = 'xpath=.//*[@data-crlat="clearAllSelectionsButton"]'
    _build_your_racecard_button = 'xpath=.//*[@data-crlat="buildYourRacecardButton"]'
    _build_card_limit_error = 'xpath=.//*[@data-crlat="buildCardLimitError"]'

    @property
    def build_race_card_button(self):
        return ButtonBase(selector=self._build_card_button, context=self._we)

    @property
    def build_race_card_text_block(self):
        text_block = self._get_webelement_text(selector=self._build_card_description, context=self._we)
        result = re.sub(r"\s+", " ", re.sub('\n', '. ', text_block))
        return result

    @property
    def exit_builder_button(self):
        return ButtonBase(selector=self._build_card_exit_button, context=self._we)

    @property
    def close_icon(self):
        return ButtonBase(selector=self._close_icon, context=self._we)

    @property
    def build_your_race_card_button(self):
        return BuildCardButton(selector=self._build_your_racecard_button, context=self._we)

    @property
    def clear_all_selections_button(self):
        return BuildCardButton(selector=self._clear_all_selections, context=self._we)

    @property
    def clear_all_selections_button_text(self):
        return self._get_webelement_text(selector=self._clear_all_selections, context=self._we)

    @property
    def build_card_limit_message(self):
        return self._get_webelement_text(selector=self._build_card_limit_error, context=self._we)


class BuildCardButton(ButtonBase):

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass

    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" enabled status is: {expected_result}'
        result = wait_for_result(lambda: 'active' in self.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result
