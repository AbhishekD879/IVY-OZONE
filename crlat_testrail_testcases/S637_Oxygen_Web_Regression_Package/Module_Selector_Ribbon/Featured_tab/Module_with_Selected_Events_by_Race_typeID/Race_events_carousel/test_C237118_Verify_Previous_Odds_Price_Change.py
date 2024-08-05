import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C237118_Verify_Previous_Odds_Price_Change(Common):
    """
    TR_ID: C237118
    NAME: Verify Previous Odds Price Change
    DESCRIPTION: This test case verify displaying of Previous odds under Price/Odds button
    DESCRIPTION: **NOTE:**
    DESCRIPTION: agreed with Adam Smith
    DESCRIPTION: that Previous Odds functionality is not applied for Featured module for now
    DESCRIPTION: (user can see previous odds appears under Price/Odds button if during live price update Feature module was active but in all other cases previous odds won't be displayed)
    DESCRIPTION: To implement Previous Odd to be displayed on Featured module changes should be made for featured microservice
    DESCRIPTION: no an issue according to comment in https://jira.egalacoral.com/browse/BMA-19508
    PRECONDITIONS: 1) CMS: https://**CMS_ENDPOINT**/keystone/modular-content/ (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: 2) Make sure events are available within module created by <Race> type ID for current day
    PRECONDITIONS: 3) To retrieve an information from Site Server about Previous Odds use link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZZZ?simpleFilter=event.suspendAtTime:greaterThan:####-##-##T##:##:##.###Z&racingForm=outcome&racingForm=event&priceHistory=true&prune=event&prune=market&translationLang=en
    PRECONDITIONS: *X.XX* - current supported version of OpenBet release
    PRECONDITIONS: *ZZZZZZ* - an event id
    PRECONDITIONS: *####-##-##T##:##:##.###Z* - date and time until event won't be suspended
    PRECONDITIONS: NOTE: This test case should check also Virtual Horses/Greyhounds events within Featured Module.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_module_selector_ribbon__gt_module_created_by_ltracegt_type_id(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon -&gt; Module created by &lt;Race&gt; type ID
        EXPECTED: * 'Feature' tab is selected by default
        EXPECTED: * Module created by &lt;Race&gt; type ID is shown
        """
        pass

    def test_003_in_the_ltracegt_events_carousel_find_event_with_live_price_available(self):
        """
        DESCRIPTION: In the '&lt;Race&gt; events carousel' find event with 'Live Price' available
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
        EXPECTED: * Only 2 last Previous Odds are displayed in format X/X&gt;X/X (older one goes first)
        """
        pass

    def test_006_verify_previous_odds_correctness(self):
        """
        DESCRIPTION: Verify Previous Odds correctness
        EXPECTED: * Previous Odds correspond to **livePriceNum** and **livePriceDen** attributes from tag *&lt;historicPrice .../&gt;*  in fractional format
        EXPECTED: *  Previous Odds correspond to **'livePriceDec'** attributes from tag *&lt;historicPrice .../&gt;*  in decimal format
        EXPECTED: * Previous odds are ordered according to **'displayOrder'** attribute (the biggest - the last)
        """
        pass

    def test_007_collapse_featured_module_and_trigger_price_change_for_some_selection(self):
        """
        DESCRIPTION: Collapse featured module and trigger price change for some selection
        EXPECTED: After module is expanded updated Previous Odds are displayed correctly
        """
        pass
