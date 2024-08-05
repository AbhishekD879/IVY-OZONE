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
class Test_C44870323_Verify_user_navigate_to_selected_EDP_when_clicking_on_in_play_tab_events_(Common):
    """
    TR_ID: C44870323
    NAME: "Verify user navigate to selected EDP when clicking on in-play tab events "
    DESCRIPTION: this test case verify navigation to EDP pages
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home Page is opened
        """
        pass

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: All inplay sports is displayed
        """
        pass

    def test_003_click_on_any_football_event(self):
        """
        DESCRIPTION: Click on any football event
        EXPECTED: Event Detail page is opened
        """
        pass

    def test_004_repeat_step_3_for_all_inplay_sports_egtennis_golf(self):
        """
        DESCRIPTION: Repeat step #3 for all inplay sports eg:tennis, golf
        EXPECTED: 
        """
        pass
