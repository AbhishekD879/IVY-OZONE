from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class Splash(ComponentBase):
    _inner = 'xpath=.//*[contains(@class, "splash-loading-wrapper")]'

    def _re_init_context(self, timeout=0):
        try:
            self._we = self._find_myself(timeout=timeout)
            return self._we
        except VoltronException as e:
            self._logger.debug(f'*** Bypassing exception "{e}"')

    def _wait_active(self, timeout=2):
        result = self._re_init_context()
        if result:
            try:
                return self._find_element_by_selector(selector=self._inner, timeout=0) is not None
            except StaleElementReferenceException:
                self._re_init_context(timeout=1)
                return self._find_element_by_selector(selector=self._inner, timeout=0) is not None

    def is_hidden(self):
        try:
            splash = self._find_element_by_selector(selector=self._inner, timeout=0)
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=1)
            splash = self._find_element_by_selector(selector=self._inner, timeout=0)
        is_displayed = splash.is_displayed() if splash else False
        return not is_displayed

    def wait_to_hide(self, timeout=25):
        name = self.__class__.__name__
        result = wait_for_result(
            lambda: self.is_hidden(),
            name='%s to hide' % name,
            expected_result=True,
            timeout=timeout
        )
        if not result:
            raise VoltronException('%s is not hidden' % name)
