import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C16706455_Vanilla_Coral_Verify_My_Freebets_Bonuses_page(Common):
    """
    TR_ID: C16706455
    NAME: [Vanilla Coral] Verify 'My Freebets/Bonuses' page
    DESCRIPTION: This Test Case verified 'My Freebets/Bonuses' page
    PRECONDITIONS: 1. User is logged ( freebets list is received in user request only after login)
    PRECONDITIONS: 2. User has Free Bets available on his account
    """
    keep_browser_open = True

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_account_button_on_the_header(self):
        """
        DESCRIPTION: Tap Account button on the header
        EXPECTED: Account Menu is displayed
        """
        pass

    def test_003_tap_offers__free_bets_options_from_the_list(self):
        """
        DESCRIPTION: Tap 'OFFERS & FREE BETS' options from the list
        EXPECTED: 'OFFERS & FREE BETS' menu is open
        """
        pass

    def test_004_tap_sports_free_bets_option(self):
        """
        DESCRIPTION: Tap 'SPORTS FREE BETS' option
        EXPECTED: 'My Freebets/Bonuses' page consists of:
        EXPECTED: * Back button
        EXPECTED: * 'My Freebets/Bonuses' title
        EXPECTED: * Cash Balance
        EXPECTED: * Total Balance
        EXPECTED: * Free bets section
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User is navigated to the previous page after tapping Back button
        """
        pass

    def test_006_verify_cash_balance(self):
        """
        DESCRIPTION: Verify Cash Balance
        EXPECTED: * Cash Balance is equal to user balance on the Header
        """
        pass

    def test_007_verify_total_balance(self):
        """
        DESCRIPTION: Verify Total Balance
        EXPECTED: Total balance is sum of all free bets and customer cash balance
        """
        pass

    def test_008_verify_free_bets_section(self):
        """
        DESCRIPTION: Verify Free bets section
        EXPECTED: Free bets section consists of:
        EXPECTED: * Expandable/collapsible panel
        EXPECTED: * Free bets icon
        EXPECTED: * Currency symbol + amount of all free bets available
        EXPECTED: * Free bets label
        EXPECTED: * List of all free bets
        EXPECTED: * CMS-controlled text message in case if there are no free bets available
        """
        pass

    def test_009_verify_free_bets_item(self):
        """
        DESCRIPTION: Verify Free bets item
        EXPECTED: Free bets item consists of:
        EXPECTED: * Free bet description
        EXPECTED: * 'Use by' label + DD/MM/YYYY date if free bet expires in more than 7 days inclusive
        EXPECTED: **OR**
        EXPECTED: 'Expires' + number of day left if free bet expires in less than 7 days
        EXPECTED: * Free bet icon + Free bet value with appropriate currency
        EXPECTED: * '&gt;' icon and link to the Freebet Details page
        """
        pass

    def test_010_tap_on_any_free_bet_item(self):
        """
        DESCRIPTION: Tap on any 'Free bet' item
        EXPECTED: 'FREEBET INFORMATION' page is opened
        """
        pass

    def test_011_place_a_bet_on_selection_by_using_free_bet(self):
        """
        DESCRIPTION: Place a bet on selection by using free bet
        EXPECTED: Bet placement is placed successfully
        """
        pass

    def test_012_go_to_my_freebetsbonuses_page(self):
        """
        DESCRIPTION: Go to 'My Freebets/Bonuses' page
        EXPECTED: * Page is opened
        EXPECTED: * Used on step #11 Free bet is not displayed within list of all free bets tokens
        """
        pass
