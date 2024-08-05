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
class Test_C10364700_Verify_subscription_changes_during_the_decrease_of_events_number_within_a_league_with_many_events(Common):
    """
    TR_ID: C10364700
    NAME: Verify subscription changes during the decrease of events number within a league with many events
    DESCRIPTION: This test case verifies whether a subscription to a league is done once it becomes visible as a result of events undisplaying from another league, shown above it.
    PRECONDITIONS: 1) Sport #1 should contain League #1 with up to 6 events; Sport #2 should contain League #2 with 10 or more events.
    PRECONDITIONS: 2) Sport #1 should contain no more than 2 leagues and occupy the entire visible space of the screen, with a League #2 being present below the visible screen space.
    PRECONDITIONS: 3) Events from Leagues #1,#2 should have 'Live' and 'Watch Live' markers being set for them within TI
    PRECONDITIONS: 4) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 5) 'virtualScroll' should be checked(enabled) in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 6) 'competitionsCount' should be set to 10 in in CMS > System configuration > Structure > InPlayCompetitionsExpanded
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 7) Load Oxygen app
    PRECONDITIONS: 8) Open/Tap on 'In-Play' tab
    PRECONDITIONS: 9) Expand Sports #1 and #2
    PRECONDITIONS: 10) Provide scrolling of page content in a way that League #1 from Sport #1 is visible at the top of the screen(with subscriptions to its event(s) being present in WS Response: ["subscribe", [#######],...]) and League #2 from Sport #2 is not visible, but is present below visible edge of the bottom of active screen area(without subscriptions to its events being present in WS Response)
    PRECONDITIONS: ![](index.php?/attachments/get/28711)
    """
    keep_browser_open = True

    def test_001_undisplay_1_event_from_league_1through_ti(self):
        """
        DESCRIPTION: Undisplay 1 event from League #1(through TI)
        EXPECTED: Event card of the undisplayed event disappears from the League #1.
        EXPECTED: Response in WS tab(view) contains an unsubscription from the event;
        EXPECTED: ["unsubscribe", [#######]]
        EXPECTED: Lane of a League #2 becomes shown within the visible area of the screen(at its bottom).
        EXPECTED: Response in WS tab(view) contains an subscription to all events within the league(#2);
        EXPECTED: ["subscribe", [#######], [#######],...]
        """
        pass

    def test_002_display_event_from_step_1through_ti_and_refresh_the_coralladbrokes_currently_opened_page(self):
        """
        DESCRIPTION: Display event from Step 1(through TI) and refresh the Coral/Ladbrokes currently opened page
        EXPECTED: 
        """
        pass

    def test_003_repeat_step_1_on_watch_live_tab_of_the_in_play_page(self):
        """
        DESCRIPTION: Repeat step 1 on 'WATCH LIVE' tab of the IN-PLAY page
        EXPECTED: 
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat Step 2
        EXPECTED: 
        """
        pass

    def test_005_repeat_steps_12_with_the_previously_used_sportsleagues_content_being_shown_in_the_upcoming_events_sectionchanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1,2 with the previously used Sports/Leagues content being shown in the 'UPCOMING EVENTS' section
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass

    def test_006_repeat_steps_1_with_the_previously_used_sportsleagues_content_being_shown_in_the_upcoming_events_section_of_in_play_tab_on_a_homepagechanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Steps 1 with the previously used Sports/Leagues content being shown in the 'UPCOMING EVENTS' section of 'In-Play' tab on a Homepage
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass
