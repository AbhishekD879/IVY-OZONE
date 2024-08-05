from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.right_column_widgets.mini_games_widget import MiniGamesWidget
from voltron.utils.waiters import wait_for_result


class LadbrokesMiniGamesWidget(MiniGamesWidget):

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        result = wait_for_result(lambda: 'is-expanded' in self.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = bool(result)
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result
