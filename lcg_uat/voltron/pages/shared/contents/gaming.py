
from voltron.pages.shared.components.header import GlobalHeader
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.pages.shared.components.footer import Footer
from voltron.utils.waiters import wait_for_result


class GamingRightMenuItem(ComponentBase):
    _name = 'xpath=.//span[contains(@class, "link-title")]'
    _icon = 'xpath=.//span[contains(@class, "link-icon")]'

    @property
    def name(self):
        wait_for_result(lambda: self._get_webelement_text(selector=self._name, timeout=0) != '',
                        name='Waiting non empty value', timeout=10)
        return self._get_webelement_text(selector=self._name)

    @property
    def icon(self):
        return self._find_element_by_selector(selector=self._icon, timeout=0)

    def is_icon_displayed(self):
        return self._find_element_by_selector(selector=self._icon, timeout=0).is_displayed()


class GamingRightMenu(ComponentBase):
    _item = 'xpath=//li[contains(@class, "menu-link img-menu-link")]'
    _logout_link = 'xpath=//*[contains(@class, "menu-item-link")][.//*[text() = "Log Out"]]'
    _deposit_link = 'xpath=//a[contains(@class, "menu-item-link btn")][.//*[text() = "Deposit"]]'
    _logout_button = 'xpath=.//span[@class="btn--md popup-modal__button btn fn-accept popup-modal__button_type_accept"]'
    _list_item_type = GamingRightMenuItem

    @property
    def logout_link(self):
        return ButtonBase(selector=self._logout_link, timeout=5)

    @property
    def logout_button(self):
        return ButtonBase(selector=self._logout_button, timeout=5)

    @property
    def deposit_link(self):
        return ButtonBase(selector=self._deposit_link, timeout=5)


class Header(GlobalHeader):
    _sign_in = 'xpath=//*[contains(@class, "menu-item-link")][.//*[text() = "Log in"]]'
    _register = 'xpath=.//a[contains(@href, "signup")]'
    _show_right_menu_button = 'xpath=.//*[contains(@class, "h-avatar navbar-user-info")]'
    _login_button = 'xpath=//*[contains(@class, "menu-item-link")][.//*[contains(text(), "LOG IN")]]'
    _close_btn = 'xpath=.//*[@class="ui-icon ui-icon-size-lg ui-close theme-ex ng-star-inserted"]'

    @property
    def right_menu(self):
        return GamingRightMenu(selector=self._show_right_menu_button, context=self._we)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, timeout=5, context=self._we)

    def has_log_in_button(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._login_button, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'{self.__class__.__name__} Login Button displayed status to be {expected_result}')

    @property
    def close_btn(self):
        return ButtonBase(selector=self._close_btn, timeout=5, context=self._we)


class GamingFooter(Footer):
    _item = 'xpath=.//*[contains(@class, "menu-item") and (@section="BottomNav") and not (contains(@class, "hidden"))]/a | .//*[contains(@class, "menu-item") and (@linkclass="bottom-nav-link") and not (contains(@class, "hidden"))]/a'
    _list_item_type = ButtonBase


class LoginSection(ComponentBase):
    _login = 'xpath=.//div[contains(@class, "login__section--primary")]'
    _login_input = 'xpath=//input[@type="text"]'
    _password_input = 'xpath=//input[@type="password"]'
    _login_section_button = 'xpath=//*[@class="login w-100 btn btn-primary"]'

    def login_input(self, value):
        we = self._find_element_by_selector(selector=self._login_input, context=self._we)
        if we is None:
            raise VoltronException('No Login dialog is not present')
        we.clear()
        we.send_keys(value)

    def password_input(self, value):
        we = self._find_element_by_selector(selector=self._password_input, context=self._we)
        if we is None:
            raise VoltronException('No Login dialog is not present')
        we.clear()
        we.send_keys(value)

    @property
    def login_section_button(self):
        return ButtonBase(selector=self._login_section_button, timeout=5, context=self._we)


class Gaming(ComponentBase):
    _header = 'xpath=.//*[@class="header"]'
    _login_dialog = 'xpath=.//div[@class="login-container"]'
    _footer = 'xpath=.//*[contains(@class, "fixed-bottom")]'
    _login = 'xpath=.//div[contains(@id, "username")]'
    _pop_up_login_close_button = 'xpath=.//*[contains(@class, "logout-popup")]//*[contains(@class, "accept")]'

    def _wait_active(self, timeout=0):
        if not wait_for_result(lambda: self._find_element_by_selector(selector=self._header, context=get_driver(), timeout=0) is not None,
                               name='Gaming page is loaded',
                               timeout=10):
            self._logger.error('*** Error waiting for Gaming page')

    def wait_login(self, timeout=10):
        return wait_for_result(lambda: self.header.right_menu_button.is_displayed(),
                               name='Login Button should be visible',
                               expected_result=True,
                               timeout=timeout)

    @property
    def header(self):
        return Header(selector=self._header, timeout=5)

    @property
    def login_section(self):
        return LoginSection(selector=self._login, timeout=5, context=get_driver())

    def login(self, username='autotester0001', password='Qwerty19'):
        self.header.sign_in.click()
        self.login_section.login_input(username)
        self.login_section.password_input(password)
        self.login_section.login_section_button.click()
        success_login = self.wait_login()
        if not success_login:
            raise VoltronException('User is not logged out')

    def wait_logged_out(self, timeout=10):
        return wait_for_result(lambda: self.header.has_log_in_button(timeout=0) and self.header.login_button.is_displayed(timeout=0),
                               name='Login Button should be visible',
                               expected_result=True,
                               timeout=timeout)

    @property
    def pop_up_log_out(self):
        return ButtonBase(selector=self._pop_up_login_close_button, context=get_driver())

    def logout(self, timeout=10):
        self.header.right_menu_button.click()
        self.header.right_menu.logout_link.click()
        logged_out = self.wait_logged_out(timeout=timeout)
        if not logged_out:
            raise VoltronException('User is not logged out')

    @property
    def footer(self):
        return GamingFooter(selector=self._footer, context=self._we)
