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
class Test_C28075_NEED_TO_BE_UPDATED_Prices_are_changed_on_Race_Landing_Page_and_Betslip_widget(Common):
    """
    TR_ID: C28075
    NAME: [NEED TO BE UPDATED] Prices are changed on <Race> Landing Page and Betslip widget
    DESCRIPTION: This test case verifies price changing on <Race> Landing page and Betslip widget
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-8235 Reflection of live price changes are not shown on Betslip widget
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/YYYYY?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet SiteServer*
    PRECONDITIONS: *   *YYYYYYY- event id*
    PRECONDITIONS: *   *LL - language (e.g. en, ukr) *
    PRECONDITIONS: See attributes on market level to define price types for event:
    PRECONDITIONS: **'priceTypeCodes' **= 'LP'
    PRECONDITIONS: **'priceTypeCodes'** = 'LP, SP'
    PRECONDITIONS: Notice, Price updates on <Race> Landing Page is possible ONLY for 'Today' tab on 'Next 4 Races' module.
    PRECONDITIONS: For the rest tabs: 'Tomorrow' and 'Future' -> 'Next 4 Races' module is not displayed there.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
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

    def test_003_in_the_next_4_races_module_find_and_add_to_betslip_an_event_withpricetypecodes_lp(self):
        """
        DESCRIPTION: In the 'Next 4 Races' module find and add to Betslip an event with **'priceTypeCodes'**= 'LP'
        EXPECTED: Added selection is displayed in Betslip widget
        """
        pass

    def test_004_trigger_price_change_for_added_on_step_4_selection_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for added on step #4 selection from the current page
        EXPECTED: **[Not actual from OX 99]** Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its color:
        EXPECTED: blue color if price has decrease
        EXPECTED: pink color if price has increased
        EXPECTED: **[Actual from OX 99]** Corresponding 'Price/Odds' button immediately displays new price
        """
        pass

    def test_005_verify_betslip_widget_reflection(self):
        """
        DESCRIPTION: Verify Betslip widget reflection
        EXPECTED: **[Not actual from OX 99]**
        EXPECTED: * 'Price changed from FROM to NEW' is displayed immediately on red background above Betslip widget
        EXPECTED: * Odds indicator (button) should change value to reflect the updated odds - color remains as active
        EXPECTED: * 'Bet Now' button remains active
        EXPECTED: **[Actual from OX 99]**
        EXPECTED: * the selection price change is displayed via push: 'Price changed from from x to y'
        EXPECTED: * Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        EXPECTED: *info message is displayed at the top of the betslip with animations - this is removed after 5 seconds: 'Some of the prices have changed'
        EXPECTED: * the Place bet button text is updated to 'Accept price change'
        EXPECTED: ** Ladbrokes**: Place bet button is inactive - until user enters a stake. If price change notification is shown and then user enters stake, Place bet button should become active.
        """
        pass

    def test_006_in_the_next_4_races_module_find_an_event_withpricetypecodes_lpsp_and_repeat_steps_4_5(self):
        """
        DESCRIPTION: In the 'Next 4 Races' module find an event with** 'priceTypeCodes' **= 'LP,SP' and repeat steps #4-5
        EXPECTED: 
        """
        pass

    def test_007_selecttodaytabby_time_filter(self):
        """
        DESCRIPTION: Select **'Today'** tab, **'By Time**' filter
        EXPECTED: 'Next 4 Races' module is shown
        """
        pass

    def test_008_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps #3-6
        EXPECTED: 
        """
        pass
