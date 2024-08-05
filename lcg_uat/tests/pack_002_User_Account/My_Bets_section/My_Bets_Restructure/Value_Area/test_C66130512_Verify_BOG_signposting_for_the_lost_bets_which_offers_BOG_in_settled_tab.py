import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66130512_Verify_BOG_signposting_for_the_lost_bets_which_offers_BOG_in_settled_tab(Common):
    """
    TR_ID: C66130512
    NAME: Verify BOG signposting  for the lost bets which offers BOG in settled tab
    DESCRIPTION: This testcase verifies BOG signposting  for the lost bets which offers BOG in settled tab
    PRECONDITIONS: User should be login to application
    PRECONDITIONS: BOG bets should be available in settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_002_place_a_bet_on_horse_racing_selection_which_offers_bog(self):
        """
        DESCRIPTION: Place a bet on horse racing selection which offers BOG
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_wait_until_the_race_is_finished_make_sure_the_selection_must_lost_now_click_on_settled_tab(self):
        """
        DESCRIPTION: Wait until the race is finished. Make sure the selection must Lost. Now Click on settled tab
        EXPECTED: Settled tab is opened
        """
        pass

    def test_004_verify_bog_signposting_in_value_area_of_the_bet(self):
        """
        DESCRIPTION: Verify BOG signposting in value area of the bet
        EXPECTED: BOG signposting should be displayed
        """
        pass
