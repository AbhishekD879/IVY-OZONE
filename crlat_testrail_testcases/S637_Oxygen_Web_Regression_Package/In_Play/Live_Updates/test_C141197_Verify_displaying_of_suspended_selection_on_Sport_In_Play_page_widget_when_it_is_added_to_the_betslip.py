import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C141197_Verify_displaying_of_suspended_selection_on_Sport_In_Play_page_widget_when_it_is_added_to_the_betslip(Common):
    """
    TR_ID: C141197
    NAME: Verify displaying of suspended selection on <Sport> In-Play page/widget when it is added to the betslip
    DESCRIPTION: This test case verifies displaying of suspended selection on <Sport> In-Play page/widget when it is added to the betslip
    PRECONDITIONS: - LiveServer is available only for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: - To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: - To verify suspension check new received value in "status" attribute using Dev Tools-> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection
    PRECONDITIONS: *NOTE:* *pushes with LiveServe updates also are received if selection is added to the betslip*
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: Navigate to Sports Landing page from Sports Ribbon/Left Navigation menu
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_open_in_play_page_for_particular_sport(self):
        """
        DESCRIPTION: Open 'In-Play' page for particular Sport
        EXPECTED: 'In-Play' page is opened
        """
        pass

    def test_004_verify_the_priceodds_buttons_view_of_the_events_displayed(self):
        """
        DESCRIPTION: Verify the 'Price/Odds' buttons view of the events displayed
        EXPECTED: 'Price/Odds' buttons display price received from backend on light grey background
        """
        pass

    def test_005_clicktap_on_priceodds_button_and_check_its_displaying(self):
        """
        DESCRIPTION: Click/Tap on Price/Odds button and check it's displaying
        EXPECTED: Selected Price/Odds button is marked as added to Betslip (Becomes green)
        """
        pass

    def test_006_verify_that_selection_is_added_to_bet_slip(self):
        """
        DESCRIPTION: Verify that selection is added to Bet Slip
        EXPECTED: Selection is present in Bet Slip and counter is increased on header
        """
        pass

    def test_007_trigger_the_following_situation_for_this_outcomeoutcomestatuscode__sand_at_the_same_time_have_sport_in_play_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for this outcome:
        DESCRIPTION: outcomeStatusCode = 'S'
        DESCRIPTION: and at the same time have <Sport> In-Play page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_008_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for selected outcome is displayed immediately as greyed out and become disabled on <Sport> In-Play page
        EXPECTED: * Price is still displaying on the Price/Odds button
        EXPECTED: * Price/Odds button is not marked as added to Betslip (is not green anymore)
        """
        pass

    def test_009_change_attribute_for_this_outcomeoutcomestatuscode__aand_at_the_same_time_have_sport_in_play_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Change attribute for this outcome:
        DESCRIPTION: outcomeStatusCode = 'A'
        DESCRIPTION: and at the same time have <Sport> In-Play page opened to watch for updates
        EXPECTED: 
        """
        pass

    def test_010_verify_outcome_for_the_event(self):
        """
        DESCRIPTION: Verify outcome for the event
        EXPECTED: * Price/Odds button for selected outcome is no more disabled, it becomes active immediately
        EXPECTED: * Price/Odds button is marked as added to Betslip (Becomes green)
        """
        pass

    def test_011_for_desktopnavigate_to_sports_landing_page_make_sure_that_sport_has_available_live_events_from_sports_ribbonleft_navigation_menu(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to Sports Landing page (make sure that Sport has available live events) from Sports Ribbon/Left Navigation menu
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: * In-Play widget with available live events for particular Sport is displayed in 3-rd Service column
        """
        pass

    def test_012_for_desktoprepeat_steps_4_10(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 4-10
        EXPECTED: 
        """
        pass
