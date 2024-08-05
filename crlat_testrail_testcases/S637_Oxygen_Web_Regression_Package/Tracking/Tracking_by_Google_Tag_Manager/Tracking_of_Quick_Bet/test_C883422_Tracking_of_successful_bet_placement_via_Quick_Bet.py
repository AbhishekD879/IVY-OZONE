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
class Test_C883422_Tracking_of_successful_bet_placement_via_Quick_Bet(Common):
    """
    TR_ID: C883422
    NAME: Tracking of successful bet placement via Quick Bet
    DESCRIPTION: This test case verifies successful bet placement within Quick bet
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * To view response open Dev tools -> Network -> WS -> choose the last request
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: **New Quickbet tracking parameters:** https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: AUTOTEST: [C1296218]
    """
    keep_browser_open = True

    def test_001_tap_one_sportrace_selection(self):
        """
        DESCRIPTION: Tap one <Sport>/<Race> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_002_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        """
        pass

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass

    def test_004_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': '{First Receipt ID}:{# of bets}', // e.g. O/161000780/0000280:1
        EXPECTED: 'revenue': <<TOTAL STAKE>> **e.g. '5.00'**
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<FOLD TYPE>>', **e.g. 'single, double, etc.''
        EXPECTED: 'id': '<<RECEIPT ID>>', **e.g. O/161000780/0000280'**
        EXPECTED: 'price': <<#STAKE AMOUNT>>, **e.g. '5.75' (including bonus stake)**
        EXPECTED: 'category': '<<EVENT CATEGORY>> ', **e.g. '21'**
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
        EXPECTED: 'cm10': <<BONUS STAKE>> **e.g. '5.00' - The total bonus stake amount associated with that specific bet**
        EXPECTED: }]
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Quick Bet
        """
        pass
