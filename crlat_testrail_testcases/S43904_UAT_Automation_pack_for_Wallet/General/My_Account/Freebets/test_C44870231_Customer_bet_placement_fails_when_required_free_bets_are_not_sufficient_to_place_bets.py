import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870231_Customer_bet_placement_fails_when_required_free_bets_are_not_sufficient_to_place_bets(Common):
    """
    TR_ID: C44870231
    NAME: Customer bet placement fails when required free bets are not sufficient to place bets
    DESCRIPTION: 
    PRECONDITIONS: Free bet amount 0.00
    PRECONDITIONS: UserName: goldenbuild1  Password : password1
    """
    keep_browser_open = True

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_login_with_above_user(self):
        """
        DESCRIPTION: Login with above user
        EXPECTED: User is logged in and free bet amount is displayed on My Account
        """
        pass

    def test_003_verify_user_can_add_a_selection_to_betslip_and_unable_to_place_a_bet_using_freebet(self):
        """
        DESCRIPTION: Verify user can add a selection to betslip and unable to place a bet using freebet
        EXPECTED: Error message displayed
        """
        pass
