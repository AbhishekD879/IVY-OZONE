from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class YourCallStaticBlock(ComponentBase):
    _icon = 'xpath=.//*[@data-crlat="yourcallIcon"]'
    _static_text = 'xpath=.//*[@data-crlat="yourcallStaticText"]'

    def has_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._icon, context=self._we, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def static_text(self):
        return self._get_webelement_text(selector=self._static_text)

    @property
    def link(self):
        we = self._find_element_by_selector(selector=self._static_text, context=self._we)
        return we.get_attribute('innerHTML') if we.get_attribute('innerHTML') else self._get_webelement_text(we=we)
