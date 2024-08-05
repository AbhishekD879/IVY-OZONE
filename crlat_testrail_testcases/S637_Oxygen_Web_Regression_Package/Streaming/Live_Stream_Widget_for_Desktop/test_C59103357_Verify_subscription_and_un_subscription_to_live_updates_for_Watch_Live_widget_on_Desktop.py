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
class Test_C59103357_Verify_subscription_and_un_subscription_to_live_updates_for_Watch_Live_widget_on_Desktop(Common):
    """
    TR_ID: C59103357
    NAME: Verify subscription and un-subscription to live updates for Watch Live widget on Desktop
    DESCRIPTION: This test case verifies subscription and un-subscription to live updates for 'Watch Live' widget on Desktop
    PRECONDITIONS: 1. Live Stream widget is enable in CMS > System Configurations > DesktopWidgetsToggle > liveStream = 'enabled'
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. Live Stream is mapped
    PRECONDITIONS: To get information about event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForEvent/xxxx?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: x.xx latest supported SiteServer version
    PRECONDITIONS: xxxx event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: startTime attribute - to see start time of event
    """
    keep_browser_open = True

    def test_001_navigate_to_sport_landing_page__matches_tab_where_live_streaming_is_mapped(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing page > Matches tab where live streaming is mapped
        EXPECTED: * Live Stream widget is present in the Main view column 2
        EXPECTED: * Live Stream widget is expanded
        EXPECTED: * First available event from current <Sport>, that has live streaming mapped, is displayed (see startTime attribute)
        EXPECTED: * In WS verify:
        EXPECTED: "GET_SPORT" request sent with topLevelType: "STREAM_EVENT" 42["IN_PLAY_SPORTS::16::STREAM_EVENT",…] response received
        EXPECTED: "GET_TYPE" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORT_TYPE::16::STREAM_EVENT::",…] response received
        EXPECTED: "subscribe" message sent only for 1 event with livestream available (by start time and display order). Thin should be First available event from current <Sport>
        """
        pass

    def test_002_navigate_to_another_tab_of_this_sport_competitions_inplay_outrights_and_verify_unsubscribe_message(self):
        """
        DESCRIPTION: Navigate to another tab of this <Sport> (Competitions/ Inplay/ Outrights...) and verify "Unsubscribe message"
        EXPECTED: * 'Live Stream widget not displayed
        EXPECTED: * "unsubscribe" message sent for event from 'Live Stream' widget event
        """
        pass

    def test_003_navigate_back_to_matches_tab(self):
        """
        DESCRIPTION: Navigate back to Matches tab
        EXPECTED: In WS verify:
        EXPECTED: *  "GET_SPORT" request sent with topLevelType: "STREAM_EVENT" 42["IN_PLAY_SPORTS::16::STREAM_EVENT",…] response received
        EXPECTED: * "GET_TYPE" request sent with topLevelType: "STREAM_EVENT"
        EXPECTED: 42["IN_PLAY_SPORT_TYPE::16::STREAM_EVENT::",…] response received
        EXPECTED: * "subscribe" message sent only for 1 event with livestream available (by start time and display order). Thin should be First available event from current <Sport>
        """
        pass

    def test_004_navigate_from_current_sport_to_any_other_page_in_the_app(self):
        """
        DESCRIPTION: Navigate from current <Sport> to any other page in the app
        EXPECTED: * 'Live Stream widget not displayed
        EXPECTED: * "unsubscribe" message sent for event from 'Live Stream' widget event
        """
        pass
