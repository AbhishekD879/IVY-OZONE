from voltron.pages.coral.components.header import CoralMobileHeader
from voltron.pages.coral.desktop_site import DesktopSite
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import find_element
from voltron.utils.waiters import wait_for_result


class TabletSite(DesktopSite):
    _header = 'xpath=.//vn-responsive-header'
    _left_hand_sport_menu = 'xpath=.//*[@data-crlat="leftColumn"]'
    _header_type = CoralMobileHeader

    @property
    def has_left_hand_sport_menu(self):
        return find_element(selector=self._left_hand_sport_menu, timeout=5) is not None

    @property
    def sport_menu(self):
        return self.home.menu_carousel

    def wait_logged_in(self, login_criteria=None, timeout=5):
        if login_criteria == 'betslip_balance':
            return wait_for_result(lambda: self.betslip.header.has_user_balance,
                                   name='User balance is displayed on Betslip',
                                   timeout=timeout)
        if login_criteria == 'betreceipt_balance':
            return wait_for_result(lambda: self.bet_receipt.user_header.has_user_balance,
                                   name='User balance is displayed on Betreceipt',
                                   timeout=timeout)
        return wait_for_result(lambda: self.header.has_right_menu() and self.header.right_menu_button.is_displayed(timeout=1),
                               timeout=timeout,
                               name='Right Menu button to be displayed',
                               bypass_exceptions=VoltronException)

    def __getattr__(self, name):
        raise VoltronException('%s class do not have "%s" option' % (self.__class__.__name__, name))
