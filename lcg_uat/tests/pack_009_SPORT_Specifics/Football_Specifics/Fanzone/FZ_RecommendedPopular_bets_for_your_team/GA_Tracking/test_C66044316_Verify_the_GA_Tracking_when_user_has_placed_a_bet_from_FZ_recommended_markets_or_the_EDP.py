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
class Test_C66044316_Verify_the_GA_Tracking_when_user_has_placed_a_bet_from_FZ_recommended_markets_or_the_EDP(Common):
    """
    TR_ID: C66044316
    NAME: Verify the GA Tracking when user has placed a bet from FZ recommended markets or the EDP
    DESCRIPTION: This test case is to verify GA Tracking when user has placed a bet from FZ recommended markets or the EDP
    PRECONDITIONS: 1. Bets Based On Your Team Module and Bets Based On Other Fans Module is configured and Enabled in Fanzone.
    PRECONDITIONS: 2. CMS Navigations --
    PRECONDITIONS: CMS -> Sports Pages -> Sport Categories -> Fanzone -> Bets Based On Your Team Module & Bets Based On Other Fans Module
    PRECONDITIONS: 3. CMS -> Fanzone-> Fanzones -> Fanzone Name ->
    PRECONDITIONS: Fanzone Configurations -> ON/OFF Toggle for Show Bets Based On Your Team & Show Bets Based on Other Fanzone Team
    """
    keep_browser_open = True

    def test_000_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the Application and Login with Valid Credentials
        EXPECTED: User should launch the Application and Login Successfully
        """
        pass

    def test_000_place_a_bet_from_fz_recommended_markets_or_the_edp(self):
        """
        DESCRIPTION: Place a bet from FZ recommended markets or the EDP.
        EXPECTED: User could able to place a bet successfully
        """
        pass

    def test_000_verify_ga_tracking_in_console_for_the_dimension64_and_dimension65(self):
        """
        DESCRIPTION: Verify GA tracking in console for the dimension64 and dimension65
        EXPECTED: dimension64: Fanzone
        EXPECTED: dimension65: ADA Recommended bets carousel.
        """
        pass
