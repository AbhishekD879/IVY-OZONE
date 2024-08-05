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
class Test_C44870152_Verify_In_Review__Passed_Journey(Common):
    """
    TR_ID: C44870152
    NAME: Verify In Review - Passed Journey
    DESCRIPTION: "
    PRECONDITIONS: "IMS AGE verification status = Active grace period
    PRECONDITIONS: and
    PRECONDITIONS: player tag = AGP_Success_Upload =< 5 & Verfication_Review"
    """
    keep_browser_open = True

    def test_001_open_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/
        EXPECTED: BETA application launched
        """
        pass

    def test_002_verify_user_unable_to_place_bet(self):
        """
        DESCRIPTION: Verify user unable to place bet
        EXPECTED: User cannot place bet
        """
        pass

    def test_003_verify_user_unable_to_depositwithdraw(self):
        """
        DESCRIPTION: Verify user unable to Deposit/withdraw
        EXPECTED: User cannot deposit or place bet
        """
        pass

    def test_004_click_on_status_link_under_kyc_review_banner(self):
        """
        DESCRIPTION: Click on Status link under KYC review banner
        EXPECTED: Account in review banner should available
        EXPECTED: Right side Check Status should be displayed
        EXPECTED: 'Your account is restricted until verification is successfully completed'
        EXPECTED: https://app.zeplin.io/project/5c935fb0320dd2055d273d96/screen/5c9a0d19ff87da691c2c89ea
        """
        pass

    def test_005_verify_user_whilst_logged_in(self):
        """
        DESCRIPTION: Verify user whilst logged in.
        EXPECTED: KYC Banner remains.
        """
        pass

    def test_006_click_on_check_status(self):
        """
        DESCRIPTION: Click on check status
        EXPECTED: User presented with new message
        EXPECTED: 'You are not verified.......'
        """
        pass

    def test_007_place_bets(self):
        """
        DESCRIPTION: Place bets
        EXPECTED: User can place bets successfully
        """
        pass

    def test_008_deposit_funds(self):
        """
        DESCRIPTION: Deposit funds
        EXPECTED: User can successfully deposit
        """
        pass

    def test_009_withdraw_funds(self):
        """
        DESCRIPTION: Withdraw funds
        EXPECTED: User can successfully withdraw funds
        """
        pass
