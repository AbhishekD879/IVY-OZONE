import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870226_Acca_Insurance__Verify_Signposting_Betslip_BetReceipt_My_Bets(Common):
    """
    TR_ID: C44870226
    NAME: Acca Insurance - Verify Signposting (Betslip/BetReceipt/My Bets)
    DESCRIPTION: 
    PRECONDITIONS: Football only.
    PRECONDITIONS: W-D-W only
    PRECONDITIONS: 5+ selections minimum.
    PRECONDITIONS: Valid on only 1st acca placed during the day.
    PRECONDITIONS: Minimum selection price 1/10.
    PRECONDITIONS: Minimum acca price 3/1.
    PRECONDITIONS: Up to Â£10 returned if 1 selection lets you down as a free bet
    """
    keep_browser_open = True

    def test_001_user_launches_the_siteapp_and_logs_in(self):
        """
        DESCRIPTION: User launches the site/app and logs in
        EXPECTED: User is able to place a bet as logged in customer
        """
        pass

    def test_002_navigate_to_football_slp(self):
        """
        DESCRIPTION: Navigate to Football SLP
        EXPECTED: User navigated to Football SLP
        """
        pass

    def test_003_place_5plus_w_d_w_acca_preplay_bet(self):
        """
        DESCRIPTION: Place 5+ W-D-W Acca (Preplay) bet
        EXPECTED: User has successfully placed a 5+ Acca and the Acca Insurance signposting is available in the bet slip,bet receipt and open bets and settled bets as per design
        """
        pass
