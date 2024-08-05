import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.descoped
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C401603_Betslip_View_with_NO_selections_added_on_Mobile(BaseBetSlipTest):
    """
    TR_ID: C401603
    VOL_ID: C11802795
    NAME: Betslip View with NO selections added on Mobile
    DESCRIPTION: This test case verifies the header of the Betslip with no selections added
    PRECONDITIONS: User account with positive balance
    PRECONDITIONS: Applies for Mobile
    """
    keep_browser_open = True

    def test_001_log_in_with_user_from_preconditions(self):
        """
        DESCRIPTION: Log in with User from Preconditions
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_click_betslip_icon_on_the_header(self):
        """
        DESCRIPTION: Click Betslip icon on the header
        EXPECTED: Betslip is opened
        EXPECTED: "Your betslip is empty" message in bold is shown at the top of Betslip content and "Please add one or more selections to place a bet" message is displayed below
        EXPECTED: "GO BETTING" button is displayed
        EXPECTED: User balance is displayed at the top right corner of the 'Betslip' header
        EXPECTED: 'Quick Deposit' link is not available in the Betslip header, only when user taps the balance button drop down with 'Hide Balance' and 'Deposit' options appear
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

    def test_003_tap_go_betting_button_and_verify_users_redirection_to_the_homepage(self):
        """
        DESCRIPTION: Tap 'GO BETTING' button and verify user's redirection to the Homepage
        EXPECTED: - User is redirected to the Homepage after the button tapping
        EXPECTED: - if previously Homepage was already opened than Betslip is closed and user stays on the Homepage
        """
        self.betslip.start_betting_button.click()
        self.site.wait_content_state('HomePage')
