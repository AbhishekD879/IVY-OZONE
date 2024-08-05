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
class Test_C14890128_from_OX99_Betslip_verify_displaying_of_i_icon_for_single_line_accumulator(Common):
    """
    TR_ID: C14890128
    NAME: [from OX99] Betslip: verify displaying of 'i' icon for single line accumulator
    DESCRIPTION: This test case verifies displaying of 'i' icon for singles
    PRECONDITIONS: Add 2 selections from different events to the Betslip
    """
    keep_browser_open = True

    def test_001_verify_that_i_icon_is_displayed_next_to_the_selection(self):
        """
        DESCRIPTION: Verify that 'i' icon is displayed next to the selection
        EXPECTED: The 'i' icon is displayed next to the selection
        """
        pass

    def test_002_tap_on_i_icon_and_verify_that_it_is_tappable(self):
        """
        DESCRIPTION: Tap on 'i' icon and verify that it is tappable
        EXPECTED: - The 'i' icon is tappable
        EXPECTED: - The pop up is displayed
        """
        pass

    def test_003_verify_pop_up_content_for_double_bet(self):
        """
        DESCRIPTION: Verify pop up content for Double bet
        EXPECTED: Pop up content:
        EXPECTED: 'A Double is a bet on two selections, both of which must win to gain a return.'
        """
        pass

    def test_004_add_one_more_selection_from_other_event_to_the_betslipverify_that_treble_bet_is_displayed(self):
        """
        DESCRIPTION: Add one more selection from other event to the Betslip.
        DESCRIPTION: Verify that Treble bet is displayed
        EXPECTED: 'Treble' bet in Multiple selection is displayed
        """
        pass

    def test_005_verify_that_i_icon_is_displayed_next_to_the_selection(self):
        """
        DESCRIPTION: Verify that 'i' icon is displayed next to the selection
        EXPECTED: The 'i' icon is displayed next to the selection
        """
        pass

    def test_006_tap_on_i_icon_and_verify_that_it_is_tappable(self):
        """
        DESCRIPTION: Tap on 'i' icon and verify that it is tappable
        EXPECTED: - The 'i' icon is tappable
        EXPECTED: - The pop up is displayed
        """
        pass

    def test_007_verify_pop_up_content_for_treble_bet(self):
        """
        DESCRIPTION: Verify pop up content for Treble bet
        EXPECTED: Pop up content:
        EXPECTED: Treble: 'A Treble is a bet on three selections; all three of which must win to gain a return.'
        """
        pass

    def test_008_verify_that_i_icon_is_available_for_each_accumulator_bet_in_the_betslip(self):
        """
        DESCRIPTION: Verify that 'i' icon is available for each Accumulator bet in the Betslip
        EXPECTED: 'i' icon is available for each Multiple selections in the Betslip
        """
        pass

    def test_009_tap_on_i_icon_and_verify_that_it_is_tappable(self):
        """
        DESCRIPTION: Tap on 'i' icon and verify that it is tappable
        EXPECTED: - The 'i' icon is tappable
        EXPECTED: - The pop up is displayed
        """
        pass

    def test_010_verify_pop_up_content_for_accumulator_bet(self):
        """
        DESCRIPTION: Verify pop up content for Accumulator bet
        EXPECTED: Pop up content:
        EXPECTED: 'An Accumulator is a bet on four or more selections; all of which must win to gain a return.'
        """
        pass

    def test_011_verify_that_pop_up_is_closable_via_ok_button(self):
        """
        DESCRIPTION: Verify that pop up is closable via OK button
        EXPECTED: Pop up is closable via OK button
        """
        pass
