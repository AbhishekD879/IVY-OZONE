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
class Test_C59925223_Verify_the_display_of_Next_races_panel_when_there_are_no_races(Common):
    """
    TR_ID: C59925223
    NAME: Verify the display of Next races panel when there are no races
    DESCRIPTION: Verify that when there are no races available then next races panel is not displayed
    PRECONDITIONS: 1: Racing post Tip should not be displayed
    PRECONDITIONS: 2: Next races should be enabled in CMS
    PRECONDITIONS: 3: Active races should NOT be available
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokescoral_app(self):
        """
        DESCRIPTION: Login to Ladbrokes/Coral App
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_place_a_single_bet_on_any_horse_racing_event(self):
        """
        DESCRIPTION: Place a Single bet on any Horse racing event
        EXPECTED: Bet receipt should be generated
        """
        pass

    def test_003_verify_next_races_panel_display(self):
        """
        DESCRIPTION: Verify Next races Panel display
        EXPECTED: Next races panel should not be displayed as there are no available races
        """
        pass
