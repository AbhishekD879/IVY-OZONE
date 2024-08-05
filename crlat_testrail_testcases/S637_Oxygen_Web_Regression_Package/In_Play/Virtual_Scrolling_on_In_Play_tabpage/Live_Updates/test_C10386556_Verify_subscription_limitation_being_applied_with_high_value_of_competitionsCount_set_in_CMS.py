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
class Test_C10386556_Verify_subscription_limitation_being_applied_with_high_value_of_competitionsCount_set_in_CMS(Common):
    """
    TR_ID: C10386556
    NAME: Verify subscription limitation being applied with high value of 'competitionsCount' set in CMS
    DESCRIPTION: This test case verifies whether only leagues with visible header lanes are subscribed under the condition of 'competitionsCount' being set to value, that is higher than the amount of leagues that screen can represent(show) in the active screen area once the Sport is expanded.
    PRECONDITIONS: 1) Sport #1 should contain: League #1 with up to 6 events; League #2 with 10 or more events; League #3 with at least 1 event.
    PRECONDITIONS: 2) Events from Leagues #1,#2 an #3 should have 'Live' and 'Watch Live' markers being set for them within TI
    PRECONDITIONS: 3) 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: 4) 'virtualScroll' should be checked(enabled) in CMS > System configuration > Structure > VirtualScrollConfig
    PRECONDITIONS: 5) 'competitionsCount' should be set to 10 in in CMS > System configuration > Structure > InPlayCompetitionsExpanded
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 6) Load Oxygen app
    PRECONDITIONS: 7) Open/Tap on 'In-Play' tab
    """
    keep_browser_open = True

    def test_001_expand_sport_1(self):
        """
        DESCRIPTION: Expand Sport #1
        EXPECTED: League lanes with event cards become visible under the Sport dropdown lane.
        EXPECTED: Response in WS tab(view) contains:
        EXPECTED: "GET_SPORT" and "GET_TYPE" requests, that were sent and feedback is received for them accordingly ["IN_PLAY_SPORTS::...] and ["IN_PLAY_SPORT_TYPE::...]  ;
        EXPECTED: Subscriptions to events ["subscribe", [#######], [#######],...] from leagues under the expanded sport, lanes of which are visible within the active screen area.
        """
        pass

    def test_002_repeat_step_1_on_watch_live_tab_of_the_in_play_page(self):
        """
        DESCRIPTION: Repeat step 1 on 'WATCH LIVE' tab of the IN-PLAY page
        EXPECTED: 
        """
        pass

    def test_003_repeat_step_1_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_sectionchanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Step 1 with the previously used Sport/Leagues content being shown in the 'UPCOMING EVENTS' section
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass

    def test_004_repeat_step_1_with_the_previously_used_sportleagues_content_being_shown_in_the_upcoming_events_section_of_in_play_tab_on_a_homepagechanges_to_events_you_created_in_pre_conditions_should_be_done_through_the_ti(self):
        """
        DESCRIPTION: Repeat Step 1 with the previously used Sport/Leagues content being shown in the 'UPCOMING EVENTS' section of 'In-Play' tab on a Homepage
        DESCRIPTION: (changes to events you created in pre-conditions should be done through the TI)
        EXPECTED: 
        """
        pass
