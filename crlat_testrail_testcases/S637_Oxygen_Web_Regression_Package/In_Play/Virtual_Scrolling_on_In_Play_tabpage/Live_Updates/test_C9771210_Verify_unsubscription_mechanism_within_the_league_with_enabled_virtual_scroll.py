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
class Test_C9771210_Verify_unsubscription_mechanism_within_the_league_with_enabled_virtual_scroll(Common):
    """
    TR_ID: C9771210
    NAME: Verify (un)subscription mechanism within the league with enabled virtual scroll
    DESCRIPTION: This test case verifies whether subscription to or unsubscription from events within a league is done once scrolling into/out of its visible header/footer is done on the screen.
    PRECONDITIONS: 1) Sport #1 should contain: League #1 with 10 or more events; League #2 with 10 or more events; League #3 with only 1 event.
    PRECONDITIONS: 2) Events from Leagues #1,#2 and #3 should have 'Live' and 'Watch Live' markers being set for them within TI
    PRECONDITIONS: 3) Leagues #1,#2 and #3 should have lowest disporder in order to be shown at the top of the table(list)
    PRECONDITIONS: 4) Leagues ordering/placement within the Sport should be following: #1, #3, #2
    PRECONDITIONS: 5) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 6) 'virtualScroll' should be checked(enabled) in CMS > System configuration > Structure > Inplay Module
    PRECONDITIONS: 6.1) 'virtualScroll' should be checked(enabled) in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 7) 'competitionsCount' should be set to 1 in in CMS > System configuration > Structure > InPlayCompetitionsExpanded
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 8) Load Oxygen app
    PRECONDITIONS: 9) Open/Tap on 'In-Play' tab
    PRECONDITIONS: 10) Provide scrolling down of content shown within the League #1, till you reach the last event card within it
    """
    keep_browser_open = True

    def test_001_clicktap_on_show_all_sport_button_and_look_for_wssinplay_publisher_response_in_ws_tabview(self):
        """
        DESCRIPTION: Click/Tap on 'SHOW ALL #SPORT button and look for 'wss://inplay-publisher' response in WS tab(view)
        EXPECTED: Additional league is now shown below the first league.
        EXPECTED: Response in WS tab(view) contains a subscription to event(s) from a newly appeared league;
        EXPECTED: ["subscribe", [#######]] or ["subscribe", [#######, #######]]
        EXPECTED: There are no subscriptions to events from other league(s) within the #SPORT, that aren't shown within the visible area of the screen.
        """
        pass

    def test_002_provide_scrolling_down_of_content_shown_on_the_page_till_the_last_event_from_the_first_league_is_not_shownfooter_of_that_event_should_not_be_visible(self):
        """
        DESCRIPTION: Provide scrolling down of content shown on the page, till the last event from the first league is not shown
        DESCRIPTION: (footer of that event should not be visible)
        EXPECTED: Response in WS tab(view) contains an unsubscription from all event(s) within the first league;
        EXPECTED: ["unsubscribe", [#######]]
        """
        pass

    def test_003_provide_scrolling_down_of_content_shown_on_the_page_till_you_reach_the_title_lane_of_new_leagueit_should_be_visible(self):
        """
        DESCRIPTION: Provide scrolling down of content shown on the page, till you reach the title lane of new league
        DESCRIPTION: (it should be visible)
        EXPECTED: Response in WS tab(view) contains a subscription to event(s) from a newly appeared league;
        EXPECTED: ["subscribe", [#######, #######]]
        """
        pass

    def test_004_repeat_steps_123_on_watch_live_tab_of_the_in_play_page(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3 on 'WATCH LIVE' tab of the IN-PLAY page
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_123_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_sectionchanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3 with the previously used Sport/League's content being shown in the 'UPCOMING EVENTS' section
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_123_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_section_of_in_play_tab_on_a_homepagechanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2,3 with the previously used Sport/League's content being shown in the 'UPCOMING EVENTS' section of 'In-Play' tab on a Homepage
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass
