from voltron.native.oxygen_native_base import OxygenBaseNative


class FastLoginPopUp(OxygenBaseNative):
    _use_button = {
        'android': 'xpath=//android.widget.Button[contains(@resource-id, "button_use_fingerprint")]',
        'ios': 'id=OK'
    }
    _not_now_button = {
        'android': 'xpath=//android.widget.Button[contains(@resource-id, "button_not_now")]',
        'ios': 'id=NOT NOW'
    }

    @property
    def use_button(self):
        return OxygenBaseNative(selector=self._use_button)

    @property
    def not_now_button(self):
        return OxygenBaseNative(selector=self._not_now_button)


class FastLoginConfirmedPopUp(OxygenBaseNative):
    _ok_button = {
        'android': 'xpath=//android.widget.Button[contains(@resource-id, "button_ok")]',
        'ios': 'id=OK'
    }

    @property
    def ok_button(self):
        return OxygenBaseNative(selector=self._ok_button)


class FastLoginDialog(OxygenBaseNative):
    _cancel_button = {
        'android': '//android.widget.Button[contains(@resource-id, "button2")]',
        'ios': 'id=Cancel'
    }

    @property
    def cancel_button(self):
        return OxygenBaseNative(selector=self._cancel_button)


class AutoLoginPopUp(OxygenBaseNative):
    _confirm_button = {
        'android': 'xpath=//android.widget.Button[contains(@resource-id, "button_confirm")]',
        'ios': 'id=CONFIRM'
    }

    @property
    def confirm_button(self):
        return OxygenBaseNative(selector=self._confirm_button)


class FailedLoginDialog(FastLoginDialog):
    _title = {
        'android': '//android.widget.Button[contains(@resource-id, "text_view_hint")]',
        'ios': 'id=Try Again'
    }
    _use_standard_button = {
        'android': '',
        'ios': 'id=Use Standard Login'
    }

    @property
    def title(self):
        return OxygenBaseNative(selector=self._title)

    @property
    def use_standard_button(self):
        return OxygenBaseNative(selector=self._use_standard_button)


class CoralNotificationDialog(OxygenBaseNative):
    _ok_button = {
        'android': '',
        'ios': 'id=OK'
    }
    _no_link = {
        'android': '',
        'ios': 'id=NO THANKS'
    }

    @property
    def ok_button(self):
        return OxygenBaseNative(selector=self._ok_button)
