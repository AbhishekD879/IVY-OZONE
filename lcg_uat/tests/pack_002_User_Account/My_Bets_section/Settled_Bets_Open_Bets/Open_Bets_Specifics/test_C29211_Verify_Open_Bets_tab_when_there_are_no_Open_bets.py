import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.portal_dependant
@pytest.mark.desktop
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29211_Verify_Open_Bets_tab_when_there_are_no_Open_bets(BaseBetSlipTest):
    """
    TR_ID: C29211
    VOL_ID: C9697786
    NAME: Verify 'Open Bets' tab when there are no Open bets
    DESCRIPTION: This test case verifies 'Open Bets' tab when no open bets are present.
    """
    keep_browser_open = True
    default_days = 30
    open_bet_message = "No open bets placed within the last " + str(default_days) + " days."

    def test_001_login_as_user_that_have_never_placed_bet(self):
        """
        DESCRIPTION: Login as user that has never placed bet
        EXPECTED: Successfully logged in
        """
        self.site.login(username=tests.settings.no_bet_history_user, async_close_dialogs=False)

        self.__class__.expected_tabs = self.get_expected_my_bets_tabs()

    def test_002_go_to_my_bets(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: 'My Bets' page / 'Bet Slip' widget is opened
        EXPECTED: 'Open Bets' tab is shown next to 'Cash Out' tab
        """
        self.site.open_my_bets_cashout()
        page_title = self.site.cashout.header_line.page_title.title
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.expected_my_bets_page_title = self.expected_my_bets_page_title.upper()
        self.assertEqual(page_title, self.expected_my_bets_page_title,
                         msg='Page title "%s" doesn\'t match expected text "%s"'
                             % (page_title, self.expected_my_bets_page_title))

        expected_tabs = self.get_expected_my_bets_tabs()
        if self.device_type == 'mobile':
            tabs = self.site.cashout.tabs_menu.items_as_ordered_dict
        else:
            tabs = self.site.betslip.tabs_menu.items_as_ordered_dict
        self.assertListEqual(list(tabs.keys()), expected_tabs,
                             msg=f'List of tabs {list(tabs.keys())} is not the same as expected {expected_tabs}')
        tabs.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: 'Regular' sort filter is selected by default
        """
        result = wait_for_result(
            lambda: self.site.open_bets.tab_content.grouping_buttons.current == self.expected_active_btn_open_bets,
            name='"%s" to became active' % self.expected_active_btn_open_bets,
            timeout=2)
        self.assertTrue(result, msg='%s sorting type is not selected by default' % self.expected_active_btn_open_bets)

    def test_004_verify_messageon_open_bets_tab_regular_sort_filter(self):
        """
        DESCRIPTION: Verify message on 'Open Bets' tab - 'Regular' sort filter
        EXPECTED: 'You currently have no open bets.' message is displayed
        """
        open_bets = self.site.open_bets.tab_content.accordions_list
        self.assertEqual(open_bets.no_bets_text.upper(), self.open_bet_message.upper(),
                         msg='Message "%s" does not match expected "%s"' %
                             (open_bets.no_bets_text, self.open_bet_message))

    def test_005_select_pools_sort_filter(self):
        """
        DESCRIPTION: Select 'Pools' sort filter
        EXPECTED: 'You currently have no open bets.' message is displayed
        """
        result = self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.POOLS_TAB_NAME)
        self.assertTrue(result, msg='%s sorting type is not selected' % vec.bet_history.POOLS_TAB_NAME)

        open_bets = self.site.open_bets.tab_content.accordions_list
        self.assertEqual(open_bets.no_bets_text, vec.bet_history.NO_OPEN_BETS,
                         msg='Message "%s" does not match expected "%s"' %
                             (open_bets.no_bets_text, vec.bet_history.NO_OPEN_BETS))
