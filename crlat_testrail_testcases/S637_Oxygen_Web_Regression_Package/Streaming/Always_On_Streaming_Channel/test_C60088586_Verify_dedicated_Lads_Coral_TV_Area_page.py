import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C60088586_Verify_dedicated_Lads_Coral_TV_Area_page(Common):
    """
    TR_ID: C60088586
    NAME: Verify dedicated Lads/Coral TV Area page
    DESCRIPTION: This test case verifies displaying of dedicated area (meeting/type) where user can view all Events associated with Always On streaming Channel
    PRECONDITIONS: Events with Always On Streaming (Ladbrokes/Coral TV) are available:
    PRECONDITIONS: typeFlagCodes = 'GVA' AND drilldownTagNames = 'EVFLAG_GAO' + LCGSISSWOGH stream is mapped
    """
    keep_browser_open = True

    def test_001_navigate_to_greyhound_landing_pageby_defaultcoral___gh_lp__today_tab__next_races_moduleladbrokes___gh_lp__next_races_tab(self):
        """
        DESCRIPTION: Navigate to Greyhound landing page
        DESCRIPTION: By default:
        DESCRIPTION: Coral - GH LP > Today tab > Next Races module
        DESCRIPTION: Ladbrokes - GH LP > Next Races tab
        EXPECTED: Ladbrokes/Coral TV channel link is displayed at the top of the Next Races module
        EXPECTED: ![](index.php?/attachments/get/122187736)
        EXPECTED: ![](index.php?/attachments/get/122187737)
        """
        pass

    def test_002_tap_on_watch_ladbrokescoral_tv_link(self):
        """
        DESCRIPTION: Tap on Watch (Ladbrokes/Coral) TV link
        EXPECTED: User is redirected to the TV Area page where all the applicable events are grouped together within a Chevron menu
        EXPECTED: ![](index.php?/attachments/get/122256451)
        EXPECTED: ![](index.php?/attachments/get/122256452)
        """
        pass

    def test_003_navigate_back_to_next_races_and_tap_on_see_all_link_on_an_event_that_is_available_for_ladscoral_tv_channel(self):
        """
        DESCRIPTION: Navigate back to Next Races and tap on See All link on an Event that is available for Lads/Coral TV channel
        EXPECTED: User is redirected to the TV Area page where all the applicable events are grouped together within a Chevron menu
        """
        pass

    def test_004_navigate_to_any_epd_which_doesnt_have_always_on_streaming_ladbrokescoral_tv_available_expand_meetings_dropdown_and_tap_on_ladbrokescoral_tv_menuindexphpattachmentsget122187746indexphpattachmentsget122187747(self):
        """
        DESCRIPTION: Navigate to any EPD which DOESN'T have Always On Streaming (Ladbrokes/Coral TV) available, expand meetings dropdown and tap on (Ladbrokes/Coral) TV menu
        DESCRIPTION: ![](index.php?/attachments/get/122187746)
        DESCRIPTION: ![](index.php?/attachments/get/122187747)
        EXPECTED: User is redirected to the TV Area page where all the applicable events are grouped together within a Chevron menu
        """
        pass
