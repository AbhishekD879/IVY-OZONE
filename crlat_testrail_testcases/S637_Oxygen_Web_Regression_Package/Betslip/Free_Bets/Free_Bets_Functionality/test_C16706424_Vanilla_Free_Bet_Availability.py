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
class Test_C16706424_Vanilla_Free_Bet_Availability(Common):
    """
    TR_ID: C16706424
    NAME: [Vanilla] Free Bet Availability
    DESCRIPTION: This test case verifies 'Free Bet' list
    PRECONDITIONS: User should have multiple Free Bets available on their account
    PRECONDITIONS: NOTE: Contact Coral UAT for assistance with applying free bet tokens to the relevant test accounts
    """
    keep_browser_open = True

    def test_001_log_in_to_applicaiton(self):
        """
        DESCRIPTION: Log in to applicaiton
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip and open Betslip
        EXPECTED: Betslip is open
        """
        pass

    def test_003_verify_if_use_free_bet_link_is_available_for_selection(self):
        """
        DESCRIPTION: Verify if 'Use Free Bet' link is available for selection
        EXPECTED: 'Use Free Bet' link is available below market name in selection section
        """
        pass

    def test_004_tap_use_free_bet_link_in_selection_section(self):
        """
        DESCRIPTION: Tap 'Use Free Bet' link in selection section
        EXPECTED: Free Bets Available pop-up is open that contains:
        EXPECTED: * Header with number of available free bets 'Free Bets Available (x&lt;number&gt;)'
        EXPECTED: * Close button on the header ('X')
        EXPECTED: * List of available free bets in the following format: &lt;currency&gt;&lt;amount&gt;&lt;name&gt;&lt;type&gt;, for example '$15.00 FreeBet Name (Any)'
        """
        pass

    def test_005_select_one_of_available_free_bet(self):
        """
        DESCRIPTION: Select one of available free bet
        EXPECTED: * Selected Free Bet has dialog box marked as selected
        EXPECTED: * Pop-up is closed after tapping 'add' button
        EXPECTED: * 'Use Free Bet' link is changed to '- Remove Free Bet' link
        """
        pass

    def test_006_verify_estimated_returns_value_when_free_bet_is_selected(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value when free bet is selected
        EXPECTED: 'Estimated Returns' is calculated based on formula:
        EXPECTED: **Free Bet Value * Odds** - if odds have a fractional format
        EXPECTED: **Free Bet Value * Odds - Free Bet Value** - if odds have a decimal format
        """
        pass

    def test_007_press_on___remove_free_bet_link(self):
        """
        DESCRIPTION: Press on "- Remove Free Bet" link
        EXPECTED: * '- Remove Free Bet' link is changed to 'Use Free Bet' link
        EXPECTED: * 'Estimated Returns' is changed to 0.00
        """
        pass

    def test_008_add_few_more_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add few more selections to the Betslip
        EXPECTED: Betslip counter is increased, added selection are present in the Betslip
        """
        pass

    def test_009_go_to_selection_1_and_tap_use_free_bet_link_and_choose_one_of_available_free_bets(self):
        """
        DESCRIPTION: Go to selection #1 and tap 'Use Free Bet' link and choose one of available free bets
        EXPECTED: Free bet is chosen successfully
        """
        pass

    def test_010_go_to_selection_2_and_tap_use_free_bet_link_and_verify_list_of_free_bets(self):
        """
        DESCRIPTION: Go to selection #2 and tap 'Use Free Bet' link and verify list of free bets
        EXPECTED: Free bet that has been chosen for selection #1 is not shown on the list of free bets for selection #2
        """
        pass

    def test_011_add_few_more_selections_to_the_betslip_so_quantity_of_selections_is_bigger_than_quantity_of_free_bets_available_for_user(self):
        """
        DESCRIPTION: Add few more selections to the Betslip, so quantity of selections is bigger than quantity of Free Bets available for User
        EXPECTED: Betslip counter is increased, added selection are present in the Betslip
        """
        pass

    def test_012_add_all_available_free_bets_to_selections(self):
        """
        DESCRIPTION: Add all available Free Bets to selections
        EXPECTED: * 'Use Free Bet link is changed to '- Remove Free Bet' link for selections with Free Bets added
        EXPECTED: * After User has added all available Free Bets to selections, "Use Free Bet" link for other selections is greyed out and non-clickable
        """
        pass
