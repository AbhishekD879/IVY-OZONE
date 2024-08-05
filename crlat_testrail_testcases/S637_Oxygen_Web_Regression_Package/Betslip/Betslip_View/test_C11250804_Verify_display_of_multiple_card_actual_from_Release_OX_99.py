import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C11250804_Verify_display_of_multiple_card_actual_from_Release_OX_99(Common):
    """
    TR_ID: C11250804
    NAME: Verify display of multiple card [actual from Release OX 99]
    DESCRIPTION: This test case verifies displaying of multiple card
    DESCRIPTION: AUTOTEST [C15250086]
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001_add_2_or_more_selections_from_different_events_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add 2 or more selections from different events to the Betslip and open Betslip
        EXPECTED: The bet slip is displayed
        """
        pass

    def test_002_verify_that_the_multiple_card_is_displayed_in_multiple_section_under_single_section(self):
        """
        DESCRIPTION: Verify that the multiple card is displayed in 'Multiple' section under 'Single' section
        EXPECTED: The multiple card is displayed in 'Multiple' section under 'Single' section
        """
        pass

    def test_003_verify_the_card_elements(self):
        """
        DESCRIPTION: Verify the card elements
        EXPECTED: The card should contain:
        EXPECTED: - multiple bet type name (multiples will include number of bets e.g. acca = x1)
        EXPECTED: price
        EXPECTED: - 'estimated returns' / 'potential returns' for that individual bet
        EXPECTED: stake box
        EXPECTED: - bet type summary info
        """
        pass

    def test_004_verify_bet_type_summary_info_text(self):
        """
        DESCRIPTION: Verify bet type summary info text
        EXPECTED: Bet summary info text:
        EXPECTED: - Trixie: '3 doubles and a treble'
        EXPECTED: - Fourfold: 'Accumulator Bet'
        EXPECTED: (Continued for Fivefold to Twentyfold as above)
        EXPECTED: - Patent: ' 3 singles, 3 doubles and a treble'
        EXPECTED: - Yankee: '6 doubles, 4 trebles and a fourfold accumulator'
        EXPECTED: - Canadian: '10 doubles, 10 trebles, 5 fourfolds and a fivefold accumulator'
        EXPECTED: - Heinz: '15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator'
        EXPECTED: - Super Heinz: '21 doubles, 35 trebles, 35 fourfolds, 21 fivefolds, 7 sixfolds and a sevenfold accumulator'
        EXPECTED: - Goliath: '28 doubles, 56 trebles, 70 fourfolds, 56 fivefolds, 28 sixfolds, 8 sevenfolds and an eightfold accumulator'
        EXPECTED: - Lucky 15: '4 singles, 6 doubles, 4 trebles and a fourfold accumulator'
        EXPECTED: - Lucky 31: '5 singles, 10 doubles, 10 trebles, 5 fourfolds and a fivefold accumulator'
        EXPECTED: - Lucky 63: '6 singles, 15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator'
        """
        pass
