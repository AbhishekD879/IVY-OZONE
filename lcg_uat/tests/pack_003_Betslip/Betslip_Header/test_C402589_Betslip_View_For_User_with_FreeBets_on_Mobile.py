import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets on prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C402589_Betslip_View_For_User_with_FreeBets_on_Mobile(BaseBetSlipTest):
    """
    TR_ID: C402589
    VOL_ID: C9698411
    NAME: Betslip View For User with FreeBets on Mobile
    DESCRIPTION: This test case verifies whether freebet icon is displayed in the right side of the balance bar of
    DESCRIPTION: the Betslip header if user has free bets
    PRECONDITIONS: Make sure you have user account with free bets available
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1, self.__class__.selection_ids = event_params.team1, event_params.selection_ids

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        """
        self.site.wait_content_state('Homepage')

    def test_002_log_in_with_account_with_free_bets_available(self):
        """
        DESCRIPTION: Log in with **account with free bets available**
        EXPECTED: User is successfully logged in
        """
        self.site.login(username=tests.settings.freebet_user, async_close_dialogs=False)
        self.assertTrue(self.site.header.has_freebets(), msg='User does not have Free bets')

    def test_003_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Betslip is opened
        EXPECTED: "Your betslip is empty" message in bold is shown at the top of Betslip content and "Please add one or
        EXPECTED: more selections to place a bet" message is displayed below
        EXPECTED: "GO BETTING" button is displayed
        EXPECTED: User balance is displayed at the top right corner of the 'Betslip' header
        EXPECTED: 'Quick Deposit' link is not available in the Betslip header, only when user taps the balance button
        EXPECTED: drop down with 'Hide Balance' and 'Deposit' options appear
        EXPECTED: 'FB' icon is NOT displayed in the right corner of the balance bar in the 'Betslip' header
        """
        self.site.header.bet_slip_counter.click()

        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened, but was expected to be opened')

        self.__class__.betslip = self.get_betslip_content()

        title = self.betslip.betslip_title
        self.assertEqual(title, vec.betslip.BETSLIP_BTN,
                         msg=f'Betslip title "{title}" is not the same as expected "{vec.betslip.BETSLIP_BTN}"')

        symbol = self.betslip.header.currency_symbol
        self.assertEqual(self.betslip.header.currency_symbol, "£",
                         msg=f'Betslip sub-header currency symbol "{symbol}" is not the same as expected "£"')

        self.assertTrue(self.betslip.header.has_user_balance,
                        msg='Betslip sub-header user balance is not displayed, but was expected to be displayed')

        message = self.betslip.no_selections_title
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Betslip "No selections" message "{message}" is not the same as expected '
                         f'"{vec.betslip.NO_SELECTIONS_TITLE}"')

        has_deposit_form = self.get_betslip_content().has_deposit_form(expected_result=False)
        self.assertFalse(has_deposit_form, msg='Deposit section is visible!')

    def test_004_close_betslip(self):
        """
        DESCRIPTION: Close Betslip
        EXPECTED: Betslip is closed
        """
        self.site.close_betslip()

    def test_005_add_a_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add a selection to the Betslip
        EXPECTED: Betslip is opened
        EXPECTED: User balance is displayed at the top right corner of the 'Betslip' header
        EXPECTED: Coral only: 'Quick Deposit' link is not available in the Betslip header, only when user taps the balance button drop down with 'Hide Balance' and 'Deposit' options appear
        EXPECTED: 'FB' icon is NOT displayed in the right corner of the balance bar in the 'Betslip' header
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1]))
        self.assertTrue(self.betslip.header.has_user_balance,
                        msg='Betslip sub-header user balance is not displayed')

        if self.brand != 'ladbrokes':
            betslip = self.get_betslip_content()
            self.assertFalse(betslip.has_deposit_form(expected_result=False),
                             msg='Deposit section is visible')

            self.assertTrue(betslip.quick_deposit_link.is_displayed(), msg='Quick Deposit is not displayed')

        self.assertFalse(self.site.header.has_freebets(expected_result=False, on_betslip=True), msg='Freebet info is shown in user header')
