from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.betslip_tabs_menu import BetslipTabsMenu
from voltron.pages.shared.contents.betslip.betslip import BetSlip, LottoBetSlip
from voltron.utils.waiters import wait_for_result


class BetSlipDesktop(BetSlip):
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers"]'
    _login_button_on_betslip = 'xpath=.//*[@data-crlat="signInButton"]'
    _unlocked_icon = 'xpath=.//*[@data-crlat="unlockedIcon"]'
    _locked_icon = 'xpath=.//*[@data-crlat="lockedIcon"]'
    _header_tabs = 'xpath=.//*[@data-crlat="bsTabsWrapper"]'
    _header_tabs_type = BetslipTabsMenu

    def wait_for_betslip_widget_displayed(self, open_status=True, timeout=7):
        """Waits for betslip widget to be opened of closed
           Just specify open status as a parameter, True goes for open, False - for close"""
        return wait_for_result(
            lambda: self.is_displayed(),
            name='Betslip widget displayed',
            expected_result=open_status,
            timeout=timeout
        )

    @property
    def name(self):
        return self.betslip_tabs.current

    @property
    def betslip_tabs(self):
        return self._header_tabs_type(selector=self._header_tabs, context=self._we, timeout=1)

    @property
    def header(self):
        raise NotImplementedError('There\'s no user info header on Desktop Betslip widget')

    @property
    def close_button(self):
        raise NotImplementedError('There\'s no close button on Desktop Betslip widget')

    @property
    def tabs_menu(self):
        return GroupingSelectionButtons(selector=self._tabs_menu, context=self._we)

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button_on_betslip, context=self._we)

    @property
    def unlocked_icon(self):
        return ComponentBase(selector=self._unlocked_icon, context=self._we, timeout=1)

    @property
    def locked_icon(self):
        return ComponentBase(selector=self._locked_icon, context=self._we, timeout=1)

    @property
    def betslip_sections_list(self):
        self._spinner_wait()
        return self._betslip_sections_list_type(selector=self._betslip_sections_list, context=self._we, timeout=3)


class LottoBetSlipDesktop(LottoBetSlip, BetSlipDesktop):
    pass
