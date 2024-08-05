import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870161_Verify_the_header_for_a_logged_in_user_Desktop_Mobile(Common):
    """
    TR_ID: C44870161
    NAME: "Verify the header for a logged in user (Desktop/Mobile)
    DESCRIPTION: and once clicked on downward facing chevron next to my avatar My Account overlay is shown (with drop down option available, eg: Banking My Bets, Odds Boosts, FreeBets,Redeem Vouchers, Bet History, Personal Details,
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_the_header_for_a_logged_in_user_mobiletablet(self):
        """
        DESCRIPTION: Verify the header for a logged in user Mobile/Tablet
        EXPECTED: User is displayed with My bets/Balance/Avatar/Betslip
        """
        pass

    def test_002_verify_the_header_for_a_logged_in_user_desktop(self):
        """
        DESCRIPTION: Verify the header for a logged in user Desktop
        EXPECTED: User is displayed with Deposit/Balance/Messages/Avatar/
        """
        pass

    def test_003_once_clicked_avatar(self):
        """
        DESCRIPTION: Once clicked Avatar
        EXPECTED: My account Menu with the following elements are shown:
        EXPECTED: Banking, Offers & Free bets, History, Messages, Connect, Settings, Gambling Controls, Help & Contact, Logout, Deposit
        """
        pass

    def test_004_on_clicking_my_bets(self):
        """
        DESCRIPTION: On clicking 'My bets,
        EXPECTED: My bets with following elements are shown,
        EXPECTED: Cashout, Open bets, Settle bets, Shop bets
        """
        pass

    def test_005_on_clickingbalance(self):
        """
        DESCRIPTION: On clicking'Balance'
        EXPECTED: Following elements are shown,
        EXPECTED: Withdrawable Online
        EXPECTED: Restricted
        EXPECTED: Available Balance
        EXPECTED: Total Balance
        EXPECTED: Deposit
        EXPECTED: Balance available to user on: Sports/Casino/Poker/Bingo
        """
        pass
