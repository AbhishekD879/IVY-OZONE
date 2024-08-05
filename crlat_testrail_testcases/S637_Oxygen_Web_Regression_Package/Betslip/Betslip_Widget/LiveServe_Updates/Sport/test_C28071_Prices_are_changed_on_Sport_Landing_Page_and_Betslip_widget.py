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
class Test_C28071_Prices_are_changed_on_Sport_Landing_Page_and_Betslip_widget(Common):
    """
    TR_ID: C28071
    NAME: Prices are changed on <Sport> Landing Page and Betslip widget
    DESCRIPTION: This test case verifies price changing on <Sport> Landing page and Betslip widget
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-8235 Reflection of live price changes are not shown on Betslip widget
    PRECONDITIONS: LiveServer is available only for **In-Play <Sport> events** with the following attributes:
    PRECONDITIONS: *   drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: *   isMarketBetInRun = "true"
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
        EXPECTED: 
        """
        pass

    def test_003_open_matches_today_tab(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Today**' tab
        EXPECTED: 
        """
        pass

    def test_004_add_selection_to_betslip_from_current_page(self):
        """
        DESCRIPTION: Add selection to Betslip from current page
        EXPECTED: Added selection is displayed in Betslip widget
        """
        pass

    def test_005_trigger_price_change_for_added_on_step_4_selection_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for added on step #4 selection from the current page
        EXPECTED: **[Not actual from OX 99]** Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color:
        EXPECTED: *   blue color if price has decrease
        EXPECTED: *   pink color if price has increased
        EXPECTED: **[Actual from OX 99]** Corresponding 'Price/Odds' button immediately displays new price
        """
        pass

    def test_006_verify_betslip_widget_reflection(self):
        """
        DESCRIPTION: Verify Betslip widget reflection
        EXPECTED: **[Not actual from OX 99]**
        EXPECTED: *   'Price changed from FROM to NEW' is displayed immediately on red background above Betslip widget
        EXPECTED: *   Odds indicator (button) should change value to reflect the updated odds - color remains as active
        EXPECTED: *   'Bet Now' button remains active
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: * the Place bet button text is updated to 'Accept price change'
        EXPECTED: **FOR LADBROKES** the Place bet button text is updated to 'ACCEPT AND PLACE BET'
        """
        pass

    def test_007_open_matches_tomorrow_tab(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Tomorrow**' tab
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps 4-6
        EXPECTED: 
        """
        pass

    def test_009_open_matches_future_tab(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Future**' tab
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps 4-6
        EXPECTED: 
        """
        pass
