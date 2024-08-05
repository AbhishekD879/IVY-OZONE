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
class Test_C820091_Tracking_of_tapping_Add_to_Betslip_button(Common):
    """
    TR_ID: C820091
    NAME: Tracking of tapping 'Add to Betslip' button
    DESCRIPTION: This test case verifies tracking of tapping 'Add to Betslip' button within Quick Bet
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Quick Bet functionality is enabled in CMS or user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: AUTOTEST: [C1288738]
    """
    keep_browser_open = True

    def test_001_add_sportrace_selection_from_homepage_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/<Race> selection from homepage to Quick Bet
        EXPECTED: Quick Bet appears at the bottom of the page
        """
        pass

    def test_002_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'ADD TO BETSLIP' button
        EXPECTED: Quick Bet is closed after tapping 'ADD TO BETSLIP' button
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
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
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Quick Bet
        """
        pass

    def test_004_remove_selection_from_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip
        EXPECTED: 
        """
        pass

    def test_005_add_race_selection_to_quick_bet_with_each_way_option_available(self):
        """
        DESCRIPTION: Add <Race> selection to Quick Bet with Each Way option available
        EXPECTED: * Quick Bet appears at the bottom of the page
        EXPECTED: * 'E/W' checkbox is displayed within Quick Bet
        """
        pass

    def test_006_enter_value_in_stake_field_and_check_ew_checkbox(self):
        """
        DESCRIPTION: Enter value in 'Stake' field and check 'E/W' checkbox
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'E/W' checkbox is selected
        """
        pass

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps #2-3
        EXPECTED: 
        """
        pass
