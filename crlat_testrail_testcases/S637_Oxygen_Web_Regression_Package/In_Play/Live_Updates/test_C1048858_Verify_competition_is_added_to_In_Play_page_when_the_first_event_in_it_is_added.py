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
class Test_C1048858_Verify_competition_is_added_to_In_Play_page_when_the_first_event_in_it_is_added(Common):
    """
    TR_ID: C1048858
    NAME: Verify competition is added to In Play page when the first event in it is added
    DESCRIPTION: This test case verifies competition is added to In Play page when the first event in it is added
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab > 'Live Now' section/switcher
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose ?EIO=3&transport=websocket record
    PRECONDITIONS: * Make sure that no events are present within tested competition
    """
    keep_browser_open = True

    def test_001_in_ti_create_a_new_competition_and_an_inplay_event_in_it_make_sure_event_is_not_suspended_and_is_displayed(self):
        """
        DESCRIPTION: In TI create a new competition and an inplay event in it (make sure event is not Suspended and is Displayed)
        EXPECTED: 
        """
        pass

    def test_002_back_in_oxygen_app_verify_changes(self):
        """
        DESCRIPTION: Back in Oxygen app verify changes
        EXPECTED: * The newly added competition appears collapsed at the bottom of <Sport> section disregarding its Display order
        EXPECTED: * 42["IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT",…] record in WS containing:
        EXPECTED: {added: [{className: ..., categoryName: ...", categoryCode: ...,…}],…}
        EXPECTED: * event is not subscribed for updates
        """
        pass

    def test_003_refresh_page_or_navigate_between_tabs_and_back(self):
        """
        DESCRIPTION: Refresh page or navigate between tabs and back
        EXPECTED: * The newly added competition changes it's position on page according to it's disporder on sport type level
        """
        pass

    def test_004_expand_competition(self):
        """
        DESCRIPTION: Expand competition
        EXPECTED: event subscribe record is sent :
        EXPECTED: 42["subscribe", [<event_id>]]
        """
        pass

    def test_005_repeat_steps_1_4_for_upcoming_sorting_type(self):
        """
        DESCRIPTION: Repeat steps 1-4 for Upcoming sorting type
        EXPECTED: *Message should look like: IN_PLAY_SPORT_COMPETITION_CHANGED::<sport_category_id>::UPCOMING_EVENT*
        """
        pass

    def test_006_repeat_steps_1_5_when_some_sport_selected_in_sports_menu_ribbon(self):
        """
        DESCRIPTION: Repeat Steps 1-5 when some Sport selected in Sports Menu Ribbon
        EXPECTED: * The newly added competition appears collapsed at the bottom of <Type> section disregarding its Display order
        EXPECTED: * 42["IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT",…] record in WS containing:
        EXPECTED: {added: [{className: ..., categoryName: ...", categoryCode: ...,…}],…}
        EXPECTED: * event is not subscribed for updates
        """
        pass

    def test_007_repeat_steps_1_5_on_sport_landing_page___in_play_tab(self):
        """
        DESCRIPTION: Repeat steps 1-5 on Sport Landing page - In Play tab
        EXPECTED: 
        """
        pass

    def test_008_for_mobiletabletrepeat_steps_1_5_on_home_page___in_play_tab(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Repeat steps 1-5 on Home page - In Play tab
        EXPECTED: 
        """
        pass

    def test_009_for_desktopnavigate_to_in_play__live_stream_section_on_homepageand_repeat_step_3_for_both_in_play_and_live_stream_filter_switchers(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'In-Play & Live Stream ' section on Homepage
        DESCRIPTION: and repeat step #3 for both 'In-Play' and 'Live Stream' filter switchers
        EXPECTED: Respective updates are received in 'INPLAY_LS_SPORT_COMPETITION_CHANGED' response
        """
        pass

    def test_010_back_in_oxygen_app_verify_changes_on_in_play_and_live_stream_section_and_choose_in_play_switcher(self):
        """
        DESCRIPTION: Back in Oxygen app verify changes on 'In-Play' and 'Live Stream' section and choose 'In-Play' switcher
        EXPECTED: * The newly added competition appears expanded at the appropriate place depending on Display order <Type> section
        EXPECTED: * 42["IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT",…] record in WS containing:
        EXPECTED: {added: [{className: ..., categoryName: ...", categoryCode: ...,…}],…}
        EXPECTED: * event is subscribed for updates
        """
        pass

    def test_011_choose_live_stream_switcher(self):
        """
        DESCRIPTION: Choose 'Live Stream' switcher
        EXPECTED: * The newly added competition appears expanded at the appropriate place depending on Display order <Type> section
        EXPECTED: * 42["IN_PLAY_SPORT_COMPETITION_CHANGED::<category_id>::LIVE_EVENT",…] record in WS containing:
        EXPECTED: {added: [{className: ..., categoryName: ...", categoryCode: ...,…}],…}
        EXPECTED: * event is subscribed for updates
        """
        pass
