from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.header import GlobalHeader, ShowRightMenuButton
from voltron.pages.shared.components.primitives.buttons import ButtonBase, IconBase
from voltron.utils.waiters import wait_for_result


class CoralShowRightMenuButton(ComponentBase):
    _avatar_icon = 'xpath=.//*[@class="avatar-icon"]'

    @property
    def avatar_icon(self):
        return ComponentBase(selector=self._avatar_icon, context=self._we, timeout=1)

    def click(self):
        wait_for_result(lambda: self.avatar_icon.is_displayed(), timeout=5)
        self.avatar_icon.click()


class CoralHeaderUserBalance(ShowRightMenuButton):
    """
    Using ShowRightMenuButton as a parent class here due to available handling of amount string
    """
    _user_name = 'xpath=.//*[@class="user-name"]'
    _amount = 'xpath=.//*[contains(@class, "user-balance")]'

    @property
    def user_name(self):
        return self._get_webelement_text(selector=self._user_name, context=self._we)

    @property
    def amount_str(self):
        self.has_amount(timeout=20)
        return self._amount_we.get_attribute('innerHTML').replace(',', '')


class CoralUserPanelContent(ComponentBase):
    _balance = 'xpath=.//vn-h-balance'
    _avatar = 'xpath=.//vn-h-avatar/div'

    @property
    def balance(self):
        return CoralHeaderUserBalance(selector=self._balance, context=self._we, timeout=2)

    @property
    def my_account_button(self):
        """Named as my_account to have backward support with coral"""
        self.scroll_to_we()
        return CoralUserAvatar(selector=self._avatar, context=self._we, timeout=2)


class CoralUserAvatar(ComponentBase):
    _freebet_icon = 'xpath=.//*[contains(@class,"badge-circle")] | //span[contains(text(), "FB")]'

    @property
    def freebet_icon(self):
        return IconBase(selector=self._freebet_icon, context=self._we, timeout=2)

    def has_freebet_icon(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._freebet_icon, context=self._we, timeout=0) is not None,
            name=f'"Free Bet" info presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class CoralMobileUserPanel(CoralUserPanelContent):
    _my_bets_button = 'xpath=.//my-bets-button'

    @property
    def my_bets_button(self):
        return ButtonBase(selector=self._my_bets_button, context=self._we, timeout=2)


class CoralMobileHeader(GlobalHeader):
    _sign_in = 'xpath=.//vn-h-button//*[contains(@class, "btn-primary")]'
    _join_us = 'xpath=.//vn-h-button//*[contains(@class, "btn-secondary")]'
    _user_panel = 'xpath=.//vn-header-section[@vnelementkey="AUTH_HEADER_SECTION" or @class="navbar-wrapper-right"]'
    _user_panel_type = CoralMobileUserPanel
    _brand_logo = 'xpath=.//vn-h-logo//a'
    _show_right_menu_button = 'xpath=.//vn-h-avatar'
    _show_right_menu_button_type = CoralShowRightMenuButton
    _freebet_info = 'xpath=.//span[contains(text(), "FB")]'

    @property
    def user_balance_section(self):
        return self.user_panel.balance

    @property
    def user_balance(self):
        return self.user_balance_section.amount

    @property
    def user_panel(self):
        return self._user_panel_type(selector=self._user_panel, context=self._we, timeout=2.5)
