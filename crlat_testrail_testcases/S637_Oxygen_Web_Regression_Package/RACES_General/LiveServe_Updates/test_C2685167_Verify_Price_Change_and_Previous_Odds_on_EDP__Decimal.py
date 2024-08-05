import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C2685167_Verify_Price_Change_and_Previous_Odds_on_EDP__Decimal(Common):
    """
    TR_ID: C2685167
    NAME: Verify Price Change and Previous Odds on EDP - Decimal
    DESCRIPTION: This test case verify displaying of Previous odds under Price/Odds button
    PRECONDITIONS: **Updates are received in push notifications**
    PRECONDITIONS: To retrieve an information from Site Server about Previous Odds use link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZZZ?simpleFilter=event.suspendAtTime:greaterThan:####-##-##T##:##:##.###Z&racingForm=outcome&racingForm=event&priceHistory=true&prune=event&prune=market&translationLang=en
    PRECONDITIONS: *X.XX* - current supported version of OpenBet release
    PRECONDITIONS: *ZZZZZZ* - an event id
    PRECONDITIONS: *####-##-##T##:##:##.###Z* - date and time until event won't be suspended
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
        EXPECTED: * <Race> landing page is opened
        EXPECTED: * 'Today' tab is opened
        """
        pass

    def test_003_go_to_the_event_details_page_with_live_price_available(self):
        """
        DESCRIPTION: Go to the event details page with 'Live Price' available
        EXPECTED: * Event details page is opened
        """
        pass

    def test_004_trigger_price_changing_for_some_outcome_and_check_previous_odds(self):
        """
        DESCRIPTION: Trigger price changing for some outcome and check Previous Odds
        EXPECTED: * 'Price/Odds' button immediately displays new price
        EXPECTED: * Previous price/odd is displayed under Price/odds button immediately
        EXPECTED: * Previous price/odd is displayed in decimal format
        """
        pass

    def test_005_repeat_step_4_several_times_and_check_previous_odds(self):
        """
        DESCRIPTION: Repeat step №4 several times and check Previous Odds
        EXPECTED: * Previous Odds are updated successfully each time
        EXPECTED: * Only 2 last Previous Odds are displayed in format X/X>X/X (older one goes first)
        """
        pass

    def test_006_verify_previous_odds_correctness(self):
        """
        DESCRIPTION: Verify Previous Odds correctness
        EXPECTED: *  Previous Odds correspond to **'livePriceDec'** attributes from tag *<historicPrice .../>*  in decimal format
        EXPECTED: * Previous odds are ordered according to **'displayOrder'** attribute (the biggest - the last)
        """
        pass

    def test_007_verify_previous_odds_price_changes_for_inactive_market_tab(self):
        """
        DESCRIPTION: Verify Previous Odds price changes for inactive market tab
        EXPECTED: If market tab is inactive and price was changed, after navigating to this tab - updated Previous Odds will be shown there
        """
        pass

    def test_008_verify_previous_odd_are_displayed_for_inactive_selection(self):
        """
        DESCRIPTION: Verify Previous Odd are displayed for inactive selection
        EXPECTED: * Price/Odds button is grayed out
        EXPECTED: * Previous Odds are displayed
        """
        pass
