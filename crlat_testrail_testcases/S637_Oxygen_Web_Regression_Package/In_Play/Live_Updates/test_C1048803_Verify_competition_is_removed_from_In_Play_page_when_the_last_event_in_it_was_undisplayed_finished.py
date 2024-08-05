import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C1048803_Verify_competition_is_removed_from_In_Play_page_when_the_last_event_in_it_was_undisplayed_finished(Common):
    """
    TR_ID: C1048803
    NAME: Verify competition is removed from In Play page when the last event in it was undisplayed/finished
    DESCRIPTION: This test case verifies removing competition from In Play page when the last event in it was undisplayed/finished
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose Sport in Sports Menu Ribbon
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: __HOW TO: create upcoming event:__
    PRECONDITIONS: Event level:
    PRECONDITIONS: ‘Start Time:’- Current time + few hours
    PRECONDITIONS: ‘Is Off’ - No or N/A
    PRECONDITIONS: ‘Bet In Play List’ - flag enabled
    PRECONDITIONS: Market Level:
    PRECONDITIONS: ‘Bet In Running’ - flag enabled
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose ?EIO=3&transport=websocket record
    """
    keep_browser_open = True

    def test_001_for_mobilefind_a_competition_with_only_one_event_and_collapse_that_competition(self):
        """
        DESCRIPTION: **For Mobile:**
        DESCRIPTION: Find a competition with only one event and collapse that competition
        EXPECTED: 
        """
        pass

    def test_002_in_ti__undisplay_the_event_from_step_1(self):
        """
        DESCRIPTION: In TI  undisplay the event from step 1
        EXPECTED: 
        """
        pass

    def test_003_back_in_oxygen_app_and_verify_changes(self):
        """
        DESCRIPTION: Back in oxygen app and verify changes
        EXPECTED: * The collapsed competition to which event belonged is removed from In Play
        EXPECTED: * IN_PLAY_SPORT_COMPETITION_CHANGED::<sport_category_id>::LIVE_EVENT record in WS with update, containing
        EXPECTED: 'removed:["<typeId>"]'
        """
        pass

    def test_004_repeat_steps_1_3_for_upcoming_section(self):
        """
        DESCRIPTION: Repeat steps 1-3 for 'Upcoming' section
        EXPECTED: *Message should look like: IN_PLAY_SPORT_COMPETITION_CHANGED::<sport_category_id>::UPCOMING_EVENT*
        """
        pass

    def test_005_repeat_steps_1_4_on_sport_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat Steps 1-4 on Sport Landing page - In Play tab
        EXPECTED: 
        """
        pass

    def test_006_for_desktopnavigate_to_in_play__live_stream_section_on_homepageand_repeat_steps_1_3_for_both_in_play_and_live_stream_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage
        DESCRIPTION: and repeat steps №1-3 for both 'In-Play' and 'Live Stream' filter switchers
        EXPECTED: Respective updates are received in 'INPLAY_LS_SPORT_COMPETITION_CHANGED' response
        """
        pass
