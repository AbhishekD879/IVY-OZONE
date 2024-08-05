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
class Test_C1150774_Verify_Price_Odds_button_displaying_on_Event_card_in_the_In_Play_Live_Stream_widget_if_selection_is_not_created_or_is_undisplayed_on_Desktop(Common):
    """
    TR_ID: C1150774
    NAME: Verify 'Price/Odds' button displaying on Event card in the In-Play/Live Stream widget if selection is not created or is undisplayed on Desktop
    DESCRIPTION: This test case verifies 'Price/Odds' button displaying on Event card in the In-Play/Live Stream widget if the selection is not created or is undisplayed on Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: * For checking data get from In-Play MS use the following instruction:
    PRECONDITIONS: 1. Dev Tools->Network->WS
    PRECONDITIONS: 2. Open "IN_PLAY_SPORTS::XX::LIVE_EVENT::XX" response
    PRECONDITIONS: XX - category ID
    PRECONDITIONS: 3. Look at 'eventCount' attribute for every type available in WS for appropriate category
    PRECONDITIONS: * Use the following link for checking attributes of In-Play events: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page_that_contains_live_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events
        EXPECTED: * Sports Landing page is loaded
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Live events are displayed in In-Play widget
        """
        pass

    def test_003_find_or_create_live_event_where_one_of_selection_from_primary_market__ie_match_result_is_not_created_or_its_removed(self):
        """
        DESCRIPTION: Find or create Live event where one of selection from 'Primary Market ' (i.e. 'Match Result') is not created or it's removed
        EXPECTED: * 'Price/Odds' button is displayed without any inscription but has grey color
        EXPECTED: *  'Price/Odds' button is NOT clickable
        EXPECTED: *  'Price/Odds' button doesn't have hover state
        """
        pass

    def test_004_add_missing_selection_to_event_from_step_3_using_ti_tool_and_refresh_the_oxygen_app_to_watch_the_updates(self):
        """
        DESCRIPTION: Add missing selection to event from step 3 using TI tool and refresh the Oxygen app to watch the updates
        EXPECTED: * 'Price/Odds' button is displayed with odds
        EXPECTED: * 'Price/Odds' button is clickable and has hover state
        """
        pass

    def test_005_trigger_the_following_situation_for_selection_of_another_live_eventdisplayed_nand_at_the_same_time_have_in_play_widget_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for selection of another Live event:
        DESCRIPTION: *displayed: "N"*
        DESCRIPTION: and at the same time have In-Play widget opened to watch for updates
        EXPECTED: * [displayed:"N"] attribute is received in WS
        EXPECTED: * Odds inscription disappears from 'Price/Odds' button immediately
        EXPECTED: * 'Price/Odds' button is displayed without any inscription but has grey color
        EXPECTED: *  'Price/Odds' button is NOT clickable
        EXPECTED: *  'Price/Odds' button doesn't have hover state
        """
        pass

    def test_006_trigger_the_following_situation_for_selection_of_live_eventdisplayed_y(self):
        """
        DESCRIPTION: Trigger the following situation for selection of Live event:
        DESCRIPTION: *displayed: "Y"*
        EXPECTED: [displayed:"Y"] attribute is received in WS for particular selection
        """
        pass

    def test_007_refresh_the_page_to_watch_the_updates(self):
        """
        DESCRIPTION: Refresh the page to watch the updates
        EXPECTED: * 'Price/Odds' button is displayed with odds for event from step 5
        EXPECTED: * 'Price/Odds' button is clickable and has hover state
        """
        pass

    def test_008_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: * Betslip counter is increased
        EXPECTED: * 'Price/Odds' button is displayed as selected (with green color)
        """
        pass

    def test_009_repeat_steps_5(self):
        """
        DESCRIPTION: Repeat steps 5
        EXPECTED: * [displayed:"N"] attribute is received in WS
        EXPECTED: * Odds inscription disappears from 'Price/Odds' button immediately
        EXPECTED: * 'Price/Odds' button is displayed without any inscription but has grey color
        EXPECTED: *  'Price/Odds' button is NOT clickable
        EXPECTED: *  'Price/Odds' button doesn't have hover state
        """
        pass

    def test_010_repeat_steps_6_7(self):
        """
        DESCRIPTION: Repeat steps 6-7
        EXPECTED: * 'Price/Odds' button is displayed with odds for event from step 5
        EXPECTED: * 'Price/Odds' button is displayed as selected (with green color)
        EXPECTED: *  'Price/Odds' button is clickable
        """
        pass

    def test_011_open_the_betslip_enter_stake_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Open the Betslip, enter stake and tap "Bet Now" button
        EXPECTED: * The bet is placed successfully
        EXPECTED: * Bet receipt with all information regarding the bet appears in the Betslip
        """
        pass

    def test_012_navigate_to_sports_landing_page_that_contains_live_events_with_mapped_stream(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events with mapped stream
        EXPECTED: * Sports Landing page is loaded
        EXPECTED: * Live Strem widget is displayed in 3-rd column below In-Play widget
        EXPECTED: * Event is displayed in Live Stream widget
        """
        pass

    def test_013_repeat_steps_3_11(self):
        """
        DESCRIPTION: Repeat steps 3-11
        EXPECTED: 
        """
        pass
