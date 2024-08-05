from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class FreebetLink(ButtonBase):
    def is_enabled(self, expected_result=True, timeout=1, poll_interval=0.5, name=None,
                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, TypeError)):
        if not name:
            name = f'"{self.__class__.__name__}" enabled status is: "{expected_result}"'

        def _is_enabled(we):
            if we.get_attribute('class') is not None:
                return 'inactive' not in we.get_attribute('class').strip(' ').split(' ')
            else:
                return False

        result = wait_for_result(lambda: _is_enabled(we=self._we),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name,
                                 bypass_exceptions=bypass_exceptions)
        return result
