import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29113_Verify_My_Freebets_Bonuses_page(Common):
    """
    TR_ID: C29113
    NAME: Verify 'My Freebets/Bonuses' page
    DESCRIPTION: This Test Case verified 'My Freebets/Bonuses' page
    DESCRIPTION: AUTOTEST [C527671]
    PRECONDITIONS: 1. User is logged  ( freebets list is received in **user** request only after login)
    PRECONDITIONS: 2. User has Free Bets available on his account
    PRECONDITIONS: 3.  **accountFreebets?freebetTokenType=SPORT** request is used to get a list of all free bets and called on 'My Balance & Freebets' page ONLY (open dev tools -> Network ->XHR tab)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_right_menu(self):
        """
        DESCRIPTION: Open right menu
        EXPECTED: 'My Balance & Freebets' icon displayed
        """
        pass

    def test_003_tap_onmy_balance__freebets(self):
        """
        DESCRIPTION: Tap on 'My Balance & Freebets'
        EXPECTED: 'My Balance & Freebets' page is opened
        """
        pass

    def test_004_open_my_balance__freebets_page(self):
        """
        DESCRIPTION: Open 'My Balance & Freebets' page
        EXPECTED: 'My Balance & Freebets' page consists of:
        EXPECTED: * Back button
        EXPECTED: * 'My Freebets/bonuses' title
        EXPECTED: * Cash Balance
        EXPECTED: * Total Balance
        EXPECTED: * Free bets section
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User is navigated to homepage
        """
        pass

    def test_006_verify_cash_balance(self):
        """
        DESCRIPTION: Verify Cash Balance
        EXPECTED: * Cash Balance is equal to user balance on the Header
        EXPECTED: * Cash Balance corresponds to **balances.[i].balance.amount** attribute, where **balanceType = sportsbook_gaming_balance** from 32010 responce (Dev tools -> Network -> WS)
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

    def test_009_freebet_item_contains(self):
        """
        DESCRIPTION: Freebet item contains:
        EXPECTED: * Free bet description
        EXPECTED: * 'Use by' label + DD/MM/YYYY date if free bet expires in more than 7 days inclusive
        EXPECTED: **OR**
        EXPECTED: 'Expires' + number of day left if free bet expires in less than 7 days
        EXPECTED: * Free bet icon + Free bet value with appropriate currency
        EXPECTED: * '>' icon and link to the Freebet Details page
        """
        pass

    def test_010_tap_on_any_free_bet_item(self):
        """
        DESCRIPTION: Tap on any 'Free bet' item
        EXPECTED: 'Freebet' detailed page is opened
        """
        pass

    def test_011_place_a_bet_on_selection_by_using_free_bet(self):
        """
        DESCRIPTION: Place a bet on selection by using free bet
        EXPECTED: Bet placement is placed successfully
        """
        pass

    def test_012_go_to_my_balance__freebets_page(self):
        """
        DESCRIPTION: Go to 'My Balance & Freebets' page
        EXPECTED: * Page is opened
        EXPECTED: * Used on step #11 Free bet is not displayed within list of all free bets tokens
        """
        pass
