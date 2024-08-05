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
class Test_C28074__NEXT_4_RACES_info_should_be_updated_Suspension_on_Race_Landing_Page_and_Betslip_widget(Common):
    """
    TR_ID: C28074
    NAME: [ NEXT 4 RACES info should be updated]  Suspension on <Race> Landing Page and Betslip widget
    DESCRIPTION: This test case verifies suspension on <Race> Landing page and Betslip widget
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-8235 Reflection of live price changes are not shown on Betslip widget
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next 4 Races' module is not displayed there.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: *   <Race> landing page is opened
        EXPECTED: *   **'Today'** tab with **'By Meeting'** filter  is opened by default
        """
        pass

    def test_003_find_events_in_the_next_4_races_no_matter_what_price_type_it_has_and_add_selection_to_betslip_from_current_page(self):
        """
        DESCRIPTION: Find events in the Next 4 Races (no matter what price type it has)  and add selection to Betslip from current page
        EXPECTED: Added selection is present in Betslip widget
        """
        pass

    def test_004_trigger_suspensionof_current_eventmarketoutcome(self):
        """
        DESCRIPTION: Trigger suspension of current event/market/outcome
        EXPECTED: Price/Odds buttons of this event immediately start displaying "S" and become disabled on <Race> Landing page
        """
        pass

    def test_005_verify_betslip_widget_reflection(self):
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
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_006_trigger_unsuspensionof_current_eventmarketoutcome(self):
        """
        DESCRIPTION: Trigger unsuspension of current event/market/outcome
        EXPECTED: Price/Odds buttons of this event are no more disabled, they become displaying prices immediately
        """
        pass

    def test_007_verify_betslip_widget_reflection(self):
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

    def test_008_selecttodaytabby_time_filter(self):
        """
        DESCRIPTION: Select **'Today'** tab, **'By Time**' filter
        EXPECTED: 'Next 4 Races' module is shown
        """
        pass

    def test_009_repeat_steps__3___8(self):
        """
        DESCRIPTION: Repeat steps # 3 - 8
        EXPECTED: 
        """
        pass
