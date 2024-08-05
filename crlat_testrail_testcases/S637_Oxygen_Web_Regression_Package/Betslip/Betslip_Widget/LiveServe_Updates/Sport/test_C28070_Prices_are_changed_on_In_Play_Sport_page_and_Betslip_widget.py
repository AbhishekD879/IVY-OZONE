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
class Test_C28070_Prices_are_changed_on_In_Play_Sport_page_and_Betslip_widget(Common):
    """
    TR_ID: C28070
    NAME: Prices are changed on In Play <Sport> page and Betslip widget
    DESCRIPTION: This test case verifies price changing on In Play <Sport> page and Betslip widget
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-8235 Reflection of live price changes are not shown on Betslip widget
    PRECONDITIONS: LiveServer is available only for In-Play <Sport> events with the following attributes:
    PRECONDITIONS: *   drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: *   isMarketBetInRun = "true"
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: **NOTE:** **LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_live_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap '**LIVE**' icon from the sports ribbon
        EXPECTED: 'In-Play' Landing page is opened
        """
        pass

    def test_003_tap_sport_icon_from_live_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from live sports ribbon
        EXPECTED: <Sport> In-Play page is opened
        """
        pass

    def test_004_choose_live_now_sorting_type(self):
        """
        DESCRIPTION: Choose '**Live Now**' sorting type
        EXPECTED: 
        """
        pass

    def test_005_add_selection_to_betslip_from_current_page(self):
        """
        DESCRIPTION: Add selection to Betslip from current page
        EXPECTED: Added selection is displayed in Betslip widget
        """
        pass

    def test_006_trigger_price_change_for_added_on_step_5_selection_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for added on step #5 selection from the current page
        EXPECTED: **[Not actual from OX 99]** Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color:
        EXPECTED: *   blue color if price has decrease
        EXPECTED: *   pink color if price has increased
        EXPECTED: **[Actual from OX 99]** Corresponding 'Price/Odds' button immediately displays new price
        """
        pass

    def test_007_verify_betslip_widget_reflection(self):
        """
        DESCRIPTION: Verify Betslip widget reflection
        EXPECTED: **[Not actual from OX 99]**
        EXPECTED: *   'Price changed from FROM to NEW' is displayed immediately on red background above Betslip widget
        EXPECTED: *   Odds indicator (button) should change value to reflect the updated odds - color remains as active
        EXPECTED: *   'Bet Now' button remains active
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: *the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: *info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: * the Place bet button text is updated to 'Accept price change'
        """
        pass

    def test_008_choose_upcoming_sorting_type(self):
        """
        DESCRIPTION: Choose '**Upcoming**' sorting type
        EXPECTED: 
        """
        pass

    def test_009_repeat_steps_7_8(self):
        """
        DESCRIPTION: Repeat steps #7-8
        EXPECTED: 
        """
        pass

    def test_010_navigate_back_to_the_homepage(self):
        """
        DESCRIPTION: Navigate back to the Homepage
        EXPECTED: 
        """
        pass

    def test_011_select_sporticon_from_sports_ribbon(self):
        """
        DESCRIPTION: Select <Sport> icon from sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_012_select_in_play_tab_and_repeat_steps_4_9(self):
        """
        DESCRIPTION: Select In-Play tab and repeat steps #4-9
        EXPECTED: 
        """
        pass

    def test_013_navigate_back_to_the_homepage(self):
        """
        DESCRIPTION: Navigate back to the Homepage
        EXPECTED: 
        """
        pass

    def test_014_open_in_play_taband_repeat_steps_4_9(self):
        """
        DESCRIPTION: Open 'In-Play' tab and repeat steps #4-9
        EXPECTED: 
        """
        pass
