from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.contents.edp.promotion_details import PromotionDetails
from voltron.pages.shared.contents.edp.promotion_details import PromotionDetailsContent
from voltron.pages.shared.contents.edp.promotion_details import PromotionDetailsTabContent
from voltron.pages.shared.contents.edp.promotion_details import TermsAndConditions
from voltron.utils.waiters import wait_for_result


class CoralPromotionDetailsContent(PromotionDetailsContent):

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        section = self._find_element_by_selector(selector='xpath=.//*[@data-crlat="accordion"]', context=self._we)
        result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result


class CoralTermsAndConditions(TermsAndConditions):

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        section = self._find_element_by_selector(selector='xpath=.//*[@data-crlat="accordion"]', context=self._we)
        result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result


class CoralPromotionDetailsTabContent(PromotionDetailsTabContent):
    _promotion_content_type = CoralPromotionDetailsContent
    _terms_and_conditions_type = CoralTermsAndConditions


class CoralPromotionDetails(PromotionDetails):
    _tab_content_type = CoralPromotionDetailsTabContent
