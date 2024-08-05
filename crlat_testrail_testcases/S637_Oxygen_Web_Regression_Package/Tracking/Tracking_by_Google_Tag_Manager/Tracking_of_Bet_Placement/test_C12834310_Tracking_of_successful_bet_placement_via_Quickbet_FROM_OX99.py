import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C12834310_Tracking_of_successful_bet_placement_via_Quickbet_FROM_OX99(Common):
    """
    TR_ID: C12834310
    NAME: Tracking of successful bet placement via Quickbet [FROM OX99]
    DESCRIPTION: This test case verifies GA tracking of successful bet placement via Quickbet
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Quick Bet GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91470520
    PRECONDITIONS: - Quick bet should be enabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should be logged in
    PRECONDITIONS: - You should have a selection added to Quickbet and Quickbet should be opened
    """
    keep_browser_open = True

    def test_001___make_a_stake_and_tap_bet_now__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Make a stake and tap 'BET NOW'
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'quickbet',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': '{Receipt ID}:{number of bets}', // e.g. O/161000780/0000280:1
        EXPECTED: 'revenue': <<TOTAL STAKE>>, **e.g. '5.00'**
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: brand: "<<EVENT_MARKET>>", **e.g. ‘Match Result’**
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>", **e.g. '21'**
        EXPECTED: dimension60: "<<EVENT_ID>>", **e.g. '11564441'**
        EXPECTED: dimension61: "<<SELECTION_ID>>", **e.g. '852419294'**
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>",
        EXPECTED: **'dimension62' = '1' belongs to In Play event**
        EXPECTED: **'dimension62' = '0' belongs to Pre Match event**
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>",
        EXPECTED: **'dimension63’ = '1' bet placed by user**
        EXPECTED: **'dimension63’ = '0' bet was built by Trader**
        EXPECTED: dimension64: "<<LOCATION>>", **e.g. "Matches. Today" - the page bet originated from**
        EXPECTED: dimension65: "<<MODULE>>”, **e.g. "event card"**
        EXPECTED: dimension66: "<<NUMBER_OF_BET_LINES>>"
        EXPECTED: dimension67: "ODDS" ( **in decimal format** )
        EXPECTED: id: "<<BET_ID>>", **e.g. O/161000780/0000280'**
        EXPECTED: cm1: "<<BONUS_STAKE_AMOUNT>>”,  **e.g. '5.00' - The total bonus stake amount associated with that specific bet**
        EXPECTED: name: "<<BET_TYPE>>"', **e.g. 'single, double, etc.''
        EXPECTED: price: "<<STAKE>>", **e.g. '5.75' (including bonus stake)**
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>", **e.g. ‘442’**
        EXPECTED: }}
        """
        pass
