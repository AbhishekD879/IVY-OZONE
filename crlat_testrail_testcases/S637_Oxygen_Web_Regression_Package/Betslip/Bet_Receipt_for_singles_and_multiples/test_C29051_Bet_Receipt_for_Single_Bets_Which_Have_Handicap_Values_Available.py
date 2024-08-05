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
class Test_C29051_Bet_Receipt_for_Single_Bets_Which_Have_Handicap_Values_Available(Common):
    """
    TR_ID: C29051
    NAME: Bet Receipt for Single Bets Which Have Handicap Values Available
    DESCRIPTION: This test case verifies Bet Receipt information on Bet Receipt page for Single Bets if all or some selections which have handicap values available are placed
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement for selection that has handicap values available
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_verify_bet_receipt_displaying_after_clickingtapping_the_bet_now_button(self):
        """
        DESCRIPTION: Verify Bet Receipt displaying after clicking/tapping the 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_002_verify_bet_receipt(self):
        """
        DESCRIPTION: Verify Bet Receipt
        EXPECTED: 1. Bet Receipt header and back button are present
        EXPECTED: 2. Bet Receipt contains the following information:
        EXPECTED: Bet Receipt details for each selection:
        EXPECTED: *   Boosted bet section (in case of bet has been boosted)
        EXPECTED: *   'Single' text on each card
        EXPECTED: *   Odds of the selection (for <Race> with 'SP' price - N/A) in the next format: i.e. @1/2 or @SP
        EXPECTED: *   Bet ID (Coral)/Receipt No (Ladbrokes). It starts with O and contains numeric values - i.e. O/0123828/0000155
        EXPECTED: *   The outcome name
        EXPECTED: *   Outcome name contains handicap value near the name (if such are available for outcomes)
        EXPECTED: *   Market type user has bet on - i.e. Win or Each Way and Event name to which the outcome belongs to. Should display in the next format: Market Name/Event Name
        EXPECTED: *  'CashOut' label if available
        EXPECTED: *  'Promo' icon if available (Ladbrokes only)
        EXPECTED: *  'Favourites' icon for Football stakes (Coral only)
        EXPECTED: *  'Win Alerts' toggle (Wrapper only)
        EXPECTED: *   Total Stake (Coral)/Stake for this bet (Ladbrokes)
        EXPECTED: *   Free Bet Amount  (if Free bet was selected)
        EXPECTED: *   Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        EXPECTED: Total Bet Receipt details:
        EXPECTED: *   Total Stake
        EXPECTED: *   Est. Returns (Coral)/Potentials Returns (Ladbrokes) (for <Race> with 'SP' price - N/A)
        EXPECTED: 3. 'Reuse Selections' and 'Go Betting' buttons
        EXPECTED: 4. Player Bets clickable banner (only for events from the following leagues: Football: England - Premier League, Spain - La liga, Italy - Serie A, UEFA Champions League; Basketball: NBA; American Football: NFL) **NOTE:** Only for Mobile view
        EXPECTED: All information corresponds to the information about just placed bet
        """
        pass

    def test_003_verify_the_handicap_value(self):
        """
        DESCRIPTION: Verify the handicap value
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_004_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: * Handicap value is displayed directly to the right of the outcome names
        EXPECTED: * Handicap value is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_005_verify_handicap_value_sign(self):
        """
        DESCRIPTION: Verify handicap value sign
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end
        EXPECTED: *   If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass
