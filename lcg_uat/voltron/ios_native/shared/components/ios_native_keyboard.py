from voltron.ios_native.shared.components.ios_native_base import IOSNativeBase


class IOSNativeKeyboard(IOSNativeBase):
    _done_button = 'xpath=//XCUIElementTypeButton[contains(@label, "Done")]'

    @property
    def done_button(self):
        return IOSNativeBase(selector=self._done_button)

    def hide_keyboard(self):
        self.done_button.click()
