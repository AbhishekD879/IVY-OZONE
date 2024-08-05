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
class Test_C820400_Tracking_of_Quick_Bet_when_screen_resolution_is_changed(Common):
    """
    TR_ID: C820400
    NAME: Tracking of Quick Bet when screen resolution is changed
    DESCRIPTION: This test case verifies tracking of Quick Bet when screen resolution is changed
    PRECONDITIONS: * Quick Bet functionality is enabled in CMS
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Make sure you have device that has Mobile view in portrait mode and Tablet view in landscape mode
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    """
    keep_browser_open = True

    def test_001_tap_one_sportrace_selection_from_homepage(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection from homepage
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_002_enter_value_in_stake_field_and_check_ew_checkbox_if_available(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox (if available)
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_003_change_screen_resolutioneg_rotate_device_to_landscape_mode(self):
        """
        DESCRIPTION: Change screen resolution
        DESCRIPTION: e.g rotate device to landscape mode
        EXPECTED: * Quick bet is displayed
        EXPECTED: * Selection remains added
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'add to quickbet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'add': {
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<EVENT NAME>>',  **e.g. 'Kempton- 19:55'**
        EXPECTED: 'category': '<<EVENT CATEGORY>>', **e.g. '21'**
        EXPECTED: 'variant': '<<EVENT TYPE>>', **e.g. '1941'**
        EXPECTED: 'brand': '<<EVENT MARKET NAME>>', **e.g. 'Win or EW'**
        EXPECTED: 'cd100': '<<EVENT ID>>', **e.g. '11564441'**
        EXPECTED: 'cd101': '<<SELECTION ID>>', **e.g. '852419294'**
        EXPECTED: 'cd102': <<IN PLAY STATUS>>,
        EXPECTED: **'cd102' = '1' belongs to In Play event**
        EXPECTED: **'cd102' = '0' belongs to Pre Match event**
        EXPECTED: 'cd106': <<CUSTOMER BUILT>>,
        EXPECTED: **'cd106' = '1' bet type = BYB**
        EXPECTED: **'cd106' = '0' bet was built by Trader**
        EXPECTED: 'cd107': '<<LOCATION>>', **e.g. "Matches. Today" - the page bet originated from**
        EXPECTED: 'cd108': '<<MODULE>>' **e.g. "England - Premier League" - the accordion bet originated from**
        EXPECTED: }]
        EXPECTED: Parameters 'category', 'variant',  'cd100' and 'cd101' correspond to Openbet info for event that was added to Quick Bet
        """
        pass
