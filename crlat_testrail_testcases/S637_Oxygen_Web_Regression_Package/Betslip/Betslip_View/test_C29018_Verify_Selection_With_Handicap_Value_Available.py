import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29018_Verify_Selection_With_Handicap_Value_Available(Common):
    """
    TR_ID: C29018
    NAME: Verify Selection With Handicap Value Available
    DESCRIPTION: This selection verifies how the selection with handicap value will be shown on the Bet Slip
    DESCRIPTION: NOTE, User Story **BMA-5049**
    DESCRIPTION: AUTOTEST [C528145]
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'handicapValueDec' **on outcome level- to see whether handicap value is available for outcome
    """
    keep_browser_open = True

    def test_001_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_add_one_or_several_football_selections_to_the_bet_slipwith_handicap_value_available(self):
        """
        DESCRIPTION: Add one or several <football> selections to the Bet Slip
        DESCRIPTION: with handicap value available
        EXPECTED: Selections are added
        """
        pass

    def test_003_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_004_verify_selectionname(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: The following info is displayed on the Bet Slip for selections:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Handicap vaue is shown near the selection name in parentheses
        EXPECTED: 3.  Market type (**'name'** attribute on the market level)
        EXPECTED: 4. Event namee
        EXPECTED: 5. Selection odds ('livePriceNum'/'livePriceDen' attributes in fraction format OR 'price Dec' in decimal format)
        """
        pass

    def test_005_verify_handicap_value(self):
        """
        DESCRIPTION: Verify handicap value
        EXPECTED: Handicap value corresponds to the **'handicapValueDec'** from the Site Server response
        """
        pass

    def test_006_verify_the_handicap_value_displaying(self):
        """
        DESCRIPTION: Verify the handicap value displaying
        EXPECTED: Handicap value is displayed directly to the right of the outcome names and is displayed in parentheses
        EXPECTED: (e.g. <Outcome Name> (handicap value))
        """
        pass

    def test_007_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: *   If **'handicapValueDec' **contains '-' sign - display it with this '-' sign (negative value) on the front end (eg. -1 )
        EXPECTED: *   If **'handicapValueDec'** contains '+' sign in the response - display '+' sign before the value on front end (eg. +3 )
        EXPECTED: *   If **'handicapValueDec'** doesn't contain any sign (e.g. 2) - display '+' sign before the value on the front end
        """
        pass

    def test_008_verify_selections_without_handicap_value_available(self):
        """
        DESCRIPTION: Verify selections without handicap value available
        EXPECTED: Handicap value is NOT shown near the outcome name
        """
        pass

    def test_009_verify_stake__estimated_returns_total_est_returnstotal_potential_returns_fields(self):
        """
        DESCRIPTION: Verify 'Stake:' , 'Estimated Returns', 'Total Est. Returns/Total Potential returns' fields
        EXPECTED: All fields are shown
        """
        pass

    def test_010_verify_x_icon_and_bet_now_buttons(self):
        """
        DESCRIPTION: Verify 'X' icon and 'Bet Now' buttons
        EXPECTED: Buttons are present and shown
        """
        pass
