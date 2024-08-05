from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class Overask(ComponentBase):
    _overask_title = 'xpath=.//*[@data-crlat="oTitleRow"]'
    _overask_exceeds = 'xpath=.//*[@data-crlat="oTopMessage"]'
    _overask_offer = 'xpath=.//*[@data-crlat="oBottomMessage"]'
    _overask_spinner = 'xpath=.//*[@data-crlat="oSpinnerRow"]'

    @property
    def overask_title(self):
        return ComponentBase(selector=self._overask_title, context=self._we, timeout=10)

    @property
    def overask_exceeds(self):
        return ComponentBase(selector=self._overask_exceeds, context=self._we)

    @property
    def overask_offer(self):
        return ComponentBase(selector=self._overask_offer, context=self._we)

    @property
    def overask_spinner(self):
        return ComponentBase(selector=self._overask_spinner, context=self._we)

    def has_overask_warning(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._overask_title, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Overask warning message presence status in {self.__class__.__name__} to be {expected_result}')
