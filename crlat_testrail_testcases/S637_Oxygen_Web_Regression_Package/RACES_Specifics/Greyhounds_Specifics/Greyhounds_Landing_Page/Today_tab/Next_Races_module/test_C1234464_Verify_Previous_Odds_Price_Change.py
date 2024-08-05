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
class Test_C1234464_Verify_Previous_Odds_Price_Change(Common):
    """
    TR_ID: C1234464
    NAME: Verify Previous Odds Price Change
    DESCRIPTION: This test case verify displaying of Previous odds under Price/Odds button for Greyhounds
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
        EXPECTED: --
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: * <Race> landing page is opened
        EXPECTED: * **Today** tab is opened,  **By Meeting** filter
        EXPECTED: * 'Next 4 Races' is shown
        """
        pass

    def test_003_in_the_next_4_races_module_find_event_with_live_price_available(self):
        """
        DESCRIPTION: In the 'Next 4 Races' module find event with 'Live Price' available
        EXPECTED: Event is shown
        """
        pass

    def test_004_trigger_price_changing_for_some_outcome_and_check_previous_odds(self):
        """
        DESCRIPTION: Trigger price changing for some outcome and check Previous Odds
        EXPECTED: * 'Price/Odds' button immediately displays new price
        EXPECTED: * Previous price/odd is displayed under Price/odds button immediately
        EXPECTED: * Previous price/odd is displayed in decimal or fractional format (depends upon the users chosen odds display preference)
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
        EXPECTED: * Previous Odds correspond to **livePriceNum** and **livePriceDen** attributes from tag *<historicPrice .../>*  in fractional format
        EXPECTED: *  Previous Odds correspond to **'livePriceDec'** attributes from tag *<historicPrice .../>*  in decimal format
        EXPECTED: * Previous odds are ordered according to **'displayOrder'** attribute (the biggest - the last)
        """
        pass
