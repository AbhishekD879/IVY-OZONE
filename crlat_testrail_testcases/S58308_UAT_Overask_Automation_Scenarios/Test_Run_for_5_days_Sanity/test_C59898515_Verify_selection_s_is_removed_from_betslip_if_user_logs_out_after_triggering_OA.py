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
class Test_C59898515_Verify_selection_s_is_removed_from_betslip_if_user_logs_out_after_triggering_OA(Common):
    """
    TR_ID: C59898515
    NAME: Verify selection/s is removed from betslip if user logs out after triggering OA.
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Login, Add selection and trigger OA
        EXPECTED: OA should be triggered.
        """
        pass

    def test_002_log_off(self):
        """
        DESCRIPTION: Log off
        EXPECTED: User should be logged off and betslip should be empty.
        """
        pass

    def test_003_log_back_in(self):
        """
        DESCRIPTION: Log back in
        EXPECTED: User should be logged in and betslip should be empty
        """
        pass

    def test_004_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Add selection and trigger OA
        EXPECTED: OA triggered
        """
        pass

    def test_005_log_off(self):
        """
        DESCRIPTION: Log off
        EXPECTED: user is logged off
        """
        pass

    def test_006_in_ti_accept_the_bet(self):
        """
        DESCRIPTION: In TI, accept the bet.
        EXPECTED: Bet should get placed succesfully.
        """
        pass

    def test_007_log_back_in(self):
        """
        DESCRIPTION: Log back in
        EXPECTED: Betslip should be empty, balance should be deducted for the bet accepted by trader and it should appear in My Bets.
        """
        pass

    def test_008_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Add selection and trigger OA
        EXPECTED: OA is triggered
        """
        pass

    def test_009_log_off(self):
        """
        DESCRIPTION: Log off
        EXPECTED: User is logged out
        """
        pass

    def test_010_in_ti_make_price_offer(self):
        """
        DESCRIPTION: In TI, make price offer
        EXPECTED: Price offer should be made
        """
        pass

    def test_011_user_add_same_selection_and_clicks_on_login_and_place_bet(self):
        """
        DESCRIPTION: User add same selection and clicks on login and place bet.
        EXPECTED: User should be logged in
        EXPECTED: User will not see price offer made by the trader
        EXPECTED: Also, another OA bet will be triggered.
        """
        pass
