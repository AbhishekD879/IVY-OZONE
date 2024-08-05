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
class Test_C9771291_Verify_limitation_on_Live_Updates_reception_with_enabled_virtual_scrolling(Common):
    """
    TR_ID: C9771291
    NAME: Verify limitation on Live Updates reception with enabled virtual scrolling
    DESCRIPTION: This test case verifies whether only events within the currently active subscriptions receive live updates when virtual scrolling functionality is enabled for IN-PLAY.
    PRECONDITIONS: 1) Sport #1 should contain: League #1 with 10 or more events; League #2 with 10 or more events.
    PRECONDITIONS: 2) Events from Leagues #1 and #2 should have 'Live' and 'Watch Live' markers being set for them within TI
    PRECONDITIONS: 3) Leagues #1 and #2 should have lowest *disporder* in order to be shown at the top of the table(list)
    PRECONDITIONS: 4) Leagues ordering/placement within the Sport should be following: #1, #2
    PRECONDITIONS: 5) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 6) Virtual Scroll should be enabled in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 7) System configuration > Structure > 'InPlayCompetitionsExpanded' should be set to 1
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 8) Load Oxygen app
    PRECONDITIONS: 9) Open/Tap on 'In-Play' tab
    PRECONDITIONS: 10) Provide scrolling down of content shown within the League #1, till you reach the last event card within it and click 'SHOW ALL #SPORT' button
    PRECONDITIONS: ![](index.php?/attachments/get/28710)
    """
    keep_browser_open = True

    def test_001_provide_changesthrough_ti_for_a_selection_of_a_visible_event_within_the_league_that_is_currently_is_subscribed(self):
        """
        DESCRIPTION: Provide changes(through TI) for a selection of a visible event within the league that is currently is subscribed.
        EXPECTED: Changing of values is visible within the event card.
        EXPECTED: Response in WS tab(view) contains a following entry regarding the event, where price(selection) change was done:
        EXPECTED: ["#######", {publishedDate: "YYYY-MM-DDTHH:MM:SS.MSE", type: "PRICE",…}]
        """
        pass

    def test_002_scroll_the_page_down_and_remember_the_event_id_for_the_event_out_of_other_league2nd_league(self):
        """
        DESCRIPTION: Scroll the page down and remember the event ID for the event out of other League(2nd League)
        EXPECTED: Response in WS tab(view) contains a subscription to event(s) from a newly appeared league;
        EXPECTED: ["subscribe", [#######, #######]]
        """
        pass

    def test_003_scroll_the_page_upto_a_point_of_view_for_the_step_1_and_provide_changesthrough_ti_for_a_selection_of_an_event_from_step_2(self):
        """
        DESCRIPTION: Scroll the page up(to a point of view for the step 1) and provide changes(through TI) for a selection of an event from step 2
        EXPECTED: Response in WS tab(view) contains an unsubscription from all event(s) within the previously visible(second) league;
        EXPECTED: ["unsubscribe", [#######], [#######]]
        EXPECTED: No additional response regarding event changes(of edited event) is shown.
        """
        pass

    def test_004_scroll_the_page_down_back_to_the_event_card_from_step_2(self):
        """
        DESCRIPTION: Scroll the page down back to the event card from step 2
        EXPECTED: Values of the selection correspond to those, set through the TI.
        EXPECTED: Response in WS tab(view) contains a subscription to event(s) from a newly appeared league;
        EXPECTED: ["subscribe", [#######, #######]]
        EXPECTED: Additional entry regarding the event, where price(selection) change was done is shown below the subscription response:
        EXPECTED: ["#######", {publishedDate: "YYYY-MM-DDTHH:MM:SS.MSE", type: "PRICE",…}]
        """
        pass

    def test_005_repeat_steps_1234_on_watch_live_tab_of_the_in_play_page(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3,4 on 'WATCH LIVE' tab of the IN-PLAY page
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1234_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_sectionchanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3,4 with the previously used Sport/League's content being shown in the 'UPCOMING EVENTS' section
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass

    def test_007_repeat_steps_1234_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_section_of_in_play_tab_on_a_homepagechanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3,4 with the previously used Sport/League's content being shown in the 'UPCOMING EVENTS' section of 'In-Play' tab on a Homepage
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass
