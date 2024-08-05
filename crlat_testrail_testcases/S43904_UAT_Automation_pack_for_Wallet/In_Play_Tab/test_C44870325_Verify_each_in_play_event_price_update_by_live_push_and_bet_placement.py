import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870325_Verify_each_in_play_event_price_update_by_live_push_and_bet_placement(Common):
    """
    TR_ID: C44870325
    NAME: Verify each in play event price update by live push and bet placement
    DESCRIPTION: this test case verify price updates on  inplay tab and bet placement
    PRECONDITIONS: UserName : goldebuild1 Password: password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: In-Play tab opened with all inplay sports
        """
        pass

    def test_003_go_to_football_and_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go to Football and Add selections to the Betslip
        EXPECTED: Selection added
        """
        pass

    def test_004_verify_price_update_in_in_play_sport_and_betslip(self):
        """
        DESCRIPTION: Verify price update in In-Play sport and betslip
        EXPECTED: Message appear in betslip - Price is changed from XX to XX
        """
        pass

    def test_005_click_on_accept_and_place_bet_button(self):
        """
        DESCRIPTION: Click on 'Accept and Place bet' Button
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_006_repeat_step_3_to_5_for_all_inplay_sports(self):
        """
        DESCRIPTION: Repeat step #3 to #5 for all inplay sports
        EXPECTED: 
        """
        pass
