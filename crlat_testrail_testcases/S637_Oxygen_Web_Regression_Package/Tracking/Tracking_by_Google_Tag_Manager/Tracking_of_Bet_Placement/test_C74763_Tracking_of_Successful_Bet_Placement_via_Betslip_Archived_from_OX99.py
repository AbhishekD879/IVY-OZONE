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
class Test_C74763_Tracking_of_Successful_Bet_Placement_via_Betslip_Archived_from_OX99(Common):
    """
    TR_ID: C74763
    NAME: Tracking of Successful Bet Placement via Betslip [Archived from OX99]
    DESCRIPTION: This test case verify tracking of successful bet placement
    PRECONDITIONS: * App is loaded
    PRECONDITIONS: * Quick Bet functionality is disabled in CMS or user`s settings
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * Browser console is opened
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop
    """
    keep_browser_open = True

    def test_001_add_a_selections_and_open_betslip_singles_sections(self):
        """
        DESCRIPTION: Add a selections and open Betslip, **'Single(s) section(s)**
        EXPECTED: * Betslip is opened
        EXPECTED: * Selection(s) is added
        """
        pass

    def test_002_enter_the_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Enter the stake and place a bet
        EXPECTED: - Bet is placed successfully
        EXPECTED: - Bet Receipt is displayed with unique **Bet ID**
        EXPECTED: (e.g. O/0123828/0000155)
        EXPECTED: **NOTE** Remember the **Bet ID**
        """
        pass

    def test_003_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        EXPECTED: Next paramantres are dispayed:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'betslip',
        EXPECTED: 'eventAction': 'place bet',
        EXPECTED: 'eventLabel': 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': **e.g. 'O/161000780/0000280'**
        EXPECTED: 'revenue': <<TOTAL STAKE>>
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<FOLD TYPE>>', **e.g. 'single''
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
        EXPECTED: 'cd103': <<BET LINES>>,  **e.g. '1,2,3' - The number of bet lines in that specific bet**
        EXPECTED: 'cd104': <<BET ODDS>>,  **e.g. '1.22' - The odds of the bet as a decimal**
        EXPECTED: 'cd106': <<CUSTOMER BUILT>>,
        EXPECTED: **'cd106' = '1' bet type = BYB**
        EXPECTED: **'cd106' = '0' bet was built by Trader**
        EXPECTED: 'cd107': '<<LOCATION>>',  **'Matches. Today" - the page bet originated from**
        EXPECTED: 'cd108': '<<MODULE>>'  **'England - Premier League" - the accordion bet originated from**
        EXPECTED: 'cm10': <<BONUS STAKE>> **e.g. '5.00' - The free bet amount placed**
        EXPECTED: 'name': '<<#2- FOLD TYPE>>',
        EXPECTED: 'id': '<<#2- RECEIPT ID>>',
        EXPECTED: 'price': <<#2- STAKE AMOUNT>>,
        EXPECTED: 'category': '<<#2- EVENT CATEGORY>> ',
        EXPECTED: 'variant': '<<#2- EVENT TYPE>>',
        EXPECTED: 'brand': '<<#2- EVENT MARKET>>',
        EXPECTED: 'cd100': '<<#2- EVENT>>',
        EXPECTED: 'cd101': '<<#2- SELECTION ID>>',
        EXPECTED: 'cd102': <<#2- IN PLAY STATUS>>,
        EXPECTED: 'cd103': <<#2- BET LINES>>,
        EXPECTED: 'cd104': <<#2- BET ODDS>>,
        EXPECTED: 'cd106': <<#2- CUSTOMER BUILT>>,
        EXPECTED: 'cd107': '<<LOCATION>>',
        EXPECTED: 'cd108': '<<MODULE>>'
        EXPECTED: 'cm10': <<#2- BONUS STAKE>>
        EXPECTED: Parameters 'category', 'variant' and 'cd100' correspond to Openbet info for event that was added to Betslip
        """
        pass

    def test_004_tap_done_button(self):
        """
        DESCRIPTION: Tap 'Done' button
        EXPECTED: Bet Receipt is closed
        """
        pass

    def test_005_repeat_steps_3_7_for_multiple_bet(self):
        """
        DESCRIPTION: Repeat steps #3-7 for Multiple bet
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventCategory': 'betslip',
        EXPECTED: 'eventAction': 'place bet',
        EXPECTED: 'eventLabel': 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': '{First Receipt ID}:{# of bets}', // e.g. O/161000780/0000280:2
        EXPECTED: 'revenue': <<TOTAL STAKE>>
        EXPECTED: 'products': [{
        EXPECTED: 'name': '<<FOLD TYPE>>', **double, treble etc.**
        EXPECTED: 'id': '<<RECEIPT ID>>',
        EXPECTED: 'price': <<STAKE AMOUNT>>
        EXPECTED: 'category': '<<#1- EVENT CATEGORY>> ', **multiple**
        EXPECTED: 'variant': '<<#1- EVENT TYPE>>', **multiple**
        EXPECTED: 'brand': '<<#1- EVENT MARKET>>', **multiple**
        EXPECTED: 'cd100': '<<#1- EVENT>>', **multiple**
        EXPECTED: 'cd101': '<<#1- SELECTION ID>>',  **"894479298,894483825,894483979"**
        EXPECTED: 'cd102': <<#1- IN PLAY STATUS>>,
        EXPECTED: 'cd103': <<#1- BET LINES>>,
        EXPECTED: 'cd104': <<#1- BET ODDS>>,
        EXPECTED: 'cd106': <<#1- CUSTOMER BUILT>>,
        EXPECTED: 'cd107': '<<#1- LOCATION>>',
        EXPECTED: 'cd108': '<<#1- MODULE>>',
        EXPECTED: 'cm10': <<#1- BONUS STAKE>>
        """
        pass

    def test_006_tap_reuse_selection_and_repeat_steps_2_5(self):
        """
        DESCRIPTION: Tap 'Reuse Selection' and repeat steps #2-5
        EXPECTED: 
        """
        pass
