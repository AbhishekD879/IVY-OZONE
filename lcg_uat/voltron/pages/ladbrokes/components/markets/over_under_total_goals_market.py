from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared.components.markets.over_under_home_away_total_goals_market import OverUnderHomeAwayTeamTotalGoalsMarket
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.markets.over_under_total_goals_market import OverUnderTotalGoalsMarket


class LadbrokesOverUnderTotalGoalsMarket(OverUnderTotalGoalsMarket):
    _inner_market = 'xpath=.//*[@data-crlat="marketComponent"]/accordion'

    def is_expanded(self, timeout=5, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        result = wait_for_result(lambda: 'is-expanded' in self._find_element_by_selector(selector=self._inner_market, timeout=0).get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand/collapse, current class value is '
                                      f'"{self._find_element_by_selector(selector=self._inner_market, timeout=0).get_attribute("class")}"',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result


class LadbrokesOverUnderHomeAwayTeamTotalGoalsMarket(OverUnderHomeAwayTeamTotalGoalsMarket):
    _inner_market = 'xpath=.//*[@data-crlat="marketComponent"]/accordion'

    def is_expanded(self, timeout=5, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        result = wait_for_result(lambda: 'is-expanded' in self._find_element_by_selector(selector=self._inner_market, timeout=0).get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand/collapse, current class value is '
                                      f'"{self._find_element_by_selector(selector=self._inner_market, timeout=0).get_attribute("class")}"',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result
