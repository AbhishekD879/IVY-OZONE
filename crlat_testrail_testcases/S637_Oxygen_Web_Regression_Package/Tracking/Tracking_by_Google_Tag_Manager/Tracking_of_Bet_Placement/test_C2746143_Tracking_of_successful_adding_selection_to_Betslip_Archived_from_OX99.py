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
class Test_C2746143_Tracking_of_successful_adding_selection_to_Betslip_Archived_from_OX99(Common):
    """
    TR_ID: C2746143
    NAME: Tracking of successful adding selection to Betslip [Archived from OX99]
    DESCRIPTION: This test case verifies tracking of successful adding selection to Betslip
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Quick Bet functionality is disabled in CMS or user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop
    """
    keep_browser_open = True

    def test_001_add_sportrace_selection_to_betslip(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection to Betslip
        EXPECTED: 
        """
        pass

    def test_002_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'add to betslip',
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
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Betslip
        """
        pass
