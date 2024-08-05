from voltron.pages.shared.components.base import ComponentBase


class TimeManagementOverlayContainer(ComponentBase):
    _message = 'xpath=.//*[@id="toast-container"]'

    @property
    def successful_message(self):
        return self._find_element_by_selector(selector=self._message, context=self._we)
