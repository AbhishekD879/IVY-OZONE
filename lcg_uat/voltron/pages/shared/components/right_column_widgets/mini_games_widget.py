from selenium.common.exceptions import StaleElementReferenceException
from collections import OrderedDict
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.right_column_widgets.right_column_item_widget import RightColumnItem
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.games_widget import MiniGameWidget
from voltron.utils.helpers import execute_in_iframe


class MiniGamesWidget(RightColumnItem):
    _verify_spinner = True
    _item = 'xpath=.//*[@class="mat-grid-tile"]'
    _list_item_type = MiniGameWidget
    _iframe = 'xpath=.//iframe[contains(@class, "mini-games-iframe")]'

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        section = self._find_element_by_selector(selector='xpath=.//*[@data-crlat="accordion"]', context=self._we)
        result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = bool(result)
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    def expand(self):
        title_text = self.name
        if self.is_expanded():
            self._logger.warning(f'*** Bypassing accordion expand, since "{title_text}" already expanded')
        else:
            self._logger.debug(f'*** Expanding "{title_text}"')

            self.section_header.click()
            wait_for_result(lambda: self.is_expanded(),
                            name=f'"{self.__class__.__name__}" section to expand',
                            timeout=2)
            self._spinner_wait()

    def _load_complete(self, timeout=None):
        """
        Waits for component to load. Most commonly component is considered to be loaded if splash disappears and url is
        changed (if applicable) or spinner to disappear
        :param timeout:
        :return:
        """
        return self._spinner_wait()

    @execute_in_iframe(_iframe, timeout=3)
    def click_item(self, item_name: str):
        return super().click_item(item_name)

    @execute_in_iframe(_iframe, timeout=3)
    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        return super().items_as_ordered_dict

    @property
    def container(self):
        return ButtonBase(selector=self._iframe, context=self._we)
