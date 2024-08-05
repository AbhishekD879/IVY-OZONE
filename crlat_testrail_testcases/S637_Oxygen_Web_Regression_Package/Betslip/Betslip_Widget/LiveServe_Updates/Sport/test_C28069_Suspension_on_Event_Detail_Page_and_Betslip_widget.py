import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C28069_Suspension_on_Event_Detail_Page_and_Betslip_widget(Common):
    """
    TR_ID: C28069
    NAME: Suspension on Event Detail Page and Betslip widget
    DESCRIPTION: This test case verifies suspension on Event Detail page and Betslip widget
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-8235 Reflection of live price changes are not shown on Betslip widget
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE:** **LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_open_matches_today_tab(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Today**' tab
        EXPECTED: 
        """
        pass

    def test_004_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details page
        EXPECTED: 
        """
        pass

    def test_005_add_selection_to_betslip_from_current_page(self):
        """
        DESCRIPTION: Add selection to Betslip from current page
        EXPECTED: Added selection is displayed in Betslip widget
        """
        pass

    def test_006_trigger_suspensionof_current_eventmarketoutcome(self):
        """
        DESCRIPTION: Trigger suspension of current event/market/outcome
        EXPECTED: Price/Odds buttons of this event immediately start displaying "S" and become disabled on <Sport> Landing page
        """
        pass

    def test_007_verify_betslip_widget_reflection(self):
        """
        DESCRIPTION: Verify Betslip widget reflection
        EXPECTED: **Before OX99**
        EXPECTED: *   Error messages 'The Outcome/Market/Event Has Been Suspended' (depends on what comes in response from server) are shown in above corresponding singles immediately
        EXPECTED: *   'Stake' field , 'Odds' and 'Estimated returns'  - are disabled and greyed out for corresponding singles
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Warning message 'Please beware that # of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **From OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_008_trigger_unsuspensionof_current_eventmarketoutcome(self):
        """
        DESCRIPTION: Trigger unsuspension of current event/market/outcome
        EXPECTED: Price/Odds buttons of this event are no more disabled, they become displaying prices immediately
        """
        pass

    def test_009_verify_betslip_widget_reflection(self):
        """
        DESCRIPTION: Verify Betslip widget reflection
        EXPECTED: **Before OX99**
        EXPECTED: *   Error messages 'The Outcome/Market/Event Has Been Suspended' (depends on what comes in response from server) disappear above corresponding singles immediately
        EXPECTED: *   'Stake' field , 'Odds' and 'Estimated returns'  - are enabled and not greyed out for corresponding singles
        EXPECTED: * Error message 'Please beware that x of your selections has been suspended' disappears above disabled 'Bet Now' (or 'Log In and Bet') button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        pass

    def test_010_open_matches_tomorrow_tab(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Tomorrow**' tab
        EXPECTED: 
        """
        pass

    def test_011_repeat_steps_4_9(self):
        """
        DESCRIPTION: Repeat steps 4-9
        EXPECTED: 
        """
        pass

    def test_012_open_matches_future_tab(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Future**' tab
        EXPECTED: 
        """
        pass

    def test_013_repeat_steps_4_9(self):
        """
        DESCRIPTION: Repeat steps 4-9
        EXPECTED: 
        """
        pass
