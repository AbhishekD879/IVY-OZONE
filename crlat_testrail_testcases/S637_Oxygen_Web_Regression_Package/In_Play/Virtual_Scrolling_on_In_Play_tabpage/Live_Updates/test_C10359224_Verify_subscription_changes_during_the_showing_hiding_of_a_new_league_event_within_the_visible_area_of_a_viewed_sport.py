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
class Test_C10359224_Verify_subscription_changes_during_the_showing_hiding_of_a_new_league_event_within_the_visible_area_of_a_viewed_sport(Common):
    """
    TR_ID: C10359224
    NAME: Verify subscription changes during the showing/hiding of a new league/event within the visible area of a viewed sport
    DESCRIPTION: This test case verifies whether the previously shown and subscribed league becomes hidden and it's subscription being revoked by adding a new league within a visible range of a viewed sport, and vice versa.
    PRECONDITIONS: 1) Sport #1 should contain League #1 with up to 3 events; Sport #2 should contain League #2 with 10 or more events.
    PRECONDITIONS: 2) Sport #1 should contain no more than 2 leagues with visible space between Sport #2 and last event from Sport #1
    PRECONDITIONS: 3) Events from Leagues #1,#2 should have 'Live' and 'Watch Live' markers being set for them within TI
    PRECONDITIONS: 4) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 5) 'virtualScroll' should be checked(enabled) in CMS > System configuration > Structure > Inplay Module
    PRECONDITIONS: 6) 'competitionsCount' should be set to 10 in in CMS > System configuration > Structure > InPlayCompetitionsExpanded
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 7) Load Oxygen app
    PRECONDITIONS: 8) Open/Tap on 'In-Play' tab
    PRECONDITIONS: 9) Expand Sports #1 and #2
    PRECONDITIONS: 10) Provide scrolling of page content in a way that League #1 from Sport #1 is visible at the top of the screen and the header of a League #2 from Sport #2 is visible at the bottom of the screen with subscriptions to events from both leagues being present in WS Response: ["subscribe", [#######]])
    PRECONDITIONS: ![](index.php?/attachments/get/28703)
    """
    keep_browser_open = True

    def test_001_adddisplay_events_for_appearing_the_new_league_3through_ti_within_the_sport_1_and_1_event_within_it_that_has_live_and_watch_live_markers_set(self):
        """
        DESCRIPTION: Add/display events for appearing the new League #3(through TI) within the Sport #1 and 1 event within it that has 'Live' and 'Watch Live' markers set.
        EXPECTED: New League lane(#3) appears within the visible area of the viewed Sport(at its bottom) with a new event card being shown under it.
        EXPECTED: Response in WS tab(view) contains a subscription to event from a newly appeared league;
        EXPECTED: ["subscribe", [#######]]
        EXPECTED: Lane of a League #2 is no longer shown within the visible area of the screen.
        EXPECTED: Response in WS tab(view) contains an unsubscription from all events within the previously visible league(#2);
        EXPECTED: ["unsubscribe", [#######], [#######],...]
        """
        pass

    def test_002_undisplay_the_event_from_league_3through_ti(self):
        """
        DESCRIPTION: Undisplay the event from League #3(through TI)
        EXPECTED: Lane of a League #3 and its event card are no longer shown within the visible area of the screen.
        EXPECTED: Response in WS tab(view) contains an unsubscription from event within the previously visible league(#3);
        EXPECTED: ["unsubscribe", [#######]]
        EXPECTED: Lane of a League #2 becomes shown within the visible area of the screen(at its bottom).
        EXPECTED: Response in WS tab(view) contains an subscription to all events within the league(#2);
        EXPECTED: ["subscribe", [#######], [#######],...]
        """
        pass

    def test_003_repeat_steps_12_on_watch_live_tab_of_the_in_play_page(self):
        """
        DESCRIPTION: Repeat Steps 1,2 on 'WATCH LIVE' tab of the IN-PLAY page
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps_12_with_the_previously_used_sportsleagues_content_being_shown_in_the_upcoming_events_sectionchanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2 with the previously used Sports/Leagues content being shown in the 'UPCOMING EVENTS' section
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_12_with_the_previously_used_sportsleagues_content_being_shown_in_the_upcoming_events_section_of_in_play_tab_on_a_homepagechanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2 with the previously used Sports/Leagues content being shown in the 'UPCOMING EVENTS' section of 'In-Play' tab on a Homepage
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass
