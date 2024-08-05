import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1391619_Tracking_of_Collapsing_Expanding_module(Common):
    """
    TR_ID: C1391619
    NAME: Tracking of Collapsing/Expanding module
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of Collapse/Expand the market in #Build Your Bet tab within the EDP
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Navigate to Football Landing page
    PRECONDITIONS: 4. Go to the Event details page with the BYB (Leagues with available BYB are marked with BYB icon on accordion) > 'Build Your Bet' tab
    """
    keep_browser_open = True

    def test_001_expand_a_market_for_the_first_time(self):
        """
        DESCRIPTION: Expand a market for the first time
        EXPECTED: Market is expanded
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'expand market accordion' }
        EXPECTED: )
        """
        pass

    def test_003_collapse_the_same_market_for_the_first_time(self):
        """
        DESCRIPTION: Collapse the same market for the first time
        EXPECTED: Market is collapsed
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'build bet',
        EXPECTED: 'eventLabel' : 'collapse market accordion' }
        EXPECTED: )
        """
        pass

    def test_005_expand_and_collapse_the_market_one_more_time(self):
        """
        DESCRIPTION: Expand and collapse the market one more time
        EXPECTED: Market is collapsed
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is **NOT** present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'your call',
        EXPECTED: 'eventAction' : 'match bet',
        EXPECTED: 'eventLabel' : '<< ACTION >>' //e.g. 'expand market accordion', 'collapse accordion market'
        EXPECTED: })
        """
        pass
