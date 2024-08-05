import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C17699641_Tracking_of_successful_multiples_bet_placement_via_Betslip_FROM_OX99(Common):
    """
    TR_ID: C17699641
    NAME: Tracking of successful multiples bet placement via Betslip [FROM OX99]
    DESCRIPTION: This test case verifies GA tracking of successful multiples bet placement via Betslip
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - Betslip GA tracking documentation: https://confluence.egalacoral.com/pages/viewpage.action?pageId=91091847
    PRECONDITIONS: - Quick bet should be disabled in CMS > System Configuration > Structure > quickBet
    PRECONDITIONS: - You should be logged in
    """
    keep_browser_open = True

    def test_001_add_the_selections_to_the_betslip_from__different_events__the_area_eg_featured__the_same_category_eg_football__the_same_type_eg_premier_league__the_same_market_eg_match_result(self):
        """
        DESCRIPTION: Add the selections to the Betslip from:
        DESCRIPTION: - Different events
        DESCRIPTION: - The area (e.g. Featured)
        DESCRIPTION: - The same category (e.g. Football)
        DESCRIPTION: - The same type (e.g. Premier League)
        DESCRIPTION: - The same market (e.g. Match Result)
        EXPECTED: - Selections are added to the Betslip
        """
        pass

    def test_002___make_a_stake_for_multiples_and_tap_bet_now__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Make a stake for multiples and tap 'BET NOW'
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost : "no" or "yes",
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': '{Receipt ID}:{number of bets}', // e.g. O/161000780/0000280:1
        EXPECTED: 'revenue': <<TOTAL STAKE>>, **e.g. '5.00'**
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: brand: "<<EVENT_MARKET>>", **e.g. ‘Match Result’**
        EXPECTED: category: "<<OPENBET_SPORT_CATEGORY_ID>>", **e.g. '21'**
        EXPECTED: dimension60: "multiple",
        EXPECTED: dimension61: "<<SELECTION_ID1, SELECTION_ID2, ...>>", **e.g. '852419294', '852419295', ...**
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>",
        EXPECTED: **'dimension62' = '1' belongs to In Play event**
        EXPECTED: **'dimension62' = '0' belongs to Pre Match event**
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>",
        EXPECTED: **'dimension63’ = '1' bet type = BYB**
        EXPECTED: **'dimension63’ = '0' bet was built by Trader or User**
        EXPECTED: dimension64: "<<LOCATION>>", **e.g. "IN-PLAY" - the page bet originated from**
        EXPECTED: dimension65: "<<MODULE>>”, **e.g. "event card"**
        EXPECTED: dimension66: "<<NUMBER_OF_BET_LINES>>"
        EXPECTED: dimension67: "ODDS" ( **in decimal format** )
        EXPECTED: id: "<<BET_ID>>", **e.g. O/161000780/0000280'**
        EXPECTED: cm1: "<<BONUS_STAKE_AMOUNT>>”,  **e.g. '5.00' - The total bonus stake amount associated with that specific bet**
        EXPECTED: name: "<<BET_TYPE>>"', **e.g. 'double', 'treble', etc.''
        EXPECTED: price: "<<STAKE>>", **e.g. '5.75' (including bonus stake)**
        EXPECTED: variant: "<<OPENBET_TYPE_ID>>", **e.g. ‘442’**
        EXPECTED: })
        """
        pass

    def test_003_add_the_selections_to_the_betslip_from__different_events__different_areas_eg_featured_and_matches__different_categories_eg_football_and_basketball__different_types_eg_premier_league_and_nba__different_markets_eg_match_result_and_money_line(self):
        """
        DESCRIPTION: Add the selections to the Betslip from:
        DESCRIPTION: - Different events
        DESCRIPTION: - Different areas (e.g. Featured and Matches)
        DESCRIPTION: - Different categories (e.g. Football and Basketball)
        DESCRIPTION: - Different types (e.g. Premier League and NBA)
        DESCRIPTION: - Different markets (e.g. Match Result and Money Line)
        EXPECTED: - Selections are added to the Betslip
        """
        pass

    def test_004___make_a_stake_for_multiples_and_tap_bet_now__type_datalayer_in_browsers_console_and_verify_ga_tracking_record(self):
        """
        DESCRIPTION: - Make a stake for multiples and tap 'BET NOW'
        DESCRIPTION: - Type 'dataLayer' in browser's console and verify GA tracking record
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'betslip',
        EXPECTED: 'eventAction' : 'place bet',
        EXPECTED: 'eventLabel' : 'success',
        EXPECTED: 'oddsBoost : "no" or "yes",
        EXPECTED: 'ecommerce': {
        EXPECTED: 'purchase': {
        EXPECTED: 'actionField': {
        EXPECTED: 'id': '{Receipt ID}:{number of bets}', // e.g. O/161000780/0000280:1
        EXPECTED: 'revenue': <<TOTAL STAKE>>, **e.g. '5.00'**
        EXPECTED: },
        EXPECTED: 'products': [{
        EXPECTED: brand: "multiple",
        EXPECTED: category: "multiple",
        EXPECTED: dimension60: "multiple",
        EXPECTED: dimension61: "<<SELECTION_ID1, SELECTION_ID2, ...>>", **e.g. '852419294', '852419295', ...**
        EXPECTED: dimension62: "<<IN-PLAY_STATUS>>",
        EXPECTED: **'dimension62' = '1' belongs to In Play event**
        EXPECTED: **'dimension62' = '0' belongs to Pre Match event**
        EXPECTED: dimension63: "<<CUSTOMER BUILT>>",
        EXPECTED: **'dimension63’ = '1' bet type = BYB**
        EXPECTED: **'dimension63’ = '0' bet was built by Trader or User**
        EXPECTED: dimension64: "multiple",
        EXPECTED: dimension65: "multiple",
        EXPECTED: dimension66: "<<NUMBER_OF_BET_LINES>>"
        EXPECTED: dimension67: "ODDS" ( **in decimal format** )
        EXPECTED: id: "<<BET_ID>>", **e.g. O/161000780/0000280'**
        EXPECTED: cm1: "<<BONUS_STAKE_AMOUNT>>”,  **e.g. '5.00' - The total bonus stake amount associated with that specific bet**
        EXPECTED: name: "<<BET_TYPE>>"', **e.g. 'double', 'treble', etc.''
        EXPECTED: price: "<<STAKE>>", **e.g. '5.75' (including bonus stake)**
        EXPECTED: variant: "multiple"
        EXPECTED: })
        """
        pass
