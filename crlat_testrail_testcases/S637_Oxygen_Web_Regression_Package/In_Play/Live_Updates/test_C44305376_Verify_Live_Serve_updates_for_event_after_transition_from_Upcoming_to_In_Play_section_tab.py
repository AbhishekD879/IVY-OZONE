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
class Test_C44305376_Verify_Live_Serve_updates_for_event_after_transition_from_Upcoming_to_In_Play_section_tab(Common):
    """
    TR_ID: C44305376
    NAME: Verify Live Serve updates for event after transition from 'Upcoming' to  'In-Play' section/tab
    DESCRIPTION: This case verifies subscription to Live Serve updates for event after transition from 'Upcoming' to  'In-Play' section/tab without refresh
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Navigate to 'In-Play' page from the Sports Menu Ribbon Mobile/Tablet or 'Main Navigation' menu at the 'Universal Header' (**Desktop**) and choose any Sport
    PRECONDITIONS: * Make sure that Live events are present in 'Live Now' section Mobile/Tablet or when 'Live Now' switcher is selected Desktop
    PRECONDITIONS: *To reach upcoming events scroll the page down to 'Upcoming' section Mobile/Tablet or select 'Upcoming' switcher Desktop
    PRECONDITIONS: Note! To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose ?EIO=3&transport=websocket record
    """
    keep_browser_open = True

    def test_001_for_any_upcoming_event_verify_subscription_to_liveserv_updates(self):
        """
        DESCRIPTION: For any Upcoming event verify subscription to LiveServ updates
        EXPECTED: Subscription is present in EIO=3&transport=websocket record
        """
        pass

    def test_002_update_any_marketselection_for_the_event_in_step_1_eg_price_change_suspend(self):
        """
        DESCRIPTION: Update any market/selection for the event in Step 1 (e.g. price change, suspend)
        EXPECTED: Update is received in WS: 42["eventID",{"publishedDate":&lt;date&gt;,"type":&lt;type&gt;
        EXPECTED: * for market: type: "EVMKT"
        EXPECTED: * for event: type: "EVENT"
        EXPECTED: * for selection: type: "SELCN"
        EXPECTED: * for price: type: "PRICE"
        """
        pass

    def test_003_modify_event_to_be_defined_by_attributes_is_off__y_and_event_attribute_isstarted(self):
        """
        DESCRIPTION: Modify event to be defined by attributes is_off = 'Y' and event attribute isStarted
        EXPECTED: * Event disappears from 'Upcoming' section
        EXPECTED: * Event is displayed in 'In-Play' section
        """
        pass

    def test_004_for_the_event_which_transited_from_upcoming_to_in_play_verify_subscription_to_liveserv_updatesnote_event_should_be_visible_in_expanded_section_to_get_liveserv_updates(self):
        """
        DESCRIPTION: For the event which transited from 'Upcoming' to 'In-Play' verify subscription to LiveServ updates
        DESCRIPTION: NOTE: Event should be visible (in expanded section) to get LiveServ updates
        EXPECTED: Subscription is present in EIO=3&transport=websocket record
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: Result is the same
        """
        pass

    def test_006_repeat_steps_1_5_for_the_following_sections_home_page_gt_in_play_tab_mobiletablet_sports_landing_page_gt_in_play_tab_desktop_home_page_for_in_play__live_stream_section_for_both_switchers(self):
        """
        DESCRIPTION: Repeat steps 1-5 for the following sections:
        DESCRIPTION: * Home page &gt; 'In-Play' tab Mobile/Tablet
        DESCRIPTION: * Sports Landing Page &gt; 'In-Play' tab
        DESCRIPTION: * [Desktop] Home page for 'In-play & Live Stream' section for both switchers
        EXPECTED: 
        """
        pass
