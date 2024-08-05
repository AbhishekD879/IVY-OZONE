import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C236728_Verify_Price_Change_and_Previous_Odds_on_EDP__Fractional(Common):
    """
    TR_ID: C236728
    NAME: Verify Price Change and Previous Odds on EDP - Fractional
    DESCRIPTION: This test case verify displaying of Previous odds under Price/Odds button for Fractional Format
    PRECONDITIONS: **Updates are received in push notifications**
    PRECONDITIONS: Fractional format is enabled
    PRECONDITIONS: There is a <Race> with LP prices
    PRECONDITIONS: To retrieve an information from Site Server about Previous Odds use link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZZZ?simpleFilter=event.suspendAtTime:greaterThan:####-##-##T##:##:##.###Z&racingForm=outcome&racingForm=event&priceHistory=true&prune=event&prune=market&translationLang=en
    PRECONDITIONS: *X.XX* - current supported version of OpenBet release
    PRECONDITIONS: *ZZZZZZ* - an event id
    PRECONDITIONS: *####-##-##T##:##:##.###Z* - date and time until event won't be suspended
    """
    keep_browser_open = True

    def test_001_open_race_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        EXPECTED: 
        """
        pass

    def test_002_trigger_price_changing_for_some_outcome_and_check_previous_odds(self):
        """
        DESCRIPTION: Trigger price changing for some outcome and check Previous Odds
        EXPECTED: * 'Price/Odds' button immediately displays new price
        EXPECTED: * Previous price/odd is displayed under Price/odds button immediately
        """
        pass

    def test_003_repeat_step_2_several_times_and_check_previous_odds(self):
        """
        DESCRIPTION: Repeat step №2 several times and check Previous Odds
        EXPECTED: * New Odds are displayed correctly
        EXPECTED: * Previous Odds are updated successfully each time
        EXPECTED: * Only 2 last Previous Odds are displayed in format X/X>X/X (older one goes first)
        """
        pass

    def test_004_verify_previous_odds_correctness(self):
        """
        DESCRIPTION: Verify Previous Odds correctness
        EXPECTED: * Previous Odds correspond to **livePriceNum** and **livePriceDen** attributes from tag *<historicPrice .../>*
        EXPECTED: * Previous odds are ordered according to **'displayOrder'** attribute (the biggest - the last)
        """
        pass

    def test_005_trigger_price_changing_for_some_outcome_from_market_tab_which_is_not_active_at_the_moment(self):
        """
        DESCRIPTION: Trigger price changing for some outcome from Market tab which is not active at the moment
        EXPECTED: 
        """
        pass

    def test_006_open_this_market(self):
        """
        DESCRIPTION: Open this Market
        EXPECTED: *  'Price/Odds' button displays new price
        EXPECTED: *  Updated Previous Odds are displayed there as well
        """
        pass

    def test_007_suspend_one_outcome_and_then_trigger_price_change_for_it(self):
        """
        DESCRIPTION: Suspend one outcome and then trigger price change for it
        EXPECTED: *  'Price/Odds' button is disabled
        EXPECTED: *  'Price/Odds' button displays new price
        EXPECTED: *  Updated Previous Odds are displayed there as well
        """
        pass
