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
class Test_C2032797_Tracking_of_clicking_on_Odds_Format_selector_on_Desktop_Universal_Header_on_the_Homepage(Common):
    """
    TR_ID: C2032797
    NAME: Tracking of clicking on 'Odds Format' selector on Desktop Universal Header on the Homepage
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer when clicking on 'Odds Format' selector on Desktop Universal Header on the Homepage.
    DESCRIPTION: Need to run the test case on Desktop.
    PRECONDITIONS: 1. Browser console should be opened
    PRECONDITIONS: 2. User is Logged In
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is loaded
        EXPECTED: * 'Odds Format' selector is displayed at Desktop Universal Header
        EXPECTED: * 'Fractional' option is selected by default
        """
        pass

    def test_002_click_on_odds_format_selector_at_desktop_universal_header(self):
        """
        DESCRIPTION: Click on 'Odds Format' selector at Desktop Universal Header
        EXPECTED: * Dropdown list with 'Fractional' and 'Decimal' options is opened
        EXPECTED: * Possible to choose appropriate Odds Format from dropdown list
        """
        pass

    def test_003_choose_decimal_option_in_odds_format_selector(self):
        """
        DESCRIPTION: Choose 'Decimal' option in 'Odds Format' selector
        EXPECTED: 'Decimal' option is displayed in 'Odds Format' selector
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'navigation',
        EXPECTED: 'eventAction' a: 'secondary',
        EXPECTED: 'eventLabel' : '<< NAV ITEM >>' //e.g. change odds
        EXPECTED: })
        """
        pass

    def test_005_repeat_steps_2_4_but_choose_fractional_option_from_odds_format_selector(self):
        """
        DESCRIPTION: Repeat steps 2-4 but choose 'Fractional' option from 'Odds Format' selector
        EXPECTED: 
        """
        pass
