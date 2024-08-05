from native_ios.pages.shared.components.base import IOSNativeBase


class Login(IOSNativeBase):
    _username_input = 'xpath=.//android.widget.EditText[@resource-id="userId"]'
    _password_input = 'xpath=.//android.view.View[@resource-id="password"]/android.widget.EditText'
    _login_button = 'xpath=.//android.widget.Button[@text="LOG IN"]'
    _odds_boost = 'xpath=//modal/div/div/div/div[2]/div/a'

    @property
    def username(self) -> IOSNativeBase:
        return IOSNativeBase(selector=self._username_input)

    @property
    def password(self) -> IOSNativeBase:
        return IOSNativeBase(selector=self._password_input)

    @property
    def login_button(self) -> IOSNativeBase:
        return IOSNativeBase(selector=self._login_button)

    @property
    def odds_boost(self) -> IOSNativeBase:
        return IOSNativeBase(selector=self._odds_boost, context=self._webview)

    @username.setter
    def username(self, value: str):
        self.username.click()
        self.password.clear()
        # self.username.enter_text(text=value)
        self.username._we.send_keys(value)

    @password.setter
    def password(self, value: str):
        self.password.click()
        self.password.clear()
        self.password._we.send_keys(value)

    def click_login(self):
        if self.login_button.is_enabled():
            self.login_button.click()
        else:
            raise Exception("Login Button Disabled")
