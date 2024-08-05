import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C64055792_GALAXY_S9_Verify_remember_last_Sport_functionality_on_In_Play_page_for_Logged_In_user(Common):
    """
    TR_ID: C64055792
    NAME: [GALAXY S9] Verify remember last Sport functionality on In-Play page for Logged In user
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001___________add_football_event(self):
        """
        DESCRIPTION: *          Add Football event
        EXPECTED: *
        """
        pass

    def test_002___________go_to_in_play_page(self):
        """
        DESCRIPTION: *          Go to In-Play page
        EXPECTED: *          * 'In-Play' page is opened
        EXPECTED: *          * First <Sport> tab is opened by default
        """
        pass

    def test_003___________choose_any_sports_icon(self):
        """
        DESCRIPTION: *          Choose any Sports icon
        EXPECTED: *          * Selected Sports tab is underlined by red line
        EXPECTED: *          * The appropriate content is displayed for selected Sports
        """
        pass

    def test_004___________navigate_across_application(self):
        """
        DESCRIPTION: *          Navigate across application
        EXPECTED: *
        """
        pass

    def test_005___________back_to_in_play_page(self):
        """
        DESCRIPTION: *          Back to In-Play page
        EXPECTED: *          * 'In-Play' page is opened
        EXPECTED: *          * Tab from step 2 is selected and underlined by red line
        """
        pass

    def test_006___________repeat_steps_1_4_when_there_are_no_in_play_events_for_saved_sport(self):
        """
        DESCRIPTION: *          Repeat steps 1-4 when there are no In-Play events for saved sport
        EXPECTED: *          * 'In-Play' Landing Page is opened
        EXPECTED: *          * First <Sport> tab is opened by default and underlined by red line
        """
        pass
