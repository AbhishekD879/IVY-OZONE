import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C60098438_Verify_redirection_to_the_Racing_TV_area_by_clicking_on_See_All_option(Common):
    """
    TR_ID: C60098438
    NAME: Verify redirection to the Racing TV area by clicking on See All option
    DESCRIPTION: This test case verifies redirection to the Racing TV area by clicking on See All option
    PRECONDITIONS: Always On Streaming (Ladbrokes/Coral TV) event(s) are available:
    PRECONDITIONS: typeFlagCodes = 'GVA' AND drilldownTagNames = 'EVFLAG_GAO' + LCGSISSWOGH stream is mapped
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhound_landing_page_and_check_events_within_next_races_available_for_the_always_on_streaming_channelby_defaultcoral___gh_lp__today_tab__next_races_moduleladbrokes___gh_lp__next_races_tab(self):
        """
        DESCRIPTION: Navigate to Greyhound landing page and check events within Next Races available for the Always On Streaming Channel
        DESCRIPTION: By default:
        DESCRIPTION: Coral - GH LP > Today tab > Next Races module
        DESCRIPTION: Ladbrokes - GH LP > Next Races tab
        EXPECTED: Signposting icon is displayed next to event(s) name
        EXPECTED: ![](index.php?/attachments/get/122186912) ![](index.php?/attachments/get/122186913)
        """
        pass

    def test_002_click_on_see_all_ladbrokes__full_race_card_coral_option_on_an_event_that_is_available_for_ladscoral_tv_channel(self):
        """
        DESCRIPTION: Click on See All (Ladbrokes) / Full Race Card (Coral) option on an Event that is available for Lads/Coral TV channel
        EXPECTED: User is navigated to the TV area where all the applicable events are grouped together within a chevron menu
        """
        pass
