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
class Test_C10375627_Verify_Live_Updates_for_subscriptionsevents_not_visible_within_the_active_screen_area(Common):
    """
    TR_ID: C10375627
    NAME: Verify Live Updates for subscriptions(events) not visible within the active screen area
    DESCRIPTION: This test case verifies whether active subscriptions (events within them) receive live updates if they are not visible within the active screen area.
    PRECONDITIONS: 1) Sport #1 should contain: League #1 with up to 6 events; League #2 with 10 or more events.
    PRECONDITIONS: 2) Events from Leagues #1,#2 should have 'Live' and 'Watch Live' markers being set for them within TI
    PRECONDITIONS: 3) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 4) 'virtualScroll' should be checked(enabled) in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 5) 'competitionsCount' should be set to 10 in in CMS > System configuration > Structure > InPlayCompetitionsExpanded
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 6) Load Oxygen app
    PRECONDITIONS: 7) Open/Tap on 'In-Play' tab
    PRECONDITIONS: 8) Expand Sport #1
    PRECONDITIONS: 9) Provide scrolling of page content in a way that subscription is done for both League #1 and League #2(events within them), with a part of events from League #2 not being visible within the active screen area.
    PRECONDITIONS: ![](index.php?/attachments/get/28713)
    """
    keep_browser_open = True

    def test_001_scroll_the_page_down_and_remember_the_event_id_for_the_event_out_of_league_2_that_was_previously_not_seen_within_the_active_screen_area(self):
        """
        DESCRIPTION: Scroll the page down and remember the event ID for the event out of League #2, that was previously not seen within the active screen area
        EXPECTED: Response in WS tab(view) contains an unsubscription from all event(s) within the previously visible League #1;
        EXPECTED: ["unsubscribe", [#######], [#######]]
        """
        pass

    def test_002_scroll_the_page_upto_a_point_where_you_started_the_step_1_and_provide_changesthrough_ti_for_a_selection_of_an_event_from_step_1(self):
        """
        DESCRIPTION: Scroll the page up(to a point where you started the step 1) and provide changes(through TI) for a selection of an event from step 1
        EXPECTED: Response in WS tab(view) contains a subscription to event(s) from a newly appeared league;
        EXPECTED: ["subscribe", [#######, #######]]
        EXPECTED: Response in WS tab(view) contains a following entry regarding the event, where price(selection) change was done:
        EXPECTED: ["#######", {publishedDate: "YYYY-MM-DDTHH:MM:SS.MSE", type: "PRICE",…}]
        """
        pass

    def test_003_scroll_the_page_downto_a_point_where_event_out_of_league_2_is_shown_and_verify_that_changes_that_youve_done_through_the_ti_are_visible_within_the_event_card(self):
        """
        DESCRIPTION: Scroll the page down(to a point where event out of League #2 is shown) and verify that changes that you've done through the TI are visible within the event card.
        EXPECTED: Event card contains up-to-date values(selections)
        """
        pass

    def test_004_repeat_steps_123_on_watch_live_tab_of_the_in_play_page(self):
        """
        DESCRIPTION: Repeat steps 1,2,3 on 'WATCH LIVE' tab of the IN-PLAY page
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_123_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_sectionchanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3 with the previously used Sport/Leagues content being shown in the 'UPCOMING EVENTS' section
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_123_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_section_of_in_play_tab_on_a_homepagechanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3 with the previously used Sport/Leagues content being shown in the 'UPCOMING EVENTS' section of 'In-Play' tab on a Homepage
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass
